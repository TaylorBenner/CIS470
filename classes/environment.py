from member import Member
from target import Target
from helper import *
import configuration

class Environment:
	def __init__( self ):
		self.members = [ Member() for i in range(configuration.POPULATION_SIZE) ]
		self.food    = [ Target("food") for i in range(configuration.TARGET_COUNT) ]

	def get_objects( self ):
		return self.members + self.food

	def get_targets( self ):
		return self.food

	def update_targets( self ):

		for obj in self.get_targets():
			if obj.consumed == 1:

				if obj.object_code == 1:
					self.food.remove( obj )
					self.new_food()

				elif obj.object_code == -1:
					self.toxins.remove( obj )
					self.new_toxin()