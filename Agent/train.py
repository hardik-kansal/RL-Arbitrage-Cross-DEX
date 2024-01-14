from chainENV import ENV
from agent1 import Agent
import numpy as np
from utils import plot_learning_curve
import math



profitThreshold=100
lpTerminalReward=200
wpTerminalReward=-500
ngTerminalReward=-300
stepLimit=10

env=ENV(profitThreshold,lpTerminalReward,wpTerminalReward,ngTerminalReward,stepLimit)


epsilon=0.99
num_episodes=100
gamma=0.99
alpha=0.001
beta=0.002
fc1_dim=128
fc2_dim=256
memory_size=50
batch_size=50
tau=1
update_period=40
warmup=10
name="model1"


def train(env,agent,epsilon,num_episodes):

    pools_dim=env.pools_dim
    episode_lengths=[]
    profit_eachEpisode=[]
    for i in range(0,num_episodes):
        print()
        print(f"#########  Episode No-{i}")
        state=env.reset()
        # print(f"Initial State--{state}")
        step_size=0
        while True:
            actions = agent.choose_action(state)
            r = np.random.rand()
            # print(r)
            if r < epsilon:
                print("Exploration")
                next_action = np.random.choice(np.arange(pools_dim))
            else:
                print("Greedy")
                next_action = np.argmax(actions[0][:pools_dim])
            gas=actions[0][agent.action_dims - 1]
            if math.isnan(gas):
                gas=-1
            action = [next_action, int(gas)]
            print(f"ActionPerformed--- {action}")
            _state,reward,done=env.step(action)
            agent.store_transition(state,actions,reward,_state,done)
            agent.learn()
            if(done):
                profit_eachEpisode.append(env.profit)
                break

            step_size+=1
        episode_lengths.append(step_size)
        if(i%50==0):
            epsilon = epsilon-0.03


    return episode_lengths,profit_eachEpisode


state_dims=env.state_dim
action_dims=env.pools_dim+1

agent=Agent(epsilon, gamma, alpha, beta, state_dims, action_dims, fc1_dim, fc2_dim,
                 memory_size, batch_size, tau, update_period, warmup, name)


episode_lengths,profit_eachEpisode = train(env, agent, epsilon, num_episodes)
plot_learning_curve(episode_lengths,profit_eachEpisode,"LearningPlot1",False)



