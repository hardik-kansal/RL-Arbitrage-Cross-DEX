from web3 import Web3
from configparser import ConfigParser
import time
import random
config = ConfigParser()
config.read("config.ini")
array=["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","0xdAC17F958D2ee523a2206206994597C13D831ec7","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0x6B175474E89094C44Da98b954EedeAC495271d0F","0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2"]

routerAddr=config['UNISWAP']['address']
routerABI=config['UNISWAP']['abi']
wethAddr=config['WETH9']['address']
wethABI=config['WETH9']['abi']
factoryAddr=config['FACTORY']['address']
factoryABI=config['FACTORY']['abi']
reservesAddr=config['RESERVES']['address']
reservesABI=config['RESERVES']['abi']

# weth
token1="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
# usdc
token0="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"


recipient="0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
privateKey=0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
swapContract=w3.eth.contract(address=routerAddr,abi=routerABI)
factory=w3.eth.contract(address=factoryAddr,abi=factoryABI)

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
    print("swap hash: ",tx_hash)

def getReserves(token0,token1):
    poolAddr=factory.caller().getPool(token0, token1, 3000)
    token0=w3.eth.contract(address=token0,abi=wethABI).caller().balanceOf(poolAddr)
    token1=w3.eth.contract(address=token1,abi=wethABI).caller().balanceOf(poolAddr)
    return token0,token1
def reserves():
    for i in range(0, 6):
        for j in range(i + 1, 6):
            print(getReserves(array[i], array[j]))

# get_weth()
reserves()
# swap(token1,token0,1000)
# reserves()
# c=w3.eth.contract(address=token0,abi=wethABI).caller().balanceOf(recipient)
# print(c)

