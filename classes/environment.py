from member import Member
from target import Target
from helper import *
import configuration

class Environment:
	def __init__( self ):
		self.members = [ Member() for i in range(configuration.POPULATION_SIZE) ]
		self.targets = [ Target() for i in range(configuration.TARGET_COUNT) ]

	def get_objects( self ):
		return self.members + self.targets