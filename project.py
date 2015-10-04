import random, pygame, sys, math, numpy, itertools
from matplotlib import pyplot as plt
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *

DEBUG        = True
WIDTH        = 600
HEIGHT       = 600
MUTATION_RATE = .05

#   Debugging Globals
_max_collision_time       = 0.0
_max_update_position_time = 0.0
_max_update_state_time    = 0.0
_max_update_time          = 0.0
_max_crossover_time       = 0.0
_max_mutation_time        = 0.0
_max_update_target_time   = 0.0
_max_score_time           = 0.0

_steps = 0



class Main:
	def __init__( self ):
		pygame.init()
		self.running        = True
		self.display        = pygame.display.set_mode([WIDTH, HEIGHT], pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.clock          = pygame.time.Clock()
		self.font           = pygame.font.SysFont("monospace", 12)
 
	# init function
	def init( self ):
		self.display.fill((255,255,255))
		pygame.display.flip()

		self.env = Environment()

	# events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	# update loop
	def update( self ):

		global _max_update_time
		t1 = int(pygame.time.get_ticks())

		active = False
		for member in self.env.members:
			if member.alive:
				member.update_state()
				member.update_position()
				self.env.targets = member.check_collisions( self.env.getTargets() )
				active = True

		self.env.update_targets()

		# all members dead
		if not active:
			self.env.score_members()
			self.env.perform_selection()
			self.env.perform_crossover()
			self.env.perform_mutation()
			self.env.generations += 1


		td = float(int(pygame.time.get_ticks())-t1)
		_max_update_time = td if td > _max_update_time else _max_update_time

	# render function
	def render( self ):
		self.display.fill((255,255,255))

		for obj in self.env.getObjects():
			if obj: obj.draw( self.display )

		gen_lbl = self.font.render("Generation: " + str(self.env.generations), 1, [0,0,0] )
		self.display.blit( gen_lbl, (10,10))

		steps_lbl = self.font.render("Steps: " + str(_steps), 1, [0,0,0] )
		self.display.blit( steps_lbl, (10,30))

		pygame.display.flip()

	# closure function
	def cleanup( self ):
		print ""
		print "maximum update() time            :%i ms" % _max_update_time
		print "---------------------------------------"
		print "maximum update_position() time   :%i ms" % _max_update_position_time
		print "maximum update_state() time      :%i ms" % _max_update_state_time
		print "maximum check_collision() time   :%i ms" % _max_collision_time
		print "maximum update_targets() time    :%i ms\n" % _max_update_target_time
		print "---------------------------------------"
		print "maximum score_members() time     :%i ms" % _max_score_time
		print "maximum perform_crossover() time :%i ms" % _max_crossover_time
		print "maximum perform_mutation() time  :%i ms\n" % _max_mutation_time
		pygame.quit()
 
	# main loop
	def execute( self ):

		global _steps 

		if self.init() == False:
			self.running = False

		while( self.running ):
			self.clock.tick(60)
			for event in pygame.event.get():
				self.events(event)

			self.update()
			self.render()
			_steps += 1

		self.cleanup()


class Environment:
	#   class members 
	_MEMBER_COUNT    = 30
	_FOOD_COUNT      = 10
	_TOXIN_COUNT     = 0

	_MEMBERS_SPAWNED = 0
	_FOOD_SPAWNED    = 0
	_TOXIN_SPAWNED   = 0

	#   class methods
	def __init__( self ):

		#   instance members
		self.food       = []
		self.toxins     = []
		self.members    = []
		self.parents    = []

		self.generations = 0

		for f in range(self._FOOD_COUNT): self.new_food()
		for t in range(self._TOXIN_COUNT): self.new_toxin()
		for m in range(self._MEMBER_COUNT): self.new_member()

	def getObjects( self ):
		return self.food + self.members + self.toxins

	def getTargets( self ):
		return self.food + self.toxins

	def new_member( self, network = None, color = None, i = None, l = None, o = None, c = None ):
		self.members.append( Member( self._MEMBERS_SPAWNED+1, network, color, i = i, l = l, o = o, c = c ) )
		self._MEMBERS_SPAWNED += 1

	def new_food( self ):
		self.food.append( Target( self._FOOD_SPAWNED+1, "food" ) )
		self._FOOD_SPAWNED += 1

	def new_toxin( self ):
		self.toxins.append( Target( self._TOXIN_SPAWNED+1, "toxin" ) )
		self._TOXIN_SPAWNED += 1

	def score_members( self ):

		global _max_score_time
		t1 = int(pygame.time.get_ticks())

		if DEBUG: print "\nrunning scoring..."
		total_score             = 0.0
		total_normalized_score  = 0.0

		for member in self.members:

			score = member.lifespan + (member.food * 1000) - (member.toxin * 1000)
			if score < 0: score = 0

			member.score = float(score)
			total_score += member.score

		for member in self.members:
			if total_score == 0: total_score = 1
			member.score = float( member.score / total_score)
			total_normalized_score += member.score

		print "total normalized: %f \n" % total_normalized_score

		td = float(int(pygame.time.get_ticks())-t1)
		_max_score_time = td if td > _max_score_time else _max_score_time

	def perform_selection( self ):
		if DEBUG: print "running selection..."
		self.members.sort( key = lambda member: member.score, reverse=True )
		for m in self.members:
			print "member %i - lifespan: %i - score: %f" %( m.member_number, m.lifespan, m.score )
		print ""

		# parent_count = int(math.floor((self._MEMBER_COUNT/2)/2)*2)
		parent_count = self._MEMBER_COUNT / 2
		self.parents = self.members[:parent_count]
		self.members = []

	def perform_crossover( self ):

		global _max_crossover_time
		t1 = int(pygame.time.get_ticks())
		if DEBUG: print "running crossover..."

		for parent in self.parents:
			child_count = self._MEMBER_COUNT / len(self.parents)
			for child in range(child_count):
				if random.random() <= MUTATION_RATE:
					self.new_member()
				else:
					self.new_member( 
						parent.brain.network, parent.color, i = parent.brain.input_neurons,
						l = parent.brain.logic_neurons, o = parent.brain.output_neurons, 
						c = parent.brain.connections 
					)


		for remaining in range( self._MEMBER_COUNT - len(self.members) ):
			self.new_member()

		td = float(int(pygame.time.get_ticks())-t1)
		_max_crossover_time = td if td > _max_crossover_time else _max_crossover_time
	
	def perform_mutation( self ):

		global _max_mutation_time
		t1 = int(pygame.time.get_ticks())

		if DEBUG: print "running mutation..."
		for member in self.members:
			mutations = 0

			for module in member.brain.network.modules:
				for connection in member.brain.network.connections[module]:
					if random.random() <= MUTATION_RATE:
						member.brain.randomize_connection( connection )

			if random.random() <= MUTATION_RATE:
				mutations += 1
				if DEBUG: print "member %i added new neuron" % member.member_number
				member.brain.add_random_neuron()

			if random.random() <= MUTATION_RATE:
				mutations += 1
				if DEBUG: print "member %i added new connection" % member.member_number
				member.brain.add_random_connection()

			if mutations > 0:
				delta_change = ((float(mutations) / 100) * 255) * 6
				for color in member.color:
					c = float(color)
					if (c + delta_change) > 255:
						color = int(c - delta_change)
					else:
						color = int(c + delta_change)
				if DEBUG: print "member %i had %i mutations" % (member.member_number, mutations)
			member.mutations = mutations
		if DEBUG: print ""

		td = float(int(pygame.time.get_ticks())-t1)
		_max_mutation_time = td if td > _max_mutation_time else _max_mutation_time

	def update_targets( self ):

		global _max_update_target_time
		t1 = int(pygame.time.get_ticks())

		for obj in self.getTargets():
			if obj.consumed == 1:

				if obj.object_code == 1:
					self.food.remove( obj )
					self.new_food()

				elif obj.object_code == -1:
					self.toxins.remove( obj )
					self.new_toxin()

		td = float(int(pygame.time.get_ticks())-t1)
		_max_update_target_time = td if td > _max_update_target_time else _max_update_target_time


class Target:
	#   class members 
	radius          = 5
	amount          = 500

	#   class methods
	def __init__( self, number, obj_type ): 

		self.x, self.y      = random_coordinates( radius = (self.radius+1) )
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
		pygame.draw.circle( display, c, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, s, (toFixed(self.x), toFixed(self.y)), self.radius, 1)


class Member:
	#   class members 
	radius          = 10
	object_type     = "member"
	max_energy      = 1000

	#   class methods
	def __init__( self, number, net, color, i = None, l = None, o = None, c = None ):

		#   instance members
		self.member_number = number

		self.x, self.y    = random_coordinates( radius = self.radius )
		self.color        = random_color() if not color else color
		self.stroke       = calculate_contrast( self.color )

		self.collided_with = None
		self.close_to      = None

		self.radians       = 0.0
		self.left_track    = 0.0
		self.right_track   = 0.0

		self.energy       = self.max_energy
		self.alive        = 1

		self.food         = 0
		self.toxin        = 0
		self.brain        = Brain( network = net, i = i, l = l, o = o, c = c ) if net else Brain()

		self.born_time    = int(pygame.time.get_ticks())
		self.death_time   = 0.0
		self.lifespan     = 0.0

		self.score         = 0.0
		self.mutations     = 0

		self.relation_to   = 0.0
		self.distance_to   = 0.0
		self.heart         = 0

		self.energy_input  = 0.0
		self.forward_angle = 40

	def update_position( self ):

		global _max_update_position_time		
		t1 = int(pygame.time.get_ticks())
		if self.alive == 1:

			object_type = 0 if self.close_to == None else self.close_to.object_code

			#   process track output
			self.left_track, self.right_track = self.brain.activate([
				self.distance_to, self.relation_to, object_type, self.energy_input
			])

			#   increment rotation
			self.radians  += ((self.left_track - self.right_track) / self.radius)
			if self.radians > 2*math.pi: self.radians = 0
			elif self.radians < 0: self.radians = 2*math.pi

			#   calculate speed
			self.velocity =  (self.left_track + self.right_track) 

			#   find delta parameters for moving
			move_x_del = deltaX( self.radians, self.velocity )
			move_y_del = deltaY( self.radians, self.velocity )

			dx = (self.x + move_x_del)
			dy = (self.y + move_y_del) 

			if dx < 0: self.x = WIDTH
			elif dx > WIDTH: self.x = 0
			else: self.x = dx

			if dy < 0: self.y = HEIGHT
			elif dy > HEIGHT: self.y = 0
			else: self.y = dy

		td = float(int(pygame.time.get_ticks())-t1)
		_max_update_position_time = td if td > _max_update_position_time else _max_update_position_time


	def update_state( self ):

		global _max_update_state_time
		global _steps

		t1 = int(pygame.time.get_ticks())

		#   living requires energy
		self.energy -= 1

		#   check energy levels
		if   self.energy <= 0: self.alive = 0
		elif self.energy > 2000: self.alive = 0

		if not self.alive:
			self.close_to = []
			self.death_time = int(pygame.time.get_ticks())
			self.lifespan   = (self.death_time - self.born_time)

			if DEBUG:
				reason = "starvation" if self.energy <= 0 else "overeating"
				print "member %i has died after %i seconds due to %s" % (self.member_number, (self.lifespan/1000), reason)

		else:

			if self.energy <= self.max_energy: self.energy_input = 1 - (self.energy / self.max_energy)
			else: self.energy_input = -1

			if self.close_to:
				self.distance_to = getSlope([self.x,self.y], [self.close_to.x, self.close_to.y])
				angle       	 = getAngle([self.x, self.y], [self.close_to.x, self.close_to.y])

				# calculate reltation to target
				self.relation_to = (abs(math.degrees(angle) - math.degrees(self.radians)) - 180)
			else:
				self.distance_to  = -1
				self.relation_to  = -1 


		td = float(int(pygame.time.get_ticks())-t1)
		_max_update_state_time = td if td > _max_update_state_time else _max_update_state_time

	def check_collisions( self, targets ):

		closest = None
		distance_to_closest = 0.0
		tolerance = self.radius * 5

		global _max_collision_time
		t1 = int(pygame.time.get_ticks())

		for target in targets:
			if numpy.isclose( [self.x, self.y], [target.x,target.y], atol = tolerance ).all():

				if closest == None:
					closest = target
					distance_to_closest = getSlope([self.x,self.y],[target.x,target.y])
				else:
					distance_to_tar = getSlope([self.x,self.y],[target.x,target.y])
					if distance_to_tar < distance_to_closest:
						closest = target
						distance_to_closest = getSlope([self.x,self.y],[target.x,target.y])

				ax = self.x - target.x
				bx = self.y - target.y
				dx = math.sqrt( ax * ax + bx * bx )

				if dx < (self.radius + target.radius) and ( self.relation_to >= -self.forward_angle and self.relation_to <= self.forward_angle )  :
					self.collided_with = target

					if target.object_code == 1:
						self.food += 1
						self.energy += target.amount
					
					if target.object_code == -1:
						self.toxin += 1
						self.energy -= target.amount

					target.consumed = 1

		self.close_to = closest
		td = float(int(pygame.time.get_ticks())-t1)
		_max_collision_time = td if td > _max_collision_time else _max_collision_time

		return targets

	def draw( self, display ):

		c, s = self.color, self.stroke
		if not self.alive:
			c = [70,70,70]
			s = [0,0,0]

		dx = self.x + deltaX( self.radians, self.radius )
		dy = self.y + deltaY( self.radians, self.radius )
		pygame.draw.circle( display, c, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, [0,0,0], (toFixed(self.x), toFixed(self.y)), self.radius, 1)

		if self.mutations > 0:
			pygame.draw.circle( display, s, (toFixed(self.x), toFixed(self.y)), self.radius / 3, 0)

		pygame.draw.aaline( display, s, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

		if self.alive:

			if DEBUG:
				bar_height  = 5
				bar_width   = (self.radius * 2) + 2

				bar_y       = self.y - self.radius - 10
				bar_x       = self.x - self.radius

				bar_rect = pygame.Rect([(bar_x, bar_y),(bar_width, bar_height)])

				energy_percent   = (float(self.energy) / float(self.max_energy))
				bar_fill_amount  = (float(self.radius * 2)) * energy_percent

				bar_fill_amount = bar_width if bar_fill_amount > bar_width else bar_fill_amount

				bar_fill = pygame.Rect([(bar_x, bar_y),(toFixed(bar_fill_amount), bar_height)])

				pygame.draw.rect( display, (100,200,100), bar_fill, 0)
				pygame.draw.rect( display, (0,0,0), bar_rect, 1)

			if DEBUG and self.close_to:
				pygame.draw.aaline( display, [90,90,90], (toFixed(self.x), toFixed(self.y)), (toFixed(self.close_to.x), toFixed(self.close_to.y)), 1)

				if self.relation_to >= -self.forward_angle and self.relation_to <= self.forward_angle:
					pygame.draw.circle( display, [150,150,50], (toFixed(self.x), toFixed(self.y)), self.radius + 5, 1)


class Brain:

	def __init__( self, network = None, i = None, l = None, o = None, c = None ):

		self.input_neurons    = [] if i == None else i
		self.logic_neurons    = [] if l == None else l
		self.output_neurons   = [] if o == None else o

		self.connections      = [] if c == None else c
		self.network          = network if network else None

		if self.network == None:
			self.build()

	def sig_neuron( self, name=None ):
		return SigmoidLayer(1, name=name)

	def tanh_neuron( self, name=None ):
		return TanhLayer(1, name=name)

	def linear_neuron( self, name=None ):
		return LinearLayer(1, name=name)

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

	def build( self ):

		self.network = FeedForwardNetwork()

		self.add_input(self.linear_neuron("distance_n"))
		self.add_input(self.linear_neuron("angle_n"))
		self.add_input(self.tanh_neuron("type_n"))
		self.add_input(self.tanh_neuron("energy_n"))

		self.add_logic(self.sig_neuron("logic_1a"))
		self.add_logic(self.sig_neuron("logic_1b"))
		self.add_logic(self.sig_neuron("logic_1c"))
		self.add_logic(self.sig_neuron("logic_1d"))
		self.add_logic(self.sig_neuron("logic_2a"))
		self.add_logic(self.sig_neuron("logic_2b"))

		self.add_output(self.linear_neuron("left_n"))
		self.add_output(self.linear_neuron("right_n"))

		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[0], self.logic_neurons[3]))

		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[1], self.logic_neurons[3]))

		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[2], self.logic_neurons[3]))

		self.add_connection(FullConnection(self.input_neurons[3], self.logic_neurons[0]))
		self.add_connection(FullConnection(self.input_neurons[3], self.logic_neurons[1]))
		self.add_connection(FullConnection(self.input_neurons[3], self.logic_neurons[2]))
		self.add_connection(FullConnection(self.input_neurons[3], self.logic_neurons[3]))

		self.add_connection(FullConnection(self.logic_neurons[0], self.logic_neurons[4]))
		self.add_connection(FullConnection(self.logic_neurons[0], self.logic_neurons[5]))

		self.add_connection(FullConnection(self.logic_neurons[1], self.logic_neurons[4]))
		self.add_connection(FullConnection(self.logic_neurons[1], self.logic_neurons[5]))

		self.add_connection(FullConnection(self.logic_neurons[2], self.logic_neurons[4]))
		self.add_connection(FullConnection(self.logic_neurons[2], self.logic_neurons[5]))

		self.add_connection(FullConnection(self.logic_neurons[3], self.logic_neurons[4]))
		self.add_connection(FullConnection(self.logic_neurons[3], self.logic_neurons[5]))

		self.add_connection(FullConnection(self.logic_neurons[4], self.output_neurons[0]))
		self.add_connection(FullConnection(self.logic_neurons[4], self.output_neurons[1]))

		self.add_connection(FullConnection(self.logic_neurons[5], self.output_neurons[0]))
		self.add_connection(FullConnection(self.logic_neurons[5], self.output_neurons[1]))

		self.network.sortModules()

	def activate( self, params ):
		return self.network.activate( params )

	def all_neurons( self ):
		return self.input_neurons + self.logic_neurons + self.output_neurons

	def randomize_connection( self, c = None ):
		if c == None:
			m = random.choice( self.logic_neurons )
			c = random.choice( self.network.connections[m] )
		c.randomize()

	def add_random_neuron( self ):

		n1 = SigmoidLayer(1)
		n2 = random.choice(self.all_neurons())

		self.add_logic( n1 )
		c1 = FullConnection(n1,n2)
		self.add_connection(c1)
		self.network.sortModules()

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


def calculate_contrast( color ):
	l = ((0.299 * color[0]) + (0.587 * color[1]) + (0.114 * color[2]))
	return [0,0,0] if l > 60 else [150,150,150]

def random_color():
	return [ random.randint(0,255) for i in range(3) ]

def random_coordinates( radius = 0 ):
	x = random.randint(radius,WIDTH-radius)
	y = random.randint(radius,HEIGHT-radius)
	return [x,y]

def toFixed( number ):
	return int(math.floor(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

def getSlope( ref, tar ):
	ax, ay = ref
	bx, by = tar
	return float(abs(math.hypot((ax-bx),(ay-by))))

def getAngle( ref, tar ):
	dx = ref[0] - tar[0]
	dy = ref[1] - tar[1]
	return math.atan2( dx, dy )


if __name__ == "__main__" :
	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]
	main_window = Main()
	main_window.execute()