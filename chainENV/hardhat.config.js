require("@nomicfoundation/hardhat-toolbox");
require('dotenv').config();
/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.19",
  networks: {
    hardhat: {
      chainId:1337,
      forking: {
        url: "https://eth-mainnet.g.alchemy.com/v2/MkbgG8QqySzFWGpWGXKPQft3lUYDmmz3",
        blockNumber: 18961474
      }
    }
  }
};
