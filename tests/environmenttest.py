import unittest, sys, random
sys.path.append("..")

import config

'''Environment Class Test Cases'''
class EnvironmentTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(EnvironmentTest("testTotalScoreShouldEqualOne"))
		suite.addTest(EnvironmentTest("testMemberScoreShouldEqual"))
		suite.addTest(EnvironmentTest("testSelectionShouldSort"))
		suite.addTest(EnvironmentTest("testShouldCreateNewPopulation"))
		suite.addTest(EnvironmentTest("testShouldCollideObjects"))
		suite.addTest(EnvironmentTest("testShouldTrackClosest"))
		return suite

	def setUp( self ):
		from project import Environment
		self.environment = Environment()

	def testTotalScoreShouldEqualOne( self ):
		assert len(self.environment.members) > 0, "No members added"
		self.environment.perform_scoring()
		total = 0.0
		for member in self.environment.members:
			total += member.norm_score
		self.assertAlmostEqual(total, 1), "Normalized score should equal 1"

	def testMemberScoreShouldEqual( self ):
		member = self.environment.add_new_member()
		score  = (member.lifespan / 1000) * member.food
		assert score == 0 or score == 1, "Uninitialized member should score 0 or 1"

		member.lifespan = 25000
		member.food     = 5
		score  = (member.lifespan / 1000) * member.food
		assert score == 125, "Member score did not calculate correctly"

	def testShouldSelectAtRate( self ):
		self.environment.perform_selection()
		amount = config.selection_rate * config.population_size
		assert len(self.environment.parents) == amount, "Incorrect amount of parents selected"

	def testSelectionShouldSort( self ):

		for m in self.environment.members:
			m.score = random.randint(1, 50000)
		self.environment.members.sort( key = lambda member: member.score, reverse=True )
		assert self.environment.members[0].score > self.environment.members[-1].score, "Top member is not more fit than last"

	def testShouldCreateNewPopulation( self ):
		for m in self.environment.members:
			m.lifespan = random.randint(1, 50000)
			m.food     = random.randint(0, 20)
		self.environment.perform_scoring()
		self.environment.perform_selection()
		self.environment.perform_crossover()

		assert len(self.environment.members) == config.population_size, "member count is not correct after crossover"
		assert len(self.environment.parents) == 0, "parents were not cleared after crossover"

	def testShouldCollideObjects( self ):
		member = self.environment.add_new_member()
		target = self.environment.add_new_target()

		member.x = 0
		member.y = 0

		target.x = 500
		target.y = 500

		self.environment.targets = [target]
		self.environment.check_collisions( member )

		assert target.consumed == 0, "target should not have been consumed"

		target.x = 0
		target.y = 0

		self.environment.targets = [target]
		self.environment.check_collisions( member )

		assert target.consumed == 1, "target should have been consumed"

	def testShouldTrackClosest( self ):
		member = self.environment.add_new_member()
		target = self.environment.add_new_target()

		member.x = 100
		member.y = 100

		target.x = 150
		target.y = 150

		self.environment.targets = [target]
		self.environment.check_collisions( member )

		assert member.close_to == target, "target was not tracked"


	def tearDown( self ):
		self.environment = None
