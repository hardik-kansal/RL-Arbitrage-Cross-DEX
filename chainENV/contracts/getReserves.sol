// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;
import "../goerli/0x1F98431c8aD98523631AE4a59f267346ea31F984/contracts/interfaces/IUniswapV3Factory.sol";
import "./IERC20.sol";
contract tokenReserves {
address[] private Tokens=[0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2,0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48,0xdAC17F958D2ee523a2206206994597C13D831ec7,0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599,0x6B175474E89094C44Da98b954EedeAC495271d0F,0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2];

address public constant factory=0x1F98431c8aD98523631AE4a59f267346ea31F984;
IUniswapV3Factory factoryContract=IUniswapV3Factory(factory);

function getReserves() external view returns (uint256[][] memory reserves) {
        reserves = new uint256[][](15);
        uint c = 0;

        for (uint i = 0; i < 6; i++) {
            address token0 = Tokens[i];
            IERC20 tokenContract1 = IERC20(token0);
            
            for (uint j = i+1; j < 6; j++) {
                address token1 = Tokens[j];
                address poolAddr = factoryContract.getPool(token0, token1, 3000);
                IERC20 tokenContract2 = IERC20(token1);

                uint256 balance1 = tokenContract1.balanceOf(poolAddr);
                uint256 balance2 = tokenContract2.balanceOf(poolAddr);
                uint256[] memory tempArray = new uint256[](2);
                tempArray[0] = balance1;
                tempArray[1] = balance2;
                reserves[c] = tempArray;
                c++;
            }
        }
    }
}


