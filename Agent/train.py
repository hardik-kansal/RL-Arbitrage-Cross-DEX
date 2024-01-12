from chainENV import ENV
from agent1 import Agent
import numpy as np
import matplotlib.pyplot as plt


profitThreshold=10
lpTerminalReward=0
wpTerminalReward=-10
ngTerminalReward=5
stepLimit=10

env=ENV(profitThreshold,lpTerminalReward,wpTerminalReward,ngTerminalReward,stepLimit)


epsilon=0.2
num_episodes=1000
gamma=0.99
alpha=0.001
beta=0.002
fc1_dim=100
fc2_dim=100
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
        actions=agent.choose_action(state)
        if np.random.rand() < epsilon:
            print("Exploration")
            next_action = np.random.choice(np.arange(pools_dim))
        else:
            print("Greedy")
            next_action = np.argmax(actions[0][:pools_dim])
        action=[next_action,int(actions[0][agent.action_dims-1])]
        print(f"ActionPerformed--- {action}")
        step_size=0
        while True:
            _state,reward,done=env.step(action)
            agent.store_transition(state,actions,reward,_state,done)
            agent.learn()
            if(done):
                profit_eachEpisode.append(env.profit)
                break

            step_size+=1
        episode_lengths.append(step_size)
        # epsilon=epsilon/1.1

    return episode_lengths,profit_eachEpisode


state_dims=env.state_dim
action_dims=env.pools_dim+1

agent=Agent(epsilon, gamma, alpha, beta, state_dims, action_dims, fc1_dim, fc2_dim,
                 memory_size, batch_size, tau, update_period, warmup, name)


episode_lengths,profit_eachEpisode = train(env, agent, epsilon, num_episodes)

# Plotting the episode lengths
plt.plot(episode_lengths, label='Episode Lengths', color='blue')
plt.plot(profit_eachEpisode, label='Profits Each Episode', color='orange')
plt.xlabel('Episode')
plt.ylabel('Values')
plt.title('Episode Lengths and Profit_eachEpsiode')
plt.legend()
plt.show()


