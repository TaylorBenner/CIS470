from member import Member
from target import Target
from helper import *
from copy import deepcopy

import config

class Environment:
	def __init__( self ):

		self.has_active  = False
		self.generations = 1
		self.remaining   = 0
		
		# init placeholder
		self.members 	  = []
		self.targets 	  = []
		self.parents      = []

		self.current_best = None
		self.overall_best = None

		self.member_count = 0

		# init members and targets
		self.members 	 = [ self.add_new_member() for i in range(config.population_size) ]
		self.targets 	 = [ self.add_new_target() for i in range(config.target_count) ]



	def add_new_member( self ):
		new_member 				= Member()
		x,y 					= Helper.nonintersecting_coordinates( new_member.radius, self.get_positions() )
		new_member.x  			= x
		new_member.y 			= y
		new_member.generation 	= self.generations
		self.member_count		+= 1
		new_member.member_num	= self.member_count
		return new_member

	def add_new_target( self ):
		new_target 				= Target()
		x,y 					= Helper.nonintersecting_coordinates( new_target.radius, self.get_positions() )
		new_target.x  			= x
		new_target.y 			= y
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

					if closest_target == None: closest_target = target
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

		self.parents = []


	def perform_mutation( self ):
		for member in self.members:
			mutations = 0
			
			if random.random() <= config.mutation_rate:
				member.brain.add_random_neuron()
				mutations += 1

			if random.random() <= config.mutation_rate:
				member.brain.add_random_connection()
				mutations += 1

			if random.random() <= config.mutation_rate:
				member.brain.randomize_connection()
				mutations += 1

			member.mutations = mutations