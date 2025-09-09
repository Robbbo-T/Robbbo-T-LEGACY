// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "../interfaces/IDetCadetOracle.sol";

/**
 * @title MockDetCadetOracle
 * @dev Mock implementation of IDetCadetOracle for testing
 */
contract MockDetCadetOracle is IDetCadetOracle {
    Feed private _currentFeed;
    
    constructor() {
        // Initialize with neutral values
        _currentFeed = Feed({
            timestamp: block.timestamp,
            score: 0,
            previousHash: keccak256("genesis"),
            signature: hex"00"
        });
    }
    
    function latest() external view override returns (Feed memory) {
        return _currentFeed;
    }
    
    function setScore(int256 _score) external {
        _currentFeed.score = _score;
        _currentFeed.timestamp = block.timestamp;
        _currentFeed.previousHash = keccak256(abi.encode(_currentFeed.timestamp, _score));
    }
    
    function setFeed(uint256 _timestamp, int256 _score, bytes32 _previousHash, bytes memory _signature) external {
        _currentFeed = Feed({
            timestamp: _timestamp,
            score: _score,
            previousHash: _previousHash,
            signature: _signature
        });
    }
}