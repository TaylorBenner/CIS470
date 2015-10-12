import config, random, math


class Main:
	def __init__( self ):
		pass


class Environment:
	def __init__( self ):


class Member:
	def __init__( self ):
		self.radius = config.member_radius
		self.x = None
		self.y = None


class Target:
	def __init__( self ):
		self.radius = config.target_radius
		self.x = None
		self.y = None


class Brain:
	def __init__( self ):
		pass

class Database:
	def __init__( self ):
		pass


class Helper:
	
	@staticmethod
	def fixed(a): 		return int(round(a))

	@staticmethod
	def delta_x(a,b): 	return math.sin(a) * b

	@staticmethod
	def delta_y(a,b): 	return math.cos(a) * b

	@staticmethod
	def random_color(): return [ random.randint(config.color_min, config.color_max) for i in range(3) ]

	@staticmethod
	def collided(a,b): 	return Helper.slope([a.x,a.y],[b.x,b.y]) < (a.radius + b.radius)

	@staticmethod
	def track_differential(a,b,c): return ((a - b) / c)

	@staticmethod
	def track_speed(a,b): return a + b

	@staticmethod
	def slope(a,b):
		dx = a[0] - b[0]
		dy = a[1] - b[1]
		return math.fabs(math.hypot(dx,dy))

	@staticmethod
	def relation(a,b):
		dx = a[0] - b[0]
		dy = a[1] - b[1]
		return math.atan2(dx,dy)

	@staticmethod
	def nonintersecting_coordinates(radius,objects):
		x,y = [
			random.randint(radius,config.viewport_width-radius), 
			random.randint(radius,config.viewport_height-radius)
		]
		for obj in objects:
			if Helper.slope([x,y],[obj.x,obj.y]) < (radius + obj.radius):
				Helper.nonintersecting_coordinates(radius, objects)
		return [x,y]


env = Environment()