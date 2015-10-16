import unittest, sys
sys.path.append("..")

import config


'''Member Class Test Cases'''
class MemberTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(MemberTest("testShouldInitialize"))
		suite.addTest(MemberTest("testShouldReturnParams"))
		suite.addTest(MemberTest("testShouldActivateNetwork"))
		suite.addTest(MemberTest("testMemberShouldStarve"))
		suite.addTest(MemberTest("testMemberShouldOvereat"))
		suite.addTest(MemberTest("testMemberShouldBeAlive"))
		suite.addTest(MemberTest("testMemberShouldRotate"))
		suite.addTest(MemberTest("testShouldCalculateDistanceToClosest"))
		suite.addTest(MemberTest("testShouldCalculateRelationToClosest"))
		return suite

	def setUp( self ):
		from classes.member import Member
		self.member = Member()

	def testShouldInitialize( self ):
		color_pass  = True
		color_index = None 
		for i,c in enumerate(self.member.color):
			if c < 0 or c > 255:
				color_index = i
				color_pass  = False
		assert (color_pass == True and color_index == None), 'Color in position %i is outside accepted RGB values' % color_index
		assert (self.member.brain is not None), 'Brain was not added to the member class'

	def testShouldReturnParams( self ):
		self.member.distance = 100
		self.member.relation = 12
		self.member.energy = 500
		energy 		= 1 - ( 1 / float(self.member.energy))
		distance 	= 1 / float(self.member.distance)
		relation 	= 1 / float(self.member.relation)
		params = self.member.get_params()
		self.assertAlmostEqual(params[0], energy), "energy input is not correct"
		self.assertAlmostEqual(params[1], distance), "distance input is not correct"
		self.assertAlmostEqual(params[2], relation), "relation input is not correct"

	def testShouldActivateNetwork( self ):
		self.member.distance = 100
		self.member.relation = 12
		self.member.energy = 500
		self.member.process_network()
		a,b = [self.member.left_track, self.member.right_track]
		self.assertGreaterEqual(a, -1)
		self.assertLessEqual(a, 1)
		self.assertGreaterEqual(b, -1)
		self.assertLessEqual(b, 1)

	def testMemberShouldStarve( self ):
		self.member.alive = True
		self.member.energy = 0
		self.member.update_member_state()
		assert self.member.alive == False, "member should die"

	def testMemberShouldOvereat( self ):
		self.member.alive = True
		self.member.energy = 5001
		self.member.update_member_state()
		assert self.member.alive == False, "member should die"

	def testMemberShouldBeAlive( self ):
		self.member.alive = False
		self.member.energy = 1000
		self.member.update_member_state()
		assert self.member.alive == True, "member should be alive"

	def testMemberShouldRotate( self ):
		before = self.member.rotation
		self.member.update_member_state()
		after  = self.member.rotation
		assert before != after, "rotation was not updated"

	def testShouldCalculateDistanceToClosest( self ):
		from classes.target import Target
		from classes.helper import Helper

		helper = Helper()
		target = Target()

		target.x = 100
		target.y = 100

		self.member.x = 150
		self.member.y = 100
		assert int(helper.get_distance(self.member,target)) == 50, "distance was not calculated correctly"

	def testShouldCalculateRelationToClosest( self ):
		from classes.target import Target
		from classes.helper import Helper

		helper = Helper()
		target = Target()

		target.x = 100
		target.y = 100

		self.member.x = 150
		self.member.y = 100

		rad = helper.get_relation_to( self.member, target )
		self.assertAlmostEqual(rad, 1.5707963267948966)


	def tearDown( self ):
		self.member = None


runner = unittest.TextTestRunner()
runner.run(MemberTest.buildSuite())
