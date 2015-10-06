from helper import *
import configuration, pygame

class Target:
	#   class members 
	radius          = 5
	amount          = 500

	#   class methods
	def __init__( self, obj_type ): 

		self.x, self.y      = Helper.random_coordinates( radius = (self.radius+1) )
		self.object_type    = obj_type
		self.consumed       = 0

		if self.object_type == "food":
			self.color  = [100,200,100]
			self.object_code = 1

		elif self.object_type == "toxin":
			self.object_code = -1
			self.color = [200,100,100]

	def draw( self, display ):
		c, s = self.color, [0,0,0]
		pygame.draw.circle( display, c, (Helper.to_fixed(self.x), Helper.to_fixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, s, (Helper.to_fixed(self.x), Helper.to_fixed(self.y)), self.radius, 1)