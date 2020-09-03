import os
import json
import time
import datetime
import pyrebase
import threading
import traceback

config = {
  "apiKey": "AIzaSyBvSo1GFKS_XN6LYKC2QDkfm8o8UK2iJhE",
  "authDomain": "",
  "databaseURL": "https://dl-monitor.firebaseio.com/",
  "storageBucket": "",
  "serviceAccount": ""
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def async_task(func):    
    def throws(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            
    def wrapped(*args, **kwargs):
        t = threading.Thread(target=throws, args=args, kwargs=kwargs)
        t.start()
    return wrapped

class Experiment(object):

	"""docstring for Experiment"""

	def __init__(self, name, capture_log=False, clear_old=True, **kwargs):
		super(Experiment, self).__init__()

		self.__dict__ = kwargs

		api_path = os.path.expanduser('~/.remote_log.api')
		with open(api_path) as file:
			self.user_api = file.read().strip()

		self.name = name
		self.exp_path = "experiments/{}/{}".format(self.user_api, self.name)
		self.clear(clear_old)
		self.checkin()
		self.ping()
		self.listen()

	@async_task
	def checkin(self):
		db.child(self.exp_path).child('start_time').set(datetime.datetime.now().isoformat())


	def clear(self, clear_old):
		if clear_old:
			db.child(self.exp_path).remove()


	def ping(self):
		def set_latest_time():
			t = threading.currentThread()
			while getattr(t, "do_run", True):
				db.child(self.exp_path).child('latest_time').set(datetime.datetime.now().isoformat())
				time.sleep(10)
		self.th = threading.Thread(target=set_latest_time)
		self.th.start()

	@async_task
	def metric(self, met, mss):
		db.child(self.exp_path).child('metric').child(met).push(float(mss))

	@async_task
	def param(self, par, mss):
		db.child(self.exp_path).child('param').child(par).set(json.dumps(mss))

	@async_task
	def log(self, mss):
		log_time = datetime.datetime.now().isoformat().split('.')[0]
		db.child(self.exp_path).child('logs').push(log_time + ': ' + mss)

	@async_task
	def listen(self):
		db.child(self.exp_path).child('command').stream(self.command)

	@async_task
	def command(self, message):
		mss = message['data']
		path = message['path']
		print(message['event'], mss, path)
		
		if mss is not None:
			db.child(self.exp_path).child('command' + path).remove()
			try:
				if mss[0] != '!':
					db.child(self.exp_path).child('results').push('>>> ' + mss + '\n' + str(eval(mss)))
				else:
					cml = '\n$:{}\n'.format(mss)
					stdout = os.popen(mss[1:]).read()
					db.child(self.exp_path).child('results').push(cml + stdout)
			except Exception:
				db.child(self.exp_path).child('results').push(str(traceback.format_exc()))


	def capture_log(self):
		# TODO
		pass

	def closs(self):
		self.th.do_run = False
