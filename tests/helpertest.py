import unittest, sys, random
sys.path.append("..")
import config


'''Helper Class Test Cases'''
class HelperTest( unittest.TestCase ):
	@staticmethod
	def buildSuite():
		suite = unittest.TestSuite()
		suite.addTest(HelperTest("testShouldReturnInt"))
		suite.addTest(HelperTest("testShouldReturnDeltaX"))
		suite.addTest(HelperTest("testShouldReturnDeltaY"))
		suite.addTest(HelperTest("testShouldReturnRandomColor"))
		suite.addTest(HelperTest("testShouldCollide"))
		suite.addTest(HelperTest("testShouldNotCollide"))
		suite.addTest(HelperTest("testShouldBeClose"))
		suite.addTest(HelperTest("testShouldNotBeClose"))
		return suite

	def setUp( self ):
		from classes.helper import Helper	
		self.Helper = Helper()

	def testShouldReturnInt( self ):
		a = float(1.5)
		b = self.Helper.fixed(a)
		assert type(b) == int, "int was not returned"

	def testShouldReturnDeltaX( self ):
		a = 100
		b = 2.5
		c = self.Helper.delta_x(a,b)
		self.assertAlmostEqual(c,-1.26591410277)

	def testShouldReturnDeltaY( self ):
		a = 100
		b = 2.5
		c = self.Helper.delta_y(a,b)
		self.assertAlmostEqual(c,2.15579718072)

	def testShouldReturnRandomColor( self ):
		color = self.Helper.random_color()
		for c in color:
			self.assertGreaterEqual(c, config.color_min)
			self.assertLessEqual(c, config.color_max)

	def testShouldCollide( self ):
		from classes.target import Target
		t1 = Target()
		t2 = Target()
		t1.x = 100
		t1.y = 100
		t2.x = 100
		t2.y = 100
		c = self.Helper.is_collided(t1,t2)
		assert c == True, "collision not detected"

	def testShouldNotCollide( self ):
		from classes.target import Target
		t1 = Target()
		t2 = Target()
		t1.x = 200
		t1.y = 200
		t2.x = 100
		t2.y = 100
		c = self.Helper.is_collided(t1,t2)
		assert c == False, "collision detected"

	def testShouldBeClose( self ):
		from classes.target import Target
		t1 = Target()
		t2 = Target()
		t1.x = 150
		t1.y = 150
		t2.x = 100
		t2.y = 100
		c = self.Helper.is_close(t1,t2)
		assert c == True, "objects are not close"

	def testShouldNotBeClose( self ):
		from classes.target import Target
		t1 = Target()
		t2 = Target()
		t1.x = 550
		t1.y = 550
		t2.x = 100
		t2.y = 100
		c = self.Helper.is_close(t1,t2)
		assert c == False, "objects close"

	def tearDown( self ):
		self.member = None



