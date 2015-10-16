from helper import *
import config, pygame

class Target:
	def __init__( self ):
		self.radius 		= config.target_radius
		self.color  		= config.target_color
		self.energy_amount 	= config.energy_gain_amount
		self.consumed 		= False
		self.x 				= None
		self.y 				= None

	def draw( self, display ):
		c, s = self.color, [0,0,0]
		pygame.draw.circle( display, c, (Helper.fixed(self.x), Helper.fixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, s, (Helper.fixed(self.x), Helper.fixed(self.y)), self.radius, 1)
