import Member
class Population:

	def __init__( self ):

		self.population_size = 10
		self.members = [ Member.Member( i + 1) for i in range( self.population_size ) ]