
# Reinforcemnt Learning Based Cross--DEX Arbitrage Agent

Under Development - Model is not trained yet.
Use conda for python installation
Use Py-charm for IDE for python




## Installation

Run these commands on Terminal

```bash
git clone git@github.com:hardik-kansal/RL-Arbitrage-Cross-DEX.git
cd RL-Arbitrage-Cross-DEX
cd chainENV 
yarn install
```
Get `COINMARKETCAP API-KEY` from `https://coinmarketcap.com/api/` \
Get `ALCHEMY API-KEY` from `https://coinmarketcap.com/api/`

Run hardhat Mainnet Fork
```bash
 yarn hardhat node --fork https://eth-mainnet.g.alchemy.com/v2/[ALCHEMY API-KEY]
```
Copy any account and private-Key and paste under [ACCOUNT] at Agent/config.ini

you can add any no of tokens (currently from uniswap only) in given format

ETH=[decimal][ethereum-address]




## Training

Go to train.py and change following hyperparamters
epsilon=0.99
num_episodes=100
gamma=0.99
alpha=0.001
beta=0.002
fc1_dim=256
fc2_dim=256
memory_size=50
batch_size=50
tau=1
update_period=40
warmup=10
name="model1"

To start training, run train.py

## Reward 

To change reward for the agent go to Agent/chainENV.py and change step function