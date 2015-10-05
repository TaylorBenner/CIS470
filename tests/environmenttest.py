import unittest, sys
sys.path.append("..")

import configuration

'''Environment Class Test Cases'''
class EnvironmentTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(EnvironmentTest("testShouldInitializeMembers"))
		return suite

	def setUp( self ):
		from project import Environment
		self.environment = Environment()

	def testShouldInitializeMembers( self ):
		assert len(self.environment.members) == configuration.POPULATION_SIZE, "Member count does not match population size"


	def tearDown( self ):
		self.member = None


runner = unittest.TextTestRunner()
runner.run(EnvironmentTest.buildSuite())