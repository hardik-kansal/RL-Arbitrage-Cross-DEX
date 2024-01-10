from web3 import Web3
from configparser import ConfigParser
import time
import random
import numpy as np
import requests
import apikey


config = ConfigParser()
config.read("config.ini")


# Market Prices of Tokens
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': apikey.apiKey,
}
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'


def getMarketPrice():
    symbol = []
    for i in config['TOKENS']:
        symbol.append(i.upper())
    symbols_formatted=','.join(symbol)
    parameters = {
        'symbol': symbols_formatted,
        'convert': 'USD'
    }
    json = requests.get(url, headers=headers, params=parameters).json()
    json = json['data']
    c=0
    array=[]
    for i in json:
       array.append(json[symbol[c]]['quote']['USD']['price'])
    return array




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


# AT class init
def get_weth(a=0.01,b=0.02):
    value=random.uniform(a,b)
    wethContract = w3.eth.contract(address=wethAddr, abi=wethABI)
    get_weth = wethContract.functions.deposit().build_transaction({
        "from": recipient,
        "nonce": w3.eth.get_transaction_count(recipient),
        "value": w3.to_wei(2, 'ether')
    })
    signed_tx = w3.eth.account.sign_transaction(get_weth, private_key=privateKey)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx = w3.eth.get_transaction(tx_hash)
    print(tx)
def swap(token0,token1,amountIn,fee=3000):
    tx=w3.eth.contract(address=token0, abi=wethABI).functions.approve(routerAddr,amountIn).build_transaction({
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

def getReserves(token0,token1):
    poolAddr=factory.caller().getPool(token0, token1, 3000)
    token0=w3.eth.contract(address=token0,abi=wethABI).caller().balanceOf(poolAddr)
    token1=w3.eth.contract(address=token1,abi=wethABI).caller().balanceOf(poolAddr)
    return token0,token1
def reserves():
    array=[]
    k = (config['TOKENS'].keys())
    c = config['TOKENS']
    count=0
    for i in k:
        array.append(c[i])
        count+=1
    for i in range(0,count):
        for j in range(i + 1, count):
            print(getReserves(array[i], array[j]))


def calculateProfit(gasUsed,marketPrice,tokenAmount):
    tokenPrice=np.multiply(marketPrice,tokenAmount)
    gasUsed=marketPrice[0]*gasUsed
    return tokenPrice-gasUsed



class chainENV:
    def step(self,actions):
        # reward
        # next state
        # done


        pass
    def reset(self):
        # initail state
        pass























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
