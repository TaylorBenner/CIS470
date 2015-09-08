import pygame
import random
import math
from pygame.locals import *

WIDTH  = 700
HEIGHT = 700

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
		self.pressed = []

		self.member  = Member( 1 )

 
	# events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

		if event.type == KEYDOWN:
			if event.key not in self.pressed:
				self.pressed.append( event.key )

		if event.type == KEYUP:
			if event.key in self.pressed:
				self.pressed.remove( event.key )

	# update loop
	def update( self ):

		if K_UP in self.pressed:
			self.member.move_forward()

		if K_LEFT in self.pressed:
			self.member.angle += .01

		if K_RIGHT in self.pressed:
			self.member.angle -= .01

		self.member.check_bounds()

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
			for event in pygame.event.get():
				self.events(event)

			self.update()
			self.render()

		self.cleanup()

class Member:

	def __init__( self, num ):
		self.radius	= 20
		self.x 		= 50
		self.y 		= 50
		self.color  = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
		self.name 	= "Creature #" + str(num)
		self.speed  = 1
		self.angle  = 0.45

	def check_bounds( self ):
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT

	def move_forward( self ):
		self.x += deltaX( self.angle, self.speed )
		self.y += deltaY( self.angle, self.speed )

	def draw( self, display ):

		stroke = (0,0,0)

		# draw main body
		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)

		#draw outline
		pygame.draw.circle( display, stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)

		# draw directional line
		dx = self.x + deltaX( self.angle, self.radius )
		dy = self.y + deltaY( self.angle, self.radius )
		pygame.draw.line( display, stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)


def toFixed( number ):
	return int(round(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

 
if __name__ == "__main__" :
	main_window = Main()
	main_window.execute()
