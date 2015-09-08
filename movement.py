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
		self.food 	 = [] 

		self.font 	 = pygame.font.SysFont("monospace", 15)

 
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

		# if no food exists
		if len(self.food) == 0:
			# add some
			self.food.append(Food(len(self.food) + 1))

		if K_UP in self.pressed:
			self.member.move()

		if K_LEFT in self.pressed:
			self.member.angle += .005

		if K_RIGHT in self.pressed:
			self.member.angle -= .005

		self.member.check_bounds()

		for food in self.food:
			if food.rect.colliderect(self.member.rect):
				self.member.food_eaten += 1
				self.food.remove(food)

		pass

	# render function
	def render( self ):

		self.display.fill((255,255,255))
		self.member.draw( self.display )

		for food in self.food:
			food.draw( self.display )

		score = self.font.render("Eaten: " + str(self.member.food_eaten), 1, (0,0,0))
		self.display.blit(score, (10, 10))

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
		self.x 		= random.randint( self.radius, (WIDTH  - self.radius))
		self.y 		= random.randint( self.radius, (HEIGHT - self.radius))

		self.color  = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
		self.stroke = (0,0,0)

		self.name 	= "Creature #" + str(num)
		self.speed  = 1
		self.angle  = 0.45

		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))
		self.food_eaten = 0

		self.debug = False

	def check_bounds( self ):
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT

	def move( self ):
		self.x += deltaX( self.angle, self.speed )
		self.y += deltaY( self.angle, self.speed )
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

	def draw( self, display ):
		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
		dx = self.x + deltaX( self.angle, self.radius )
		dy = self.y + deltaY( self.angle, self.radius )
		pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

		if self.debug:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)


class Food:
	def __init__( self, num ):

		self.size = 10		
		self.x = random.randint(self.size, (WIDTH  - self.size))
		self.y = random.randint(self.size, (HEIGHT - self.size))

		self.color  = (100,170,170)
		self.stroke = (0,0,0)

		self.name   = "Food Pellet #" + str(num)
		self.rect   = pygame.Rect((self.x, self.y), (self.size, self.size)) 

	def draw( self, display ):
		pygame.draw.rect( display, self.color, self.rect, 0)
		pygame.draw.rect( display, self.stroke, self.rect, 1)


def toFixed( number ):
	return int(round(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

 
if __name__ == "__main__" :
	main_window = Main()
	main_window.execute()
