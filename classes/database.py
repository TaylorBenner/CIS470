import config, shelve, time

class Database:
	def __init__( self ):		
		self.filename = config.database_filename
		self.database = shelve.open( self.filename )
		

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