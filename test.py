from message import Experiment


test = Experiment('Exp_name_3')
test.param('newa', dict({'c': 1, 'd': 6}))
test.param('newb', dict({'c': 1, 'd': 6}))
test.param('newc', dict({'c': 1, 'd': 6}))

# for i in range(100):
# 	test.metric('acc', i)


# for i in range(100):
# 	test.metric('loss', (100 - i) / 100)


import time
import random
i = 0
while True:
	test.log('Hello' + str(time.time()))
	test.metric('acc', i + random.randint(0, 10))
	test.metric('loss', 1 - 0.01 * i)
	time.sleep(3)
	print(i, 'cc')
	i+=1
print("Exit loop")    
test.close()