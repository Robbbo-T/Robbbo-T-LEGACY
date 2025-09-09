// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
contract TekCred is ERC721Enumerable, AccessControl {
    bytes32 public constant ISSUER_ROLE = keccak256("ISSUER_ROLE");
    constructor() ERC721("TekCred", "TKCRED") { _grantRole(DEFAULT_ADMIN_ROLE, msg.sender); }
    function issue(address to, uint256 id) external onlyRole(ISSUER_ROLE) { _safeMint(to, id); }
    function _beforeTokenTransfer(address from, address to, uint256, uint256) internal view override {
        require(from == address(0) || to == address(0), "SBT non-transferable");
    }
}