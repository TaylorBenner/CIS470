import pygame
import random
from pygame.locals import *

POP_SIZE 	  = 50
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

        self.population = population()
        self.population.show_members()

 
    # events handler
    def events( self, event ):

        if event.type == pygame.QUIT:
            self.running = False

    # update loop
    def update( self ):
    	for member in self.population.members:

    		if member.direction == "up":
    			member.y -= member.speed
    		elif member.direction == "down":
    			member.y += member.speed
    		elif member.direction == "left":
    			member.x -= member.speed
    		elif member.direction == "right":
    			member.x += member.speed

    		member.check_bounds()

        pass

    # render function
    def render( self ):

    	self.display.fill((255,255,255))
    	for member in self.population.members:
    		pygame.draw.circle( 
    			self.display, 
    			member.color, 
    			(member.x, member.y),
    			member.size,
    			0)

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
			print "%s %i %i %s" % (member.name, member.x, member.y, member.direction)


class member:

	def __init__( self, num ):

		self.direction = random.choice(["up","down","left","right"])
		self.size 	= 10
		self.x 		= random.randint( self.size, (WIDTH - self.size))
		self.y 		= random.randint( self.size, (HEIGHT - self.size))
		self.color 	= (random.randint(0,255), random.randint(0,255), random.randint(0,255))
		self.name 	= "Creature #" + str(num)
		self.speed  = 1

	def check_bounds( self ):
		
		if self.x > WIDTH:
			self.x = 0
		elif self.x < 0:
			self.x = WIDTH

		if self.y > HEIGHT:
			self.y = 0
		elif self.y < 0:
			self.y = HEIGHT

 
if __name__ == "__main__" :
    main_window = main()
    main_window.execute()
