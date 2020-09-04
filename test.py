from hajau import Experiment


class Model(object):

	def __init__(self):
		self.lr = 0

test = Experiment('Exp_name_3')
test.param('newa', dict({'c': 1, 'd': 6}))
test.param('newb', dict({'c': 1, 'd': 6}))
test.param('newc', dict({'c': 1, 'd': 6}))


model = Model()

test.debug(model=model)

import time
import random
i = 0
while True:
	test.log('Hello' + str(time.time()))
	test.metric('acc', i + random.randint(0, 10))
	test.metric('loss', 1 - 0.01 * i + random.random())
	time.sleep(3)
	print(i, 'cc', model.lr)
	i+=1
print("Exit loop")    
test.close()
