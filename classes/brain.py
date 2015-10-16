import random
from pybrain import *

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
				self.add_random_connection()

	def randomize_connection( self, c = None ):
		if c == None:
			m = random.choice( self.logic_neurons )
			c = random.choice( self.network.connections[m] )
		c.randomize()

	def build_network( self ):

		self.network = FeedForwardNetwork()

		self.add_input(self.tanh_neuron())
		self.add_input(self.tanh_neuron())
		self.add_input(self.tanh_neuron())

		self.add_logic(self.linear_neuron())
		self.add_logic(self.linear_neuron())
		self.add_logic(self.linear_neuron())

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

