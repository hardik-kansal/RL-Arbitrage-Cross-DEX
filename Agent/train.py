from chainENV import ENV
env=ENV(100,0,-1000)
print(env.maGas)
print(env.reset())
print(env.step([0,env.maGas]))

