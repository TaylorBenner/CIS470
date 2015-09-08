import pygame
import random
from pygame.locals import *

POP_SIZE 	  = 1
WIDTH  		  = 700
HEIGHT 		  = 700

class main:

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

		self.population = population()
		self.population.show_members()

 
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
		for member in self.population.members:

			member.left_track 	= 0
			member.right_track 	= 0

			if K_LEFT in self.pressed:
				member.left_track 	= 0
				member.right_track 	= 1

			if K_RIGHT in self.pressed:
				member.left_track 	= 1
				member.right_track 	= 0

			member.update_rotation()
			member.check_bounds()

		pass

	# render function
	def render( self ):

		self.display.fill((255,255,255))
		for member in self.population.members:
			member.draw_member( self.display )

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

class population:

	def __init__( self ):
		self.generation = 0
		self.members = []

		for i in range( POP_SIZE ):
			new_member = member( i+1 )
			self.members.append( new_member )

	def show_members( self ):
		for member in self.members:
			print "%s %i %i" % (member.name, member.x, member.y)


class member:

	def __init__( self, num ):
		self.size 	= 10
		self.x 		= random.randint( self.size, (WIDTH - self.size))
		self.y 		= random.randint( self.size, (HEIGHT - self.size))
		# self.color 	= (random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.color  = (160,160,160)
		self.name 	= "Creature #" + str(num)

		self.left_speed  = 1
		self.right_speed  = 1

		self.left_track = 0
		self.right_track = 0

		self.rotational_velocity = 0.0
		self.rotational_radian = 0.0

	def check_bounds( self ):
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT

	def update_rotation( self ):
		self.rotational_velocity = (self.left_track + self.right_track)
		self.rotational_radian += self.rotational_velocity
		
		if self.rotational_radian > 360.0:
			self.rotational_radian = 0
		elif self.rotational_radian < 0:
			self.rotational_radian = 360


		print self.rotational_radian

	def draw_member( self, display ):
		# draw main body to display
		pygame.draw.circle( 
			display, 
			self.color, 
			(self.x, self.y),
			self.size,
			0)

		# draw line indicating direction
		# pygame.draw.line(
		# 	display,
		# 	(0,0,0),
		# 	(self.x, self.y),
		# 	(self.x, (self.y - self.size)),
		# 	(self.size / 10))

 
if __name__ == "__main__" :
	main_window = main()
	main_window.execute()
