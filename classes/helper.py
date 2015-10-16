import random, math
import config

class Helper:
	
	@staticmethod
	def fixed(a): return int(round(a))

	@staticmethod
	def delta_x(a,b): return math.sin(a) * b

	@staticmethod
	def delta_y(a,b): return math.cos(a) * b

	@staticmethod
	def random_color(): return [ random.randint(config.color_min, config.color_max) for i in range(3) ]

	@staticmethod
	def is_collided(a,b): return Helper.slope([a.x,a.y],[b.x,b.y]) < (a.radius + b.radius)

	@staticmethod
	def is_close(a,b): return Helper.slope([a.x,a.y],[b.x,b.y]) < (config.member_view_distance)

	@staticmethod
	def get_distance(a,b): return Helper.slope([a.x,a.y],[b.x,b.y])

	@staticmethod
	def get_relation_to(a,b): return Helper.relation([a.x,a.y],[b.x,b.y])

	@staticmethod
	def track_differential(a,b,c): return ((a - b) / c)

	@staticmethod
	def track_speed(a,b): return a + b

	@staticmethod
	def make_uniform(a, b):
		if b == 1:
			if a == 0:
				return 0
			else:
				return (1 - (1 / float(a)))
		elif b == 2:
			if a == 0:
				return 0
			else:
				return (1 / float(a))

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
	def nonintersecting_coordinates(radius,positions):
		x,y = [
			random.randint(radius,config.viewport_width-radius), 
			random.randint(radius,config.viewport_height-radius)
		]
		for pos in positions:
			if Helper.slope([x,y],[pos[0],pos[1]]) < (radius + config.intersection_tolerance):
				Helper.nonintersecting_coordinates(radius, positions)
		return [x,y]


