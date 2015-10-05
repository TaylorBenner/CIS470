from brain import Brain
from helper import *
import configuration, pygame

class Member:

	radius = configuration.MEMBER_RADIUS

	def __init__( self ):
		self.x, self.y   = Helper.random_coordinates( self.radius )
		self.color       = Helper.random_color()
		self.brain       = Brain()

		self.alive       = True
		self.rotation    = 0.0
		self.speed       = 0.0
		self.left_track  = 0.0
		self.right_track = 0.0

	def update( self ):
		self.update_state()
		self.update_position()

	def update_position( self ):
		pass

	def update_state( self ):
		pass

	def draw( self, display ):
		pass