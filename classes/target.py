from helper import *
import configuration, pygame

class Target:
	radius = configuration.TARGET_RADIUS
	color  = [100,200,100]

	def __init__( self ):
		self.x, self.y = Helper.random_coordinates( self.radius )

	def update( self ):
		pass

	def draw( self, display ):

		fixed_x = Helper.to_fixed( self.x )
		fixed_y = Helper.to_fixed( self.y )

		pygame.draw.circle( display, self.color, (fixed_x, fixed_y), self.radius, 0)
		pygame.draw.circle( display, [0,0,0], (fixed_x, fixed_y), self.radius, 1)