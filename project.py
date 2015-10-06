from classes.helper import Helper
from classes.environment import Environment

import configuration, sys, pygame, random

class Main:
	def __init__( self ):
		pygame.init()
		self.running     = True
		self.display     = pygame.display.set_mode([configuration.WIDTH, configuration.HEIGHT], pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.clock       = pygame.time.Clock()
		self.font        = pygame.font.SysFont("monospace", 12)
		self.environment = Environment()
		self.display.fill((255,255,255))
		pygame.display.flip()


	def execute( self ):
		while( self.running ):
			for event in pygame.event.get():
				self.events(event)
			self.update()
			self.render()
		self.cleanup()

	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	def update( self ):

		for obj in self.environment.members:
			if obj: obj.update( self.environment.members )

		self.environment.update_targets()


	def render( self ):
		self.display.fill((255,255,255))

		for obj in self.environment.get_objects():
			if obj: obj.draw( self.display )

		pygame.display.flip()

	def cleanup( self ):
		pass



class Database:
	filename = configuration.DATABASE_NAME
	pass


if __name__ == "__main__" :
	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]
	main_window = Main()
	main_window.execute()
