import random, math, sys
import pygame
from pygame.locals import *

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import TanhLayer, LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

POP_SIZE = 10
WIDTH  	 = 700
HEIGHT 	 = 700
DEBUG  	 = False

class Brain:
	def __init__( self, shape ):
		self.network = buildNetwork(shape[0], shape[1], shape[2], outclass=TanhLayer )

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

		self.population = Population()
		self.food 	 	= []
		self.toxins  	= []

		self.population.show_members()
		self.next_generation_event =  pygame.USEREVENT + 1
		pygame.time.set_timer( self.next_generation_event, 10000 )
 
	# events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

		if event.type == self.next_generation_event:
			self.food = []
			self.toxis = []
			self.population.next_generation()


	# update loop
	def update( self ):

		if len(self.food) == 0:
			for i in range(0,20):
				self.food.append(Food(len(self.food) + 1))

		if len(self.toxins) == 0:
			for i in range(0,20):
				self.toxins.append(Toxin(len(self.toxins) + 1))


		for member in self.population.members:
			member.think()
			member.move()
			member.check_bounds()

			for food in self.food:
				if food.rect.colliderect( member.rect ):
					member.food_eaten += 1
					self.food.remove(food)

			for toxin in self.toxins:
				if toxin.rect.colliderect( member.rect ):
					member.damage_taken += 1
					self.toxins.remove(toxin)

		pass

	# render function
	def render( self ):

		self.display.fill((255,255,255))

		for food in self.food:
			food.draw( self.display )

		for toxin in self.toxins:
			toxin.draw( self.display )

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
			for event in pygame.event.get():
				self.events(event)

			self.update()
			self.render()

		self.cleanup()


class Population:
	def __init__( self ):
		self.generation = 0
		self.members = []

		for i in range( POP_SIZE ):
			new_member = Member( i+1 )
			self.members.append( new_member )

	def show_members( self ):
		for member in self.members:
			print "%s %i %i" % (member.name, member.x, member.y)

	def next_generation( self ):
		self.members.sort(key=lambda x: (x.food_eaten - x.damage_taken), reverse=True)
		parents = self.members[:2]
		il = [parent.brain.network['in'] for parent in parents]
		hl = [parent.brain.network['hidden0'] for parent in parents]
		ol = [parent.brain.network['out'] for parent in parents]

		self.members = []
		for i in range(POP_SIZE):
			new_member = Member( i+1 )
			nil = random.choice(il)
			hil = random.choice(hl)
			oil = random.choice(ol)
			ith = FullConnection(nil, hil)
			hto = FullConnection(hil, oil)
			new_member.brain.network = FeedForwardNetwork()
			new_member.brain.network.addInputModule( nil )
			new_member.brain.network.addModule( hil )
			new_member.brain.network.addOutputModule( oil )
			new_member.brain.network.addConnection(ith)
			new_member.brain.network.addConnection(hto)
			new_member.brain.network.sortModules()
			self.members.append( new_member )
			

class Member:
	def __init__( self, num ):

		# initial position, size, and x,y pos
		self.radius	= 10
		self.x = (HEIGHT / 2) - (self.radius / 2)
		self.y = (WIDTH / 2) - (self.radius / 2)
		# self.x 		= random.randint( self.radius, (WIDTH  - self.radius))
		# self.y 		= random.randint( self.radius, (HEIGHT - self.radius))

		# member description
		self.color  = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
		self.stroke = (0,0,0)

		# member name for reporting purposes
		self.name 	= "Creature #" + str(num)

		# direction member is facing
		self.angle  		= 0.0
		self.left_track  	= 0.0
		self.right_track 	= 0.0
		self.velocity    	= 0.0
		self.rotation_delta = 0.0

		# member hitbox
		self.rect = pygame.Rect((self.x-self.radius, self.y-self.radius),(self.radius*2, self.radius*2))

		# member statistics
		self.food_eaten = 0
		self.damage_taken = 0

		# init brain
		self.brain = Brain([2,5,2])

	def think( self ):
		self.left_track, self.right_track = self.brain.network.activate([self.food_eaten, self.damage_taken])
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

		self.rotation_delta = (self.left_track - self.right_track) / self.radius
		self.velocity		= self.left_track + self.right_track
		self.angle += self.rotation_delta
		self.x += mod * deltaX( self.angle, self.velocity )
		self.y += mod * deltaY( self.angle, self.velocity )
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
