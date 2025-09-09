// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../contracts/TekTokMonetaryPolicy.sol";
import "../contracts/TekTok.sol";
import "../contracts/mocks/MockDetCadetOracle.sol";
import "../contracts/mocks/MockRecoveryOracle.sol";

/**
 * @title TekTokMonetaryPolicyTest
 * @dev Unit tests for TekTokMonetaryPolicy contract
 */
contract TekTokMonetaryPolicyTest is Test {
    TekTokMonetaryPolicy policy;
    TekTok token;
    MockDetCadetOracle detOracle;
    MockRecoveryOracle recoveryOracle;
    
    address admin = address(0x1);
    address innovators = address(0x2);
    address treasury = address(0x3);
    address sustain = address(0x4);
    
    function setUp() public {
        vm.startPrank(admin);
        
        // Deploy token
        token = new TekTok();
        
        // Deploy oracles
        detOracle = new MockDetCadetOracle();
        recoveryOracle = new MockRecoveryOracle();
        
        // Deploy monetary policy
        policy = new TekTokMonetaryPolicy(token, detOracle, recoveryOracle);
        
        // Grant minter role to policy
        token.grantRole(token.MINTER_ROLE(), address(policy));
        
        vm.stopPrank();
    }
    
    function testInitialState() public {
        assertEq(address(policy.token()), address(token));
        assertEq(address(policy.poi()), address(detOracle));
        assertEq(address(policy.recovery()), address(recoveryOracle));
        assertEq(policy.maxWeeklyBps(), 20);
        assertEq(policy.lastMintWeek(), 0);
    }
    
    function testPositiveScoreFlow() public {
        // Set positive DET/CADET score
        int256 positiveScore = 1e15; // Large positive score
        detOracle.setScore(positiveScore);
        
        // Set recovery amount
        uint256 recoveryUSD18 = 1000 * 1e18; // 1000 USD
        recoveryOracle.setRecoupedUSD18(recoveryUSD18);
        
        // Fast forward one week
        vm.warp(block.timestamp + 1 weeks);
        
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        // Check that tokens were minted
        uint256 totalMinted = token.totalSupply();
        assertGt(totalMinted, 0);
        
        // Check distribution (55/25/10)
        uint256 innovatorsBalance = token.balanceOf(innovators);
        uint256 treasuryBalance = token.balanceOf(treasury);
        uint256 sustainBalance = token.balanceOf(sustain);
        
        assertGt(innovatorsBalance, 0);
        assertGt(treasuryBalance, 0);
        assertGt(sustainBalance, 0);
        
        // Verify distribution ratios
        assertEq(innovatorsBalance, (totalMinted * 55) / 100);
        assertEq(treasuryBalance, (totalMinted * 25) / 100);
        assertEq(sustainBalance, (totalMinted * 10) / 100);
    }
    
    function testNegativeScoreFlow() public {
        // Set negative DET/CADET score
        int256 negativeScore = -1e15;
        detOracle.setScore(negativeScore);
        
        // Set recovery amount
        uint256 recoveryUSD18 = 500 * 1e18; // 500 USD
        recoveryOracle.setRecoupedUSD18(recoveryUSD18);
        
        // Fast forward one week
        vm.warp(block.timestamp + 1 weeks);
        
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        // Check that tokens were still minted from recovery only
        uint256 totalMinted = token.totalSupply();
        assertGt(totalMinted, 0);
        
        // Should be based only on recovery amount (500 USD / 1e12 = 500000 tokens)
        uint256 expectedFromRecovery = recoveryUSD18 / 1e12;
        assertEq(totalMinted, expectedFromRecovery);
    }
    
    function testRecoveryFlow() public {
        // Set zero DET score but positive recovery
        detOracle.setScore(0);
        
        uint256 recoveryUSD18 = 2000 * 1e18; // 2000 USD recovered
        recoveryOracle.setRecoupedUSD18(recoveryUSD18);
        
        // Fast forward one week
        vm.warp(block.timestamp + 1 weeks);
        
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        uint256 totalMinted = token.totalSupply();
        uint256 expectedFromRecovery = recoveryUSD18 / 1e12; // 2M tokens
        
        assertEq(totalMinted, expectedFromRecovery);
    }
    
    function testCooldownPrevention() public {
        // Set positive score
        detOracle.setScore(1e15);
        recoveryOracle.setRecoupedUSD18(1000 * 1e18);
        
        // First mint
        vm.warp(block.timestamp + 1 weeks);
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        uint256 firstMint = token.totalSupply();
        assertGt(firstMint, 0);
        
        // Try to mint again in same week - should fail
        vm.prank(admin);
        vm.expectRevert("cooldown");
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        // Fast forward another week - should succeed
        vm.warp(block.timestamp + 1 weeks);
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        assertGt(token.totalSupply(), firstMint);
    }
    
    function testWeeklyCapEnforcement() public {
        // Set very high scores to test cap
        detOracle.setScore(1e20); // Very large score
        recoveryOracle.setRecoupedUSD18(1e25); // Very large recovery
        
        vm.warp(block.timestamp + 1 weeks);
        
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        uint256 totalSupply = token.totalSupply();
        uint256 cap = totalSupply + 1e24; // From contract logic
        uint256 maxWeekly = cap * 20 / 10000; // 0.20% cap
        
        // Total minted should not exceed weekly cap
        assertLe(totalSupply, maxWeekly);
    }
    
    function testEmittedEvents() public {
        detOracle.setScore(1e15);
        recoveryOracle.setRecoupedUSD18(1000 * 1e18);
        
        vm.warp(block.timestamp + 1 weeks);
        
        vm.expectEmit(true, true, true, true);
        // We need to calculate expected values for the event
        uint256 currentWeek = block.timestamp / 1 weeks;
        
        vm.prank(admin);
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
    }
    
    function testAccessControl() public {
        // Non-admin should not be able to mint
        vm.prank(innovators);
        vm.expectRevert();
        policy.mintAccordingToFeeds(innovators, treasury, sustain);
        
        // Non-admin should not be able to set oracles
        vm.prank(innovators);
        vm.expectRevert();
        policy.setOracles(detOracle, recoveryOracle);
    }
}