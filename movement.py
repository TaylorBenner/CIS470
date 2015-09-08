import pygame
import random
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
			self.member.y -= 1

		if K_DOWN in self.pressed:
			self.member.y += 1

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
		self.x 		= (WIDTH / 2) - self.radius
		self.y 		= (HEIGHT / 2) - self.radius
		self.color  = (0,0,0)
		self.name 	= "Creature #" + str(num)

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
		pygame.draw.circle( 
			display, 
			self.color, 
			(self.x, self.y),
			self.radius,
			1)

		pygame.draw.line(
			display,
			(0,0,0),
			(self.x, self.y),
			(self.x, (self.y - self.radius)),
			1)

 
if __name__ == "__main__" :
	main_window = Main()
	main_window.execute()
