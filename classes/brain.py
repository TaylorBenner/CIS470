from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import *

class Brain:

	def __init__( self, network = None ):

		if not network:
			self.network = self.build_network()
		else:
			self.network = network

	def build_network( self ):
		net = FeedForwardNetwork()

		l1 = LinearLayer(4)
		l2 = LinearLayer(1)
		l3 = LinearLayer(2)

		net.addInputModule( l1 )
		net.addModule( l2 )
		net.addOutputModule( l3 )

		net.addConnection(FullConnection(l1,l2))
		net.addConnection(FullConnection(l2,l3))

		net.sortModules()
		return net

	def activate( self, params ):
		if params:
			return self.network.activate( params )

