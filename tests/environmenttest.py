import unittest, sys
sys.path.append("..")

import configuration

'''Environment Class Test Cases'''
class EnvironmentTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(EnvironmentTest("testShouldInitialize"))
		return suite

	def setUp( self ):
		from project import Environment
		self.environment = Environment()

	def testShouldInitialize( self ):
		assert len(self.environment.members) == configuration.POPULATION_SIZE, "Member count does not match configuration file"
		assert len(self.environment.targets) == configuration.TARGET_COUNT, "Target count does not match configuration file"


	def tearDown( self ):
		self.environment = None


runner = unittest.TextTestRunner()
runner.run(EnvironmentTest.buildSuite())