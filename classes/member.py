from brain import Brain
from helper import *
import configuration, pygame

class Member:

	radius     = configuration.MEMBER_RADIUS
	max_energy = configuration.DEFAULT_ENERGY

	def __init__( self ):
		self.x, self.y   = Helper.random_coordinates( self.radius )
		self.color       = Helper.random_color()
		self.brain       = Brain()

		self.alive       = True
		self.rotation    = 0.0
		self.speed       = 0.0
		self.left_track  = 0.0
		self.right_track = 0.0

		self.distance    = 0.0
		self.angle       = 0.0
		self.energy      = self.max_energy
		self.object_type = 0

	def update( self ):
		self.update_state()
		self.update_position()

	def get_params( self ):
		return [self.distance, self.angle, self.object_type, self.energy]

	def update_state( self ):
		self.left_track, self.right_track = self.brain.activate(self.get_params())
		pass

	def update_position( self ):
		pass


	def draw( self, display ):

		fixed_x  = Helper.to_fixed( self.x )
		fixed_y  = Helper.to_fixed( self.y )

		fixed_dx = Helper.to_fixed(self.x + Helper.delta_x(self.rotation, self.radius))
		fixed_dy = Helper.to_fixed(self.y + Helper.delta_y(self.rotation, self.radius))

		pygame.draw.circle( display, self.color, (fixed_x, fixed_y), self.radius, 0)
		pygame.draw.circle( display, [0,0,0], (fixed_x, fixed_y), self.radius, 1)
		pygame.draw.aaline( display, [0,0,0], (fixed_x, fixed_y), (fixed_dx, fixed_dy), 1)