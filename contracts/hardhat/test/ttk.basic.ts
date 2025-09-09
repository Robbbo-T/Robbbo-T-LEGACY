import { expect } from "chai";
import { ethers } from "hardhat";

describe("TTKToken", function () {
  it("deploys and mints", async function () {
    const [admin, user] = await ethers.getSigners();
    const TTK = await ethers.getContractFactory("TTKToken");
    const token = await TTK.connect(admin).deploy(admin.address);
    await token.waitForDeployment();
    await token.connect(admin).mint(user.address, ethers.parseEther("10"));
    expect(await token.balanceOf(user.address)).to.equal(ethers.parseEther("10"));
  });
});