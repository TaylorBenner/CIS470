import pygame
import random, math
from pygame.locals import *
from pylygon import Polygon

from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, TanhLayer, FullConnection

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
		self.clock   = pygame.time.Clock()
		self.member  = Member( 1 )

 
	# events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	# update loop
	def update( self ):
		#self.member.move()
		pass

	# render function
	def render( self ):
		self.display.fill((255,255,255))

		self.member.draw( self.display )

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


class Member:

	def __init__( self, num ):

		self.radius = 15
		self.x 		= (WIDTH/2) - (self.radius/2)
		self.y 		= (HEIGHT/2) - (self.radius/2)

		self.angle       = 0.0
		self.left_track  = 0.0
		self.right_track = 0.0
		self.speed 		 = 0.0

		self.color 	= (random.randint(100,255), random.randint(100,255), random.randint(100,255))
		self.stroke = (0,0,0)

		self.name 	= "Creature #" + str(num)

		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))
		self.brain = Brain()

	def move( self, mod = 1 ):

		self.left_track, self.right_track = self.brain.network.activate( [self.angle, self.speed] )

		self.angle += (self.left_track - self.right_track) / self.radius
		self.speed = (self.left_track + self.right_track) / 2

		self.x += mod * deltaX( self.angle, self.speed )
		self.y += mod * deltaY( self.angle, self.speed )

	def check_bounds( self ):
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT

	def draw( self, display ):
		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)

		dx = self.x + deltaX( self.angle, self.radius )
		dy = self.y + deltaY( self.angle, self.radius )

		pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

		focal_length  = (self.radius * 2) * 6
		field_of_view = 90
		vision 		  = Polygon([(self.x, self.y), (110, 0), (110, 70)])

		pygame.draw.rect(
			display,
			self.stroke,
			vision,
			1
		)

		if DEBUG:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)

class Brain:

	def __init__(self):
		self.network = self.build()

	def build( self ):
		net = FeedForwardNetwork()

		net.addInputModule( LinearLayer( 2, name="in"))
		net.addModule( SigmoidLayer( 5, name="hidden" ))
		net.addOutputModule( TanhLayer( 2, name="output" ))

		net.addConnection( FullConnection( net['in'], net['hidden'] ))
		net.addConnection( FullConnection( net['hidden'], net['output'] ))

		net.sortModules()
		return net

 

def toFixed( number ):
	return int(round(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

if __name__ == "__main__" :
	main_window = Main()
	main_window.execute()
