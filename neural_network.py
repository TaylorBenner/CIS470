from pybrain.structure import FeedForwardNetwork
from pybrain.structure import LinearLayer, SigmoidLayer, TanhLayer, SoftmaxLayer
from pybrain.structure import FullConnection

import math, sys, random, pygame
from pygame.locals import *

WIDTH = 900
HEIGHT = 900

class Brain:

	def __init__( self, shape):
		self.shape   = shape
		self.network = self.build()

	def build( self ):
		net = FeedForwardNetwork()

		self.input_layer  = LinearLayer( int(self.shape[0]), name="input")
		self.hidden_layer = SigmoidLayer( int(self.shape[1]), name="hidden")
		self.output_layer = TanhLayer( int(self.shape[2]), name="output")

		net.addInputModule(self.input_layer)
		net.addModule(self.hidden_layer)
		net.addOutputModule(self.output_layer)

		net.addConnection(FullConnection(self.input_layer, self.hidden_layer))
		net.addConnection(FullConnection(self.hidden_layer, self.output_layer))

		net.sortModules()
		return net

	def activate( self, params ):
		if params:
			return self.network.activate( params )


def getSlope(ref,tar):
	ax, ay = ref
	bx, by = tar
	return math.hypot( bx-ax, by-ay )

def getAngle(ref,tar):
	dx   = tar[0] - ref[0]	
	dy   = tar[1] - ref[1]
	rads = math.atan2( dy, dx )
	rads %= 2 * math.pi
	return float(math.degrees(rads))

def toFixed( number ):
	return int(round(number))

def deltaX( angle, number ):
	return math.sin(angle) * number

def deltaY( angle, number ):
	return math.cos(angle) * number

class Environment:

	def __init__( self ):
		self.width 	= WIDTH
		self.height = HEIGHT
		self.center_x = (self.width / 2)
		self.center_y = (self.height / 2)

class Member:
	def __init__(self):

		self.color 			= ( random.randint(50,150), random.randint(50,150), random.randint(50,150) )

		self.radius  		= 20
		self.x 		 		= random.randint(1, WIDTH-1)
		self.y 		 		= random.randint(1, HEIGHT-1)

		self.degrees  		= 0.0
		self.radians  		= (self.degrees * (math.pi/180))

		self.rotation_delta = 0.0
		self.velocity 		= 0.0

		self.brain    		= Brain([4, 10, 2])

	def update( self ):

		tar = [(WIDTH/2),(HEIGHT/2)]

		self.distance  = getSlope([self.x,self.y], tar)
		self.direction = getAngle([self.x,self.y], tar)

		self.left_track, self.right_track = self.brain.activate([
			self.x,
			self.y,
			self.distance,
			self.direction
		])

		self.rotation_delta = (self.left_track - self.right_track) / self.radius
		self.velocity = self.left_track + self.right_track

		self.radians += self.rotation_delta
		if self.radians > (math.pi*2) : self.radians = 0
		elif self.radians < 0 : self.radians = (math.pi*2)

		self.degrees = (self.radians * (180/math.pi))
		if self.degrees > 360: self.degrees = 0
		elif self.degrees < 0: self.degrees = 360

		self.x += deltaX( self.radians, self.velocity )
		self.y += deltaY( self.radians, self.velocity )

		if self.x < 0: self.x = WIDTH
		elif self.x > WIDTH: self.x =  0

		if self.y < 0: self.y = HEIGHT
		elif self.y > HEIGHT: self.y = 0

	def draw( self, display ):

		dx = toFixed(self.x + deltaX( self.radians, self.radius ))
		dy = toFixed(self.y + deltaY( self.radians, self.radius ))

		pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
		pygame.draw.circle( display, (0,0,0), (toFixed(self.x), toFixed(self.y)), self.radius, 1)
		pygame.draw.line( display, (0,0,0), (toFixed(self.x), toFixed(self.y)), (dx, dy), 1)


class Main:

	#init main
	def __init__( self ):
		self.running        = True
		self.display        = None
		self.size = self.width, self.height = WIDTH, HEIGHT
 
	# init function
	def init( self ):
		pygame.init()
		self.display 		= pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
		self.running 		= True
		self.clock 			= pygame.time.Clock()
		self.font  			= pygame.font.SysFont("monospace", 15)
		self.pressed 		= []
		self.members 		= [ Member() for i in range(8) ]

		self.display.fill((255,255,255))
		pygame.display.flip()

	 # events handler
	def events( self, event ):
		if event.type == pygame.QUIT:
			self.running = False			

	# update loop
	def update( self ):

		for member in self.members:
			member.update()
		pass

	# render function
	def render( self ):

		self.display.fill((255,255,255))

		keys = pygame.key.get_pressed()
		if keys[pygame.K_SPACE]:

			start = 5
			for number, member in enumerate(self.members):

				font_color = member.color

				label_lt = self.font.render("LT : " + str(member.left_track), 1, font_color )
				label_rt = self.font.render("RT : " + str(member.right_track), 1, font_color )
				label_de = self.font.render("DEG: " + str(member.degrees), 1, font_color )
				label_ra = self.font.render("RAD: " + str(member.radians), 1, font_color )
				label_ds = self.font.render("DIS: " + str(member.distance), 1, font_color )
				label_dr = self.font.render("DIR: " + str(member.direction), 1, font_color )
				self.display.blit( label_lt, (5, start))
				self.display.blit( label_rt, (5, start + (1*15)))
				self.display.blit( label_de, (5, start + (2*15)))
				self.display.blit( label_ra, (5, start + (3*15)))
				self.display.blit( label_ds, (5, start + (4*15)))
				self.display.blit( label_dr, (5, start + (5*15)))
				start += 105
		for member in self.members:
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
			self.clock.tick(60)
			for event in pygame.event.get():
				self.events(event)
			self.update()
			self.render()
		self.cleanup()


if __name__ == "__main__" :

	args = sys.argv
	if len(args) > 1:
		DEBUG = args[1]

	main_window = Main()
	main_window.execute()