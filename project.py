import random, math, sys
import pygame
from pygame.locals import *
from pylygon import Polygon

WIDTH  = 700
HEIGHT = 700
DEBUG  = False

class Main:

	#init main
	def __init__( self ):
		self.running 	    = True
		self.display 		= None
		self.size = self.width, self.height = WIDTH, HEIGHT
 
	# init function
	def init( self ):
		pygame.init()
		self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.display.fill((255,255,255))
		pygame.display.flip()

		self.running = True
		self.population = Population()

		self.clock = pygame.time.Clock()
 
	# events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	# update loop
	def update( self ):

		for member in self.population.members:
			member.left_track = .3
			member.right_track = 1
			member.move()
			member.check_bounds()

		pass

	# render function
	def render( self ):
		self.display.fill((255,255,255))

		for member in self.population.members:
			member.draw( self.display )

		pygame.display.flip()
		pass

	# closure function
	def cleanup( self ):
		pygame.quit()
 
	# main loop
	def execute( self ):

		if self.init() == False:
			self.running = False
 
		while( self.running ):

			self.clock.tick(60)

			for event in pygame.event.get():
				self.events(event)

			self.update()
			self.render()

		self.cleanup()


#
#	Poulation Class
#
class Population:
	def __init__( self ):

		self.population_size = 1
		self.members = [Member( i+1 ) for i in range( self.population_size )]


#
#	Member Class
#
class Member:

	def __init__( self, number ):

		self.name 			= "member " + str(number)
		self.radius 		= 20
		self.color 			= (random.randint(100,200), random.randint(100,200), random.randint(100,200))
		self.stroke 		= (0,0,0)
		self.x 				= (WIDTH / 2) - (self.radius / 2)
		self.y 				= (HEIGHT / 2) - (self.radius / 2)
		self.angle  		= 0.45
		self.left_track  	= 0.0
		self.right_track 	= 0.0
		self.velocity    	= 0.0
		self.rotation_delta = 0.0
		self.food_eaten 	= 0
		self.toxin_eaten 	= 0

		self.view_distance  = (self.radius * 2) * 5
		self.view_width     = 50

		self.rect 			= pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))
		self.triangle 		= Polygon([(self.x, self.y), (self.x + self.view_width, self.y + self.view_distance), (self.x-self.view_width, self.y+self.view_distance)])

	# function that calculates new position based on angle, speed, radius, and current position
	def move( self, mod = 1 ):

		self.rotation_delta = (self.left_track - self.right_track) / self.radius
		self.velocity		= self.left_track + self.right_track

		self.angle += self.rotation_delta
		self.x     += mod * deltaX( self.angle, self.velocity )
		self.y 	   += mod * deltaY( self.angle, self.velocity )
		
		self.rect   = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))
		self.triangle = Polygon([(self.x, self.y), (self.x + self.view_width, self.y + self.view_distance), (self.x-self.view_width, self.y+self.view_distance)])

	# function for drawing member and member's hitbox
	def draw( self, display ):

		dx = self.x + deltaX( self.angle, self.radius )
		dy = self.y + deltaY( self.angle, self.radius )

		# self.triangle.C = (toFixed(self.x), toFixed(self.y))
		# self.triangle.rotate( self.angle )

		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
		pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

		pygame.draw.polygon( display, (255,0,0), self.triangle, 1)

		if DEBUG:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)


	# function to wrap member to opposite side of screen
	def check_bounds( self ):
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT


def toFixed( number ):
	return int(round(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

if __name__ == "__main__" :

	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]

	main_window = Main()
	main_window.execute()