import unittest, sys, random
sys.path.append("..")
from pybrain import *
import config


'''Brain Class Test Cases'''
class BrainTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(BrainTest("testShouldBuildNetwork"))
		suite.addTest(BrainTest("testShouldAddConnection"))
		suite.addTest(BrainTest("testShouldAddNeuron"))
		suite.addTest(BrainTest("testShouldRandomizeConnection"))
		return suite

	def setUp( self ):
		from classes.brain import Brain	
		self.brain = Brain()	

	def testShouldBuildNetwork( self ):
		assert self.brain.network is not None, "network not initialized"

	def testShouldAddConnection( self ):
		before = 0
		for mod in self.brain.network.modules:
			for con in self.brain.network.connections[mod]:
				before += 1
		self.brain.add_random_connection()
		after = 0
		for mod in self.brain.network.modules:
			for con in self.brain.network.connections[mod]:
				after += 1
		assert after == before + 1, "connection not added"

	def testShouldAddNeuron( self ):
		before = 0
		for mod in self.brain.network.modules:
			before += 1
		self.brain.add_random_neuron()
		after = 0
		for mod in self.brain.network.modules:
			after += 1
		assert after == before + 1, "connection not added"

	def testShouldRandomizeConnection( self ):
		c = self.brain.connections[0]
		b = c.params[0]
		self.brain.randomize_connection(c)
		d = c.params[0]

		self.assertNotAlmostEqual(b,d), "connection not randomized"


	def tearDown( self ):
		self.member = None
