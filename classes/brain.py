from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *

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


