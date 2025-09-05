// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/AccessControl.sol";

contract DetEventAnchor is AccessControl {
    bytes32 public constant ANCHOR_ROLE = keccak256("ANCHOR_ROLE");

    event DetAnchored(bytes32 indexed hash, string eventType, string ref, uint256 ts);

    constructor(address admin) {
        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(ANCHOR_ROLE, admin);
    }

    function anchor(bytes32 detHash, string calldata eventType, string calldata ref) external {
        require(hasRole(ANCHOR_ROLE, msg.sender), "not allowed");
        emit DetAnchored(detHash, eventType, ref, block.timestamp);
    }
}