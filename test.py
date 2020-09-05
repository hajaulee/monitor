from hajau import Experiment


class Model(object):

	def __init__(self):
		self.lr = 0

	def show(self, c):
		print('Model said:', c)



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
	test.log('Now is: ' + str(time.time()))
	test.metric('acc', min(i, 90) + random.randint(0, 10))
	test.metric('loss', max(0, 1 - 0.01 * i) + random.random())
	time.sleep(3)
	print('Epoch {}, lr: {}'.format(i, model.lr))
	i+=1
print("Exit loop")    
test.close()
