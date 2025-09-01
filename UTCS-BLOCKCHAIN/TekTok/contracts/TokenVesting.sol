// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "./TekTok.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
contract TokenVesting is Ownable {
    TekTok public immutable token;
    struct Grant { uint64 start; uint64 cliff; uint64 duration; uint256 amount; uint256 released; }
    mapping(address => Grant) public grants;
    constructor(TekTok _token){ token=_token; }
    function addGrant(address b,uint64 s,uint64 c,uint64 d,uint256 a) external onlyOwner { grants[b]=Grant(s,c,d,a,0); }
    function release() external {
        Grant storage g=grants[msg.sender]; require(block.timestamp>=g.cliff,"cliff");
        uint256 vested=_vested(g); uint256 rel=vested-g.released; g.released=vested; token.mint(msg.sender, rel);
    }
    function _vested(Grant memory g) internal view returns(uint256){
        if(block.timestamp<g.cliff)return 0; if(block.timestamp>=g.start+g.duration)return g.amount;
        return (g.amount*(block.timestamp-g.start))/g.duration;
    }
}