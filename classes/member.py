from brain import Brain
from helper import *
import configuration, pygame

class Member:

	radius = configuration.MEMBER_RADIUS

	def __init__( self ):
		self.x, self.y = Helper.random_coordinates( self.radius )
		self.color     = Helper.random_color()
		self.brain     = Brain()

		self.alive     = True
		self.rotation  = 0.0

	def update( self ):
		self.update_position()
		self.update_state()

	def update_position( self ):
		pass

	def update_state( self ):
		pass

	def draw( self, display ):
		pass