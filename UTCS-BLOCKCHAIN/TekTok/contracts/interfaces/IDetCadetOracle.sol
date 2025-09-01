// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
interface IDetCadetOracle {
    struct Feed { uint256 timestamp; int256 score; bytes32 previousHash; bytes signature; }
    function latest() external view returns (Feed memory);
}