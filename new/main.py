import config, random, math, pygame, sys
from copy import deepcopy
from pybrain import *


class Main:
	def __init__( self ):
		pygame.init()
		self.running        = True
		self.will_render    = True
		self.display        = pygame.display.set_mode(
								[config.window_width, config.window_height], 
								pygame.HWSURFACE | pygame.DOUBLEBUF
							  )
		self.clock          = pygame.time.Clock()
		self.font           = pygame.font.SysFont("monospace", 12)
		self.environment    = Environment()
		self.steps			= 0
		self.sim_start		= pygame.time.get_ticks()

		self.display.fill((255,255,255))
		pygame.display.flip()

	def execute( self ):
		while( self.running ):

			if not self.will_render:
				self.clock.tick(60)

			for event in pygame.event.get():
				self.events(event)

			keys = pygame.key.get_pressed() 
			if keys[pygame.K_SPACE]:
				self.will_render = False
			else:
				self.will_render = True

			self.update()
			self.render()
			self.steps += 1

		self.cleanup()

	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	def update( self ):

		self.environment.update_all()
		if self.environment.has_active == False:

			self.environment.perform_scoring()
			self.environment.perform_selection()
			self.environment.perform_crossover()
			self.environment.perform_mutation()

			self.environment.generations += 1

	def render( self ):

		self.display.fill((255,255,255))

		for obj in self.environment.get_objects():
			obj.draw( self.display )

		pygame.draw.rect( self.display, [150,150,150], [config.viewport_width, 0, config.window_width - config.viewport_width, config.viewport_height])
		pygame.draw.aaline( self.display, [0,0,0], [config.viewport_width, 0], [config.viewport_width, config.viewport_height], 1)

		labels = [
			self.font.render("Mutation Rate: " + str(config.mutation_rate * 100) + '%', 1, [0,0,0] ),
			self.font.render("Selection Rate: " + str(config.selection_rate * 100) + '%', 1, [0,0,0] ),
			self.font.render("Simulation Steps: " + str(self.steps), 1, [0,0,0] ),
			self.font.render("Generation: " + str(self.environment.generations), 1, [0,0,0] ),
			self.font.render("Members Alive: " + str(self.environment.remaining), 1, [0,0,0] ),
			self.font.render("Overall Best:", 1, [0,0,0] )
		]

		if self.environment.overall_best != None:
			labels.append(self.font.render("Score   : " + str(self.environment.overall_best.score), 1, [0,0,0] ))
			labels.append(self.font.render("Neurons : " + str(len(self.environment.overall_best.brain.all_neurons())), 1, [0,0,0] ))
			labels.append(self.font.render("Food    : " + str(self.environment.overall_best.food), 1, [0,0,0] ))

		padding_increment = 10

		for ind, label in enumerate(labels):
			self.display.blit( label, (config.viewport_width + config.panel_padding, padding_increment))
			if ind == 4 or ind == 1: padding_increment += 20
			else: padding_increment += 10

		pygame.display.flip()

	def cleanup( self ):
		pygame.quit()



class Environment:
	def __init__( self ):
		
		# init placeholder
		self.members 	  = []
		self.targets 	  = []
		self.parents      = []
		self.current_best = None
		self.overall_best = None

		# init members and targets
		self.members 	 = [ self.add_new_member() for i in range(config.population_size) ]
		self.targets 	 = [ self.add_new_target() for i in range(config.target_count) ]

		self.has_active  = False
		self.generations = 1
		self.remaining   = 0


	def add_new_member( self ):
		new_member 		= Member()
		x,y 			= Helper.nonintersecting_coordinates( new_member.radius, self.get_positions() )
		new_member.x  	= x
		new_member.y 	= y
		return new_member

	def add_new_target( self ):
		new_target 		= Target()
		x,y 			= Helper.nonintersecting_coordinates( new_target.radius, self.get_positions() )
		new_target.x  	= x
		new_target.y 	= y
		return new_target

	def get_objects( self ):
		return self.members + self.targets

	def get_positions( self ):
		return [[obj.x,obj.y] for obj in self.get_objects()]

	def check_collisions( self, member ):
		if member.alive:
			closest_target = None
			for target in self.targets:
				if Helper.is_close( member, target ):

					if closest_target == None: 
						closest_target = target

					current_distance = Helper.get_distance( member, target )
					closest_distance = Helper.get_distance( member, closest_target )

					if current_distance < closest_distance: 
						closest_target = target

					if Helper.is_collided( member, target ):
						target.consumed  = True
						member.energy 	+= target.energy_amount
						member.food 	+= 1
						closest_target 	 = None

			member.close_to = closest_target

	def update_all( self ):

		number_alive 	= 0
		self.has_active = False

		for member in self.members:
			member.update_member_state()
			member.update_member_position()
			self.check_collisions( member )

			if member.alive:
				number_alive += 1
				self.has_active = True


		for target in self.targets:
			if target.consumed:
				self.targets.remove( target )
				self.targets.append(self.add_new_target())

		self.remaining = number_alive

	def perform_scoring( self ):

		total_score 		= 0.0
		total_norm_score 	= 0.0

		for member in self.members:
			member.score = (member.lifespan / 1000) * member.food
			if member.score == 0 : member.score = 1
			total_score += member.score

			if self.current_best == None:
				self.current_best = member

			if member.score > self.current_best.score:
				self.current_best = member

		for member in self.members:
			member.norm_score = member.score / total_score
			total_norm_score += member.norm_score


		if self.overall_best == None:
			self.overall_best = self.current_best

		elif self.current_best.score > self.overall_best.score:
			self.overall_best = self.current_best


	def perform_selection( self ):
		self.members.sort( key = lambda member: member.score, reverse=True )
		parent_count = int(float(config.population_size) * config.selection_rate)
		self.parents = self.members[:parent_count]
		self.members = []

	def perform_crossover( self ):

		for parent in self.parents:
			for i in range(config.population_size / len(self.parents)):
				child = self.add_new_member()

				if random.random() >= config.mutation_rate:
					child.brain = deepcopy(parent.brain)
					child.brain.network.sortModules()
					child.color = parent.color

				self.members.append( child )

		for remaining in range(config.population_size - len(self.members)):
			child = self.add_new_member()
			self.members.append( child )


	def perform_mutation( self ):
		for member in self.members:
			mutations = 0
			# if random.random() <= config.mutation_rate:
			# 	member.brain.add_random_neuron()
			# 	mutations += 1

			# if random.random() <= config.mutation_rate:
			# 	member.brain.add_random_connection()
			# 	mutations += 1

			if random.random() <= config.mutation_rate:
				member.brain.randomize_connection()
				mutations += 1

			member.mutations = mutations




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

	def update_member_state( self ):

		if self.energy == 0 or self.energy > 5000:
			self.alive    = False
			self.died  	  = pygame.time.get_ticks()
			self.lifespan = self.died - self.born

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


class Brain:
	def __init__( self ):

		self.network 			= []
		self.input_neurons		= []
		self.logic_neurons		= []
		self.output_neurons		= []
		self.connections		= []

		self.build_network()

	def sig_neuron( self ):
		return SigmoidLayer(1)

	def tanh_neuron( self ):
		return TanhLayer(1)

	def linear_neuron( self ):
		return LinearLayer(1)

	def add_input( self, n ):
		self.input_neurons.append( n )
		self.network.addInputModule( n )

	def add_output( self, n ):
		self.output_neurons.append( n )
		self.network.addOutputModule( n )

	def add_logic( self, n ):
		self.logic_neurons.append( n )
		self.network.addModule( n )

	def add_connection( self, c ):
		self.connections.append( c )
		self.network.addConnection( c )

	def add_random_neuron( self ):
		n1 = random.choice([SigmoidLayer(1), LinearLayer(1), TanhLayer(1), GaussianLayer(1)])
		n2 = random.choice(self.all_neurons())
		self.add_logic( n1 )
		c1 = FullConnection(n1,n2)
		self.add_connection(c1)
		self.network.sortModules()

	def all_neurons( self ):
		return self.input_neurons + self.logic_neurons + self.output_neurons

	def remove_connection( self, c ):
		self.connections.remove( c )
		for m in self.network.modules:
			for v in self.network.connections[m]:
				if v is c:
					self.network.connections[m].remove(v)
		self.network.sortModules()

	def add_random_connection( self ):
		c1 = None
		try:
			n1 = random.choice(self.all_neurons())
			n2 = random.choice(self.all_neurons())
			c1 = FullConnection(n1,n2)
			if n1.name is not n2.name: 
				self.add_connection(c1)	
			self.network.sortModules()
		except: 
			if c1 != None:
				self.remove_connection(c1)

	def randomize_connection( self, c = None ):
		if c == None:
			m = random.choice( self.logic_neurons )
			c = random.choice( self.network.connections[m] )
		c.randomize()

	def build_network( self ):

		self.network = FeedForwardNetwork()

		self.add_input(self.sig_neuron())
		self.add_input(self.sig_neuron())
		self.add_input(self.sig_neuron())

		self.add_logic(self.sig_neuron())
		self.add_logic(self.sig_neuron())
		self.add_logic(self.sig_neuron())

		self.add_output(self.tanh_neuron())
		self.add_output(self.tanh_neuron())

		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[0]))

		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[1]))

		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[2]))

		self.add_connection(FullConnection(self.logic_neurons[0], self.output_neurons[0]))
		self.add_connection(FullConnection(self.logic_neurons[0], self.output_neurons[1]))

		self.add_connection(FullConnection(self.logic_neurons[1], self.output_neurons[0]))
		self.add_connection(FullConnection(self.logic_neurons[1], self.output_neurons[1]))

		self.add_connection(FullConnection(self.logic_neurons[2], self.output_neurons[0]))
		self.add_connection(FullConnection(self.logic_neurons[2], self.output_neurons[1]))

		self.network.sortModules()

	def activate_network( self, params ):
		if params:
			return self.network.activate( params )


class Database:
	def __init__( self ):
		pass


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



if __name__ == "__main__" :
	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]
	main_window = Main()
	main_window.execute()