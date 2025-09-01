// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
interface IRecoveryOracle {
    struct Feed { uint256 timestamp; uint256 recoupedUSD18; bytes32 previousHash; bytes signature; }
    function latest() external view returns (Feed memory);
}