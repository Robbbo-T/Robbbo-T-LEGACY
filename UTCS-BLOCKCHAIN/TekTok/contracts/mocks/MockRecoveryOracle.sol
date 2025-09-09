// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../interfaces/IRecoveryOracle.sol";

/**
 * @title MockRecoveryOracle
 * @dev Mock implementation of IRecoveryOracle for testing
 */
contract MockRecoveryOracle is IRecoveryOracle {
    Feed private _currentFeed;
    
    constructor() {
        // Initialize with zero recovery
        _currentFeed = Feed({
            timestamp: block.timestamp,
            recoupedUSD18: 0,
            previousHash: keccak256("genesis"),
            signature: hex"00"
        });
    }
    
    function latest() external view override returns (Feed memory) {
        return _currentFeed;
    }
    
    function setRecoupedUSD18(uint256 _recoupedUSD18) external {
        _currentFeed.recoupedUSD18 = _recoupedUSD18;
        _currentFeed.timestamp = block.timestamp;
        _currentFeed.previousHash = keccak256(abi.encode(_currentFeed.timestamp, _recoupedUSD18));
    }
    
    function setFeed(uint256 _timestamp, uint256 _recoupedUSD18, bytes32 _previousHash, bytes memory _signature) external {
        _currentFeed = Feed({
            timestamp: _timestamp,
            recoupedUSD18: _recoupedUSD18,
            previousHash: _previousHash,
            signature: _signature
        });
    }
}