// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./interfaces/IDetCadetOracle.sol";
import "./interfaces/IRecoveryOracle.sol";
import "./TekTok.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract TekTokMonetaryPolicy is AccessControl {
    bytes32 public constant POLICY_ROLE = keccak256("POLICY_ROLE");
    TekTok public immutable token;
    IDetCadetOracle public poi;
    IRecoveryOracle public recovery;
    uint256 public maxWeeklyBps = 20; // 0.20% cap
    uint256 public lastMintWeek;
    event Minted(uint256 weekNo, uint256 amount, int256 poiScore, uint256 recUSD18);

    constructor(TekTok _token, IDetCadetOracle _poi, IRecoveryOracle _recovery) {
        token = _token; poi = _poi; recovery = _recovery;
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender); _grantRole(POLICY_ROLE, msg.sender);
    }
    function setOracles(IDetCadetOracle _poi, IRecoveryOracle _recovery) external onlyRole(POLICY_ROLE) {
        poi = _poi; recovery = _recovery;
    }
    function _week() internal view returns (uint256) { return block.timestamp / 1 weeks; }

    function mintAccordingToFeeds(address innovators, address treasury, address sustain) external onlyRole(POLICY_ROLE) {
        require(_week() > lastMintWeek, "cooldown");
        var p = poi.latest(); var r = recovery.latest();
        int256 score = p.score;
        uint256 cap = token.totalSupply() + (10**24); // example cap logic
        uint256 maxWeekly = cap * maxWeeklyBps / 10000;
        uint256 byPoi = score > 0 ? uint256(score) / 1e10 : 0;     // scale to tokens
        uint256 byRec = r.recoupedUSD18 / 1e12;                    // 1e18 USD → 1e6 scaler
        uint256 raw = byPoi + byRec;
        uint256 amount = raw > maxWeekly ? maxWeekly : raw;

        // split: 55/25/10/10 (last 10% assumed vesting/DAO-managed)
        token.mint(innovators, (amount * 55) / 100);
        token.mint(treasury,   (amount * 25) / 100);
        token.mint(sustain,    (amount * 10) / 100);

        lastMintWeek = _week();
        emit Minted(lastMintWeek, amount, score, r.recoupedUSD18);
    }
}