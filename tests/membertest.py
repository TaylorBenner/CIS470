import unittest, sys
sys.path.append("..")

import configuration


'''Member Class Test Cases'''
class MemberTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(MemberTest("testShouldInitializeXCoordinate"))
		suite.addTest(MemberTest("testShouldInitializeYCoordinate"))
		suite.addTest(MemberTest("testShouldInitializeColor"))
		return suite

	def setUp( self ):
		from project import Member
		self.member = Member()

	def testShouldInitializeXCoordinate( self ):
		lower_limit = configuration.MEMBER_RADIUS
		upper_limit = configuration.WIDTH - configuration.MEMBER_RADIUS
		assert (self.member.x >= lower_limit and self.member.x <= upper_limit), 'Initialized X Value is outside the bounds of the view area'

	def testShouldInitializeYCoordinate( self ):
		lower_limit = configuration.MEMBER_RADIUS
		upper_limit = configuration.WIDTH - configuration.MEMBER_RADIUS
		assert (self.member.y >= lower_limit and self.member.y <= upper_limit), 'Initialized Y Value is outside the bounds of the view area'

	def testShouldInitializeColor( self ):
		color_pass  = True
		color_index = None 
		for i,c in enumerate(self.member.color):
			if c < 0 or c > 255:
				color_index = i
				color_pass  = False
		assert color_pass == True and color_index == None, 'Color in position %i is outside accepted RGB values' % color_index

	def tearDown( self ):
		self.member = None


runner = unittest.TextTestRunner()
runner.run(MemberTest.buildSuite())
