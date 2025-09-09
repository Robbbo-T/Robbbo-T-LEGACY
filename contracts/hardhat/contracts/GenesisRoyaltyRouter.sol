// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

interface IERC20Like {
    function balanceOf(address) external view returns (uint256);
    function allowance(address,address) external view returns (uint256);
    function transferFrom(address,address,uint256) external returns (bool);
}

contract GenesisRoyaltyRouter is AccessControl {
    using SafeERC20 for IERC20Like;

    bytes32 public constant SPLIT_ADMIN = keccak256("SPLIT_ADMIN");

    struct Split { address to; uint96 share; } // share in ppm (parts per million)
    // oegiId => splits
    mapping(bytes32 => Split[]) public splits;
    // sum check
    mapping(bytes32 => uint96) public splitSum;

    event SplitsSet(bytes32 indexed oegiId, Split[] splits, uint96 sumPpm);
    event Distributed(bytes32 indexed oegiId, address token, uint256 amount);

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(SPLIT_ADMIN, admin);
    }

    function setSplits(bytes32 oegiId, Split[] calldata newSplits)
        external onlyRole(SPLIT_ADMIN)
    {
        delete splits[oegiId];
        uint96 sum;
        for (uint i=0; i<newSplits.length; i++) {
            splits[oegiId].push(newSplits[i]);
            sum += newSplits[i].share;
        }
        require(sum == 1_000_000, "sum!=100%");
        splitSum[oegiId] = sum;
        emit SplitsSet(oegiId, newSplits, sum);
    }

    function distribute(bytes32 oegiId, address erc20, uint256 amount) external {
        require(splitSum[oegiId] == 1_000_000, "splits not set");
        IERC20Like token = IERC20Like(erc20);
        require(token.allowance(msg.sender, address(this)) >= amount, "allowance");
        require(token.transferFrom(msg.sender, address(this), amount), "xfer in");
        // push out
        for (uint i=0; i<splits[oegiId].length; i++) {
            uint256 part = (amount * splits[oegiId][i].share) / 1_000_000;
            require(token.transferFrom(address(this), splits[oegiId][i].to, part), "xfer out");
        }
        emit Distributed(oegiId, erc20, amount);
    }
}