import random, math
import configuration

class Helper:

	@staticmethod
	def random_coordinates( radius = 0 ):
		x = random.randint(radius, configuration.WIDTH - radius)
		y = random.randint(radius, configuration.HEIGHT - radius)
		return [x,y]

	@staticmethod
	def random_color():
		return [ random.randint(0,255) for i in range(3) ]

	@staticmethod
	def to_fixed( number ):
		return int(math.floor(number))

	@staticmethod
	def delta_x( angle, number ):
		return math.sin(angle) * number

	@staticmethod
	def delta_y( angle, number ):
		return math.cos(angle) * number