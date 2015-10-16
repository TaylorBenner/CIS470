import shelve, time, numpy
import sys
from matplotlib import pyplot as plt

sys.path.append("..") 
import config

class Database:
	def __init__( self ):		
		self.filename = config.database_filename
		self.database = shelve.open( "../" + self.filename )
		

	def generate_key( self, member ):
		return "%i-%i-%i-%i" % (member.member_num, member.generation, member.score, time.time())


	def save_population( self, members ):
		for member in members:
			key = self.generate_key( member )
			if key not in self.database:
				self.database[key] = {
					"food"		: member.food,
					"weights"	: member.brain.network.params,
					"lifespan"	: member.lifespan,
					"mutations" : member.mutations
				}

	def get_by_key( self, key ):
		return self.database[key]

	def get_all_keys( self ):
		return self.database.keys()

	def get_all_from_generation( self, generation ):
		records = []
		for key in self.get_all_keys():
			if self.get_member_generation(key) == generation:
				records.append( key )
		return records

	def get_member_num( self, key ):
		parts = key.split("-")
		return int(parts[0])

	def get_member_generation( self, key ):
		parts = key.split("-")
		return int(parts[1])

	def get_member_score( self, key ):
		parts = key.split("-")
		return int(parts[2])

	def get_member_timestamp( self, key ):
		parts = key.split("-")
		return int(parts[3])

	def get_member_mutations( self, key ):
		value = self.database[key]
		return value['mutations']

	def get_best_from_generation( self, generation ):
		best = None
		for member in self.get_all_from_generation( generation ):
			if best == None: best = member
			if self.get_member_score( member ) > self.get_member_score( best ):
				best = member
		return best

	def get_best_from_each_generation( self ):
		members = []
		gen_range = self.get_number_of_generations()
		for gen in range(1, gen_range):
			members.append(self.get_best_from_generation( gen ))
		return members

	def get_number_of_generations( self ):
		max_gen = 0
		for key in self.get_all_keys():
			gen = self.get_member_generation( key )
			if  gen > max_gen:
				max_gen = gen
		return max_gen


	def graph_optimization( self ):
		plt.figure(1)
		plot_x = []
		plot_y = []

		gen_range = self.get_number_of_generations()
		for gen in range(1, gen_range):
			best = self.get_best_from_generation(gen)
			plot_x.append(gen)
			plot_y.append( self.get_member_score(best))

		plt.plot(plot_x, plot_y)
		plt.ylabel("Best Score")
		plt.xlabel("Generation")
		plt.show()

	def get_mean( self, numbers ): return sum(numbers) / float(len(numbers))



db = Database()
db.graph_optimization()



