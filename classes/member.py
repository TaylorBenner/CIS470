from brain import Brain
from helper import *
import configuration, pygame, numpy

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

		self.distance_to   = 0.0
		self.relation_to   = 0.0
		self.forward_angle = 30
		self.energy        = self.max_energy
		self.object_type   = 0

		self.close_to      = None

	def update( self, targets ):
		self.update_state()
		self.update_position()
		self.check_collisions( targets )

	def get_params( self ):
		return [self.distance_to, self.relation_to, self.object_type, self.energy]

	def update_state( self ):
		self.left_track, self.right_track = self.brain.activate(self.get_params())
		self.speed = self.left_track + self.right_track
		self.rotation += (self.left_track - self.right_track) / self.radius
		if self.rotation > math.pi *2 : self.rotation = 0
		elif self.rotation < 0: self.rotation = math.pi * 2

	def update_position( self ):

		move_x_del = Helper.delta_x( self.rotation, self.speed )
		move_y_del = Helper.delta_y( self.rotation, self.speed )

		dx = (self.x + move_x_del)
		dy = (self.y + move_y_del) 

		if dx < 0: self.x = configuration.WIDTH
		elif dx > configuration.WIDTH: self.x = 0
		else: self.x = dx

		if dy < 0: self.y = configuration.HEIGHT
		elif dy > configuration.HEIGHT: self.y = 0
		else: self.y = dy


	def check_collisions( self, targets ):

		closest = None
		distance_to_closest = 0.0
		tolerance = self.radius * 5

		for target in targets:
			if numpy.isclose( [self.x, self.y], [target.x,target.y], atol = tolerance ).all():

				if closest == None:
					closest = target
					distance_to_closest = Helper.get_slope([self.x,self.y],[target.x,target.y])
				else:
					distance_to_tar = Helper.get_slope([self.x,self.y],[target.x,target.y])
					if distance_to_tar < distance_to_closest:
						closest = target
						distance_to_closest = Helper.get_slope([self.x,self.y],[target.x,target.y])

				ax = self.x - target.x
				bx = self.y - target.y
				dx = math.sqrt( ax * ax + bx * bx )

				if dx < (self.radius + target.radius) and ( self.relation_to >= -self.forward_angle and self.relation_to <= self.forward_angle )  :
					self.collided_with = target

					if target.object_type == 1:
						self.food += 1
						self.energy += target.amount
					
					if target.object_type == -1:
						self.toxin += 1
						self.energy -= target.amount

					target.consumed = 1

		self.close_to = closest
		return targets



	def draw( self, display ):

		fixed_x  = Helper.to_fixed( self.x )
		fixed_y  = Helper.to_fixed( self.y )

		fixed_dx = Helper.to_fixed(self.x + Helper.delta_x(self.rotation, self.radius))
		fixed_dy = Helper.to_fixed(self.y + Helper.delta_y(self.rotation, self.radius))

		pygame.draw.circle( display, self.color, (fixed_x, fixed_y), self.radius, 0)
		pygame.draw.circle( display, [0,0,0], (fixed_x, fixed_y), self.radius, 1)
		pygame.draw.aaline( display, [0,0,0], (fixed_x, fixed_y), (fixed_dx, fixed_dy), 1)