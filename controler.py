from core.engine import Engine
from core.apis import APIS
from include.display import Display

import sys, traceback
class Controler(object):
	def __init__(self):
		self._display = Display()
		self._api = APIS()
		
	def start(self):
		try:
			#reg command
			self._display.reg_commands('1',"input one author's name, return author info",self.do_author_info,None)
			self._display.reg_commands('2',"input authors' name, return publications count",self.do_publications,None)
			self._display.reg_commands('3',"start crawler",self.do_crawler,None)
			self._display.reg_commands('q',"exit the program",self.do_quit,None)
			#start display
			self._display.start()
			



		except (Exception) as e:
			print e
			traceback.print_exc(file=sys.stdout)
			
	def do_author_info(self, para):

		while(True):
			print"author info> input author name(enter 'b' to go back):"
			command = raw_input("author info> ")
			if( command == 'b'):
				break
			self._api.print_athor_info(command)

	def do_publications(self, para):
		while(True):
			print"publications> input several authors name, spilted by ','(enter 'b' to go back):"
			command = raw_input("publications> ")
			if( command == 'b'):
				break

			self._api.print_publications(command)

	def do_crawler(self,para):
		print "do_crawler"
		#create crawler engin
		crawler_engine = Engine()
		#start engine 
		crawler_engine.start( )
		#stop engin 
		crawler_engine.stop()

	def do_quit(self, para):
		print "quting..."
		self._display.stop()

	