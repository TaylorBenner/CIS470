import unittest, sys
sys.path.append("..")

import configuration


'''Member Class Test Cases'''
class MemberTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(MemberTest("testShouldInitialize"))
		return suite

	def setUp( self ):
		from classes.member import Member
		self.member = Member()

	def testShouldInitialize ( self ):
		lower_limit = configuration.MEMBER_RADIUS
		upper_limit = configuration.WIDTH - configuration.MEMBER_RADIUS

		color_pass  = True
		color_index = None 
		for i,c in enumerate(self.member.color):
			if c < 0 or c > 255:
				color_index = i
				color_pass  = False

		assert (self.member.x >= lower_limit and self.member.x <= upper_limit), 'Initialized X Value is outside the bounds of the view area'
		assert (self.member.y >= lower_limit and self.member.y <= upper_limit), 'Initialized Y Value is outside the bounds of the view area'
		assert (color_pass == True and color_index == None), 'Color in position %i is outside accepted RGB values' % color_index
		assert (self.member.brain is not None), 'Brain was not added to the member class'

	def tearDown( self ):
		self.member = None


runner = unittest.TextTestRunner()
runner.run(MemberTest.buildSuite())
