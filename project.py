from classes.helper 	 import Helper
from classes.environment import Environment
from classes.database    import Database

import config, sys, pygame, random

class Main:
	def __init__( self ):
		pygame.init()
		self.running        = True
		self.will_render    = True
		self.display        = pygame.display.set_mode(
								[config.window_width, config.window_height], 
								pygame.HWSURFACE | pygame.DOUBLEBUF
							  )
		self.clock          = pygame.time.Clock()
		self.font           = pygame.font.SysFont("monospace", 12)
		self.environment    = Environment()
		self.database 		= Database()
		self.steps			= 0
		self.sim_start		= pygame.time.get_ticks()

		self.display.fill((255,255,255))
		pygame.display.flip()

	def execute( self ):
		while( self.running ):

			if not self.will_render:
				self.clock.tick(60)

			for event in pygame.event.get():
				self.events(event)

			keys = pygame.key.get_pressed() 
			if keys[pygame.K_SPACE]:
				self.will_render = False
			else:
				self.will_render = True

			self.update()
			self.render()
			self.steps += 1

		self.cleanup()

	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False

	def update( self ):

		self.environment.update_all()
		if self.environment.has_active == False:

			self.environment.perform_scoring()

			self.database.save_population( self.environment.members )

			self.environment.perform_selection()
			self.environment.perform_crossover()
			self.environment.perform_mutation()

			self.environment.generations += 1

	def render( self ):

		self.display.fill((255,255,255))

		for obj in self.environment.get_objects():
			obj.draw( self.display )

		pygame.draw.rect( self.display, [150,150,150], [config.viewport_width, 0, config.window_width - config.viewport_width, config.viewport_height])
		pygame.draw.aaline( self.display, [0,0,0], [config.viewport_width, 0], [config.viewport_width, config.viewport_height], 1)

		labels = [
			self.font.render("Mutation Rate: " + str(config.mutation_rate * 100) + '%', 1, [0,0,0] ),
			self.font.render("Selection Rate: " + str(config.selection_rate * 100) + '%', 1, [0,0,0] ),
			self.font.render("Simulation Steps: " + str(self.steps), 1, [0,0,0] ),
			self.font.render("Generation: " + str(self.environment.generations), 1, [0,0,0] ),
			self.font.render("Members Alive: " + str(self.environment.remaining), 1, [0,0,0] ),
			self.font.render("Overall Best:", 1, [0,0,0] )
		]

		if self.environment.overall_best != None:
			labels.append(self.font.render("Score   : " + str(self.environment.overall_best.score), 1, [0,0,0] ))
			labels.append(self.font.render("Neurons : " + str(len(self.environment.overall_best.brain.all_neurons())), 1, [0,0,0] ))
			labels.append(self.font.render("Food    : " + str(self.environment.overall_best.food), 1, [0,0,0] ))

		padding_increment = 10

		for ind, label in enumerate(labels):
			self.display.blit( label, (config.viewport_width + config.panel_padding, padding_increment))
			if ind == 4 or ind == 1: padding_increment += 20
			else: padding_increment += 10

		pygame.display.flip()

	def cleanup( self ):
		self.database.graph_optimization()
		pygame.quit()
		

if __name__ == "__main__" :
	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]
	main_window = Main()
	main_window.execute()
