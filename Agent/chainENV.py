from web3 import Web3
from configparser import ConfigParser
import time
import random
import numpy as np
import requests
import apikey
from math import comb


config = ConfigParser()
config.read("config.ini")


# Market Prices of Tokens
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey.apiKey,
}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


routerAddr=config['UNISWAP']['address']
routerABI=config['UNISWAP']['abi']
wethAddr=config['WETH9']['address']
wethABI=config['WETH9']['abi']
factoryAddr=config['FACTORY']['address']
factoryABI=config['FACTORY']['abi']
reservesAddr=config['RESERVES']['address']
reservesABI=config['RESERVES']['abi']
recipient=config['Account']['address']
privateKey=config['Account']['key']


w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
swapContract=w3.eth.contract(address=routerAddr,abi=routerABI)
factory=w3.eth.contract(address=factoryAddr,abi=factoryABI)


def calculateProfit(gasUsed,marketPrice,tokenAmount):
    tokenPrice=np.multiply(marketPrice,tokenAmount)
    gasUsed=marketPrice[0]*gasUsed
    return tokenPrice-gasUsed




class chainENV:
    def __init__(self):
        self.pools_dim=self.getNoOfPools()
        self.action_dim=2
        self.state_dim=self.getStateDim()
        self.array,self.count=self.getToken()
        self.state_space=np.zeroes(self.state_dim)
        self.action_space=np.zeroes(self.action_dim)
        self.pool_addr=self.getPoolAddr()


    def getTokenID(self,poolIndex):
        pass
        #
        # p=0
        # for i in range(0,tokenIndex):
        #     p+=self.count-i-1
        #
        # if(poolIndex<self.count-1 and poolIndex>=p):
        #     return tokenIndex,False
        # else:
        #     return tokenIndex,True
    def getTokenSwapIndex(self):
        condn = self.state_space[:self.count] != 0
        tokenIndex=np.where(condn)[0][0]
        return tokenIndex
    def step(self,actions):
        poolIndex=actions[0]
        gasPredicted=actions[1]
        pooladdr=self.pool_addr[poolIndex]
        token0,token1,done=self.getTokenID(poolIndex)
        if(done):
            pass
        self.swap(token0,token1,self.state_space[self.getTokenSwapIndex()],3000)
        # check profit by gasUsed and if else Profit
        # reward=
        _state=self.getStateSpace()
        pass
    def getStateSpace(self):
        reserves=self.reserves()
        pass


    def reset(self):
        # get_state_initial
        pass
    def get_weth(a=0.01, b=0.02):
        value = random.uniform(a, b)
        wethContract = w3.eth.contract(address=wethAddr, abi=wethABI)
        get_weth = wethContract.functions.deposit().build_transaction({
            "from": recipient,
            "nonce": w3.eth.get_transaction_count(recipient),
            "value": w3.to_wei(value, 'ether')
        })
        signed_tx = w3.eth.account.sign_transaction(get_weth, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx = w3.eth.get_transaction(tx_hash)
        print(tx)
    def getMarketPrice(self):
        symbol = []
        for i in config['TOKENS']:
            symbol.append(i.upper())
        symbols_formatted = ','.join(symbol)
        parameters = {
            'symbol': symbols_formatted,
            'convert': 'USD'
        }
        json = requests.get(url, headers=headers, params=parameters).json()
        json = json['data']
        c = 0
        array = []
        for i in json:
            array.append(json[symbol[c]]['quote']['USD']['price'])
        return array
    def getNoOfPools(self):
        k = (config['TOKENS'].keys())
        count = 0
        for i in k:
            count += 1
        return comb(count, 2)
    def getStateDim(self):
       k = (config['TOKENS'].keys())
       p = self.pools_dim*2
       return k + p + 1
    def getToken(self):
        array = []
        k = (config['TOKENS'].keys())
        c = config['TOKENS']
        count = 0
        for i in k:
            array.append(c[i])
            count += 1
        return array, count
    def getReserves(self,token0, token1,poolAddr):

        token0 = w3.eth.contract(address=token0, abi=wethABI).caller().balanceOf(poolAddr)
        token1 = w3.eth.contract(address=token1, abi=wethABI).caller().balanceOf(poolAddr)
        return token0, token1
    def reserves(self):
        count=self.count
        array=self.array
        for i in range(0, count):
            for j in range(i + 1, count):
                print(self.getReserves(array[i], array[j]))
    def getPoolAddr(self):
        array = self.array
        array1=[]
        for i in range(0, self.count):
            for j in range(i + 1, self.count):
                poolAddr = factory.caller().getPool(array[i], array[j], 3000)
                array1.append(poolAddr)
        return array1
    def swap(self, token0, token1, amountIn, fee=3000):
        tx = w3.eth.contract(address=token0, abi=wethABI).functions.approve(routerAddr, amountIn).build_transaction({
            "from": recipient,
            "nonce": w3.eth.get_transaction_count(recipient)
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(tx_hash)
        swapTx = swapContract.functions.exactInputSingle(
            (token0, token1, fee, recipient, int(time.time()) + 60, amountIn, 0, 0)).build_transaction({
            "from": recipient,
            "nonce": w3.eth.get_transaction_count(recipient)
        })
        signed_tx = w3.eth.account.sign_transaction(swapTx, private_key=privateKey)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx = w3.eth.get_transaction(tx_hash)
        print(tx)












# swap(token1,token0,10000000000)
# usdc=w3.eth.contract(address=token0,abi=wethABI).caller().balanceOf(recipient)
# print(usdc)

# print(w3.eth.get_block_transaction_count(w3.eth.get_block_number()))
# print("Block no---")
# print(w3.eth.get_block_number())
# print("Getting weth--")
# get_weth()
# print("blockno after weth--")
# print(w3.eth.get_block_transaction_count(w3.eth.get_block_number()))
#
# reserves()
# # print("Swap tx-")
# swap(token1,token0,100000000000000)
# print("blockno after swap--")
# print(w3.eth.get_block_transaction_count(w3.eth.get_block_number()))
# reserves()
# c=w3.eth.contract(address=token0,abi=wethABI).caller().balanceOf(recipient)
# # print(c)
# array=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","0xdAC17F958D2ee523a2206206994597C13D831ec7","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0x6B175474E89094C44Da98b954EedeAC495271d0F","0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"]
# weth
# token1="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
# # usdc
# token0="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
