import random, math, sys
import pygame
from pygame.locals import *

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer

WIDTH  = 700
HEIGHT = 700
DEBUG  = False

class Brain:
	def __init__( self, shape ):
		self.network = buildNetwork(shape[0], shape[1], shape[2], outclass=TanhLayer, bias=True)

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
		self.toxins  = []

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

		self.member.think()

		if len(self.food) == 0:
			for i in range(0,10):
				self.food.append(Food(len(self.food) + 1))

		if len(self.toxins) == 0:
			for i in range(0,10):
				self.toxins.append(Toxin(len(self.toxins) + 1))

		if K_UP in self.pressed:
			self.member.move()

		if K_DOWN in self.pressed:
			self.member.move( -1 )

		if K_LEFT in self.pressed:
			self.member.angle += self.member.rotation_speed

		if K_RIGHT in self.pressed:
			self.member.angle -= self.member.rotation_speed

		self.member.check_bounds()

		for food in self.food:
			if food.rect.colliderect(self.member.rect):
				self.member.food_eaten += 1
				self.food.remove(food)

		for toxin in self.toxins:
			if toxin.rect.colliderect(self.member.rect):
				self.member.damage_taken += 1
				self.toxins.remove(toxin)

		pass

	# render function
	def render( self ):

		self.display.fill((255,255,255))
		self.member.draw( self.display )

		for food in self.food:
			food.draw( self.display )

		for toxin in self.toxins:
			toxin.draw( self.display )

		food = self.font.render("Eaten: " + str(self.member.food_eaten), 1, (0,0,0))
		self.display.blit(food, (10, 10))

		damage = self.font.render("Damage: " + str(self.member.damage_taken), 1, (0,0,0))
		self.display.blit(damage, (10, 30))

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

		# initial position, size, and x,y pos
		self.radius	= 20
		self.x 		= random.randint( self.radius, (WIDTH  - self.radius))
		self.y 		= random.randint( self.radius, (HEIGHT - self.radius))

		# member description
		self.color  = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
		self.stroke = (0,0,0)

		# member name for reporting purposes
		self.name 	= "Creature #" + str(num)

		# member movement speed
		self.speed  = .5

		# rotation amount from tread differential
		self.rotation_speed = 0.01

		# direction member is facing
		self.angle  = 0.45

		self.left_track = 0
		self.right_track = 0

		# member hitbox
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

		# member statistics
		self.food_eaten = 0
		self.damage_taken = 0

		# init brain
		self.brain = Brain([2,5,2])

	def think( self ):
		self.left_track, self.right_track = self.brain.network.activate([self.angle, self.rotation_speed])
		# print "%f  -  %f" %(self.left_track, self.right_track)

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

	# function that calculates new position based on angle, speed, radius, and current position
	def move( self, mod = 1 ):
		self.x += mod * deltaX( self.angle, self.speed )
		self.y += mod * deltaY( self.angle, self.speed )
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

	# function for drawing member and member's hitbox
	def draw( self, display ):
		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
		dx = self.x + deltaX( self.angle, self.radius )
		dy = self.y + deltaY( self.angle, self.radius )
		pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

		if DEBUG:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)


class Food:
	def __init__( self, num ):

		self.radius = 5
		self.x = random.randint(self.radius, (WIDTH  - self.radius))
		self.y = random.randint(self.radius, (HEIGHT - self.radius))

		self.color  = (100,200,100)
		self.stroke = (50,100,50)

		self.name   = "Food Pellet #" + str(num)

		# food hitbox
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

	def draw( self, display ):
		pygame.draw.circle( display, self.color, (self.x, self.y), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (self.x, self.y), self.radius, 1)

		if DEBUG:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)



class Toxin:
	def __init__( self, num ):

		self.radius = 5	
		self.x = random.randint(self.radius, (WIDTH  - self.radius))
		self.y = random.randint(self.radius, (HEIGHT - self.radius))

		self.color  = (200,100,100)
		self.stroke = (100,50,50)

		self.name   = "Toxin Pellet #" + str(num)

		# toxin hitbox
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

	def draw( self, display ):
		pygame.draw.circle( display, self.color, (self.x, self.y), self.radius, 0)
		pygame.draw.circle( display, self.stroke, (self.x, self.y), self.radius, 1)
		
		if DEBUG:
			pygame.draw.rect(display, (200,100,100), self.rect, 1)


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
