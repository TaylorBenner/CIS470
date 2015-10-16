from brain import Brain
from helper import *
import config, pygame

class Member:

	max_energy = config.member_max_energy

	def __init__( self ):
		self.radius 	 = config.member_radius
		self.color  	 = Helper.random_color()

		self.brain       = Brain()

		self.x 			 = None
		self.y 			 = None

		self.energy      = self.max_energy
		self.distance    = 0.0
		self.relation    = 0.0
		self.rotation    = 0.0
		self.speed       = 0.0

		self.left_track  = None
		self.right_track = None

		self.close_to    = None
		self.alive 		 = True
		self.food 		 = 0
		self.score       = 0
		self.norm_score  = 0.0
		self.mutations   = 0

		self.error_count = 0

		self.born 		 = pygame.time.get_ticks()
		self.died		 = None
		self.lifespan    = 0

		self.generation  = 0
		self.member_num  = 0

	def update_member_state( self ):

		if self.energy == 0 or self.energy > 5000:
			self.alive    = False
			self.died  	  = pygame.time.get_ticks()
			self.lifespan = self.died - self.born
		else:
			self.alive = True

		if self.alive:
			self.process_network()
			self.rotation += (self.left_track - self.right_track) / self.radius
			if self.rotation > (2 * math.pi): self.rotation = 0
			elif self.rotation < 0: self.rotation = (2 * math.pi)
			self.speed = self.left_track + self.right_track

			if self.close_to != None:
				self.distance = Helper.get_distance(self,self.close_to)
				self.relation = Helper.get_relation_to(self,self.close_to)

			self.energy -= config.energy_loss


	def update_member_position( self ):

		if self.alive:

			x_move = self.x + Helper.delta_x( self.rotation, self.speed )
			y_move = self.y + Helper.delta_y( self.rotation, self.speed )

			if x_move > config.viewport_width: x_move = 0
			elif x_move < 0: x_move = config.viewport_width

			if y_move > config.viewport_height: y_move = 0
			elif y_move < 0: y_move = config.viewport_height

			self.x, self.y = x_move, y_move
	
	def process_network( self ):
		if self.error_count < 10:
			try:
				self.left_track, self.right_track = self.brain.activate_network(self.get_params())
			except:
				self.brain.network.sortModules()
				self.error_count += 1
				self.process_network()
		else:
			self.left_track, self.right_track = [0,0]
			self.color = [20,20,20]

	def get_params( self ):
		energy_input 	= Helper.make_uniform(self.energy, 1)
		distance 		= Helper.make_uniform(self.distance, 2)
		relation		= Helper.make_uniform(self.relation, 2)
		return [ energy_input, distance, relation ]

	def draw( self, display ):
		if self.alive:
			dx = self.x + Helper.delta_x( self.rotation, self.radius )
			dy = self.y + Helper.delta_y( self.rotation, self.radius )
			# if self.close_to != None and config.debug: pygame.draw.aaline( display, [130,130,130], (Helper.fixed(self.x), Helper.fixed(self.y)), (Helper.fixed(self.close_to.x), Helper.fixed(self.close_to.y)), 1)
			pygame.draw.circle( display, self.color, (Helper.fixed(self.x), Helper.fixed(self.y)), self.radius, 0)
			pygame.draw.circle( display, [0,0,0], (Helper.fixed(self.x), Helper.fixed(self.y)), self.radius, 1)
			pygame.draw.aaline( display, [0,0,0], (Helper.fixed(self.x), Helper.fixed(self.y)), (Helper.fixed(dx), Helper.fixed(dy)), 1)

			if config.debug:
				font = pygame.font.SysFont("monospace", 10)

				label = font.render(str(self.mutations), 1, [0,0,0] )
				display.blit( label, (self.x - 6, self.y + 10))

				label = font.render(str(self.food), 1, [0,0,0] )
				display.blit( label, (self.x, self.y + 10))

