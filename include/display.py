from threading import Thread
from threading import Condition
from threading import Lock
from time import sleep
import sys, traceback

class Display(Thread):
	def __init__(self):
		Thread.__init__(self)
		self._commands = {}
		self._switch = False

	def show_options(self):
		
		print "> please select the options below:"
		for key,(des, func, args) in self._commands.iteritems():
			string = "[{0}] {1}".format(key,des)
			print string
		print ""


	def reg_commands(self, key, des, func, args):
		self._commands[key] = (des, func, args)

		#print key+des


	def run(self):
		try:
			#show_options()
			self._switch = True
			while(self._switch):
				self.show_options()
				command = raw_input("> ")
				if(self._commands.has_key(command) == False):
					print "> Wrong input, please input again\n"
					continue
				des, func, args = self._commands[command]
				func(args)

		except (Exception) as e:
			print e
			traceback.print_exc(file=sys.stdout)
  

	def stop(self):
		self._switch = False



