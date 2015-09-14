import random, math, sys
import pygame
from pygame.locals import *
from pylygon import Polygon

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import TanhLayer, LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection
from pybrain.supervised.trainers import BackpropTrainer

WIDTH  = 700
HEIGHT = 700
DEBUG  = False

class Main:

    #init main
    def __init__( self ):
        self.running        = True
        self.display        = None
        self.size = self.width, self.height = WIDTH, HEIGHT
 
    # init function
    def init( self ):
        pygame.init()
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.display.fill((255,255,255))
        pygame.display.flip()

        self.running = True
        self.population = Population()
        self.food = []
        self.toxins = []

        self.clock = pygame.time.Clock()
 
    # events handler
    def events( self, event ):
        if event.type == pygame.QUIT:
            self.running = False

    # update loop
    def update( self ):

        if len(self.food) == 0:
            for i in range(20):
                self.food.append(Food(i+1))

        if len(self.toxins) == 0:
            for i in range(20):
                self.toxins.append(Toxin(i+1))

        for member in self.population.members:

            member.obj_distance_x = 0.0
            member.obj_distance_y = 0.0

            for food in self.food:
                food_seen = food.rect.collidepoly( member.vision_poly )
                if not food_seen is False:
                    dist = food.rect.distance(member.hit_poly)
                    member.obj_distance_x = dist[0]
                    member.obj_distance_y = dist[1]
                    member.object_type = 1
                    member.food_last_seen = dist

                food_eaten = food.rect.collidepoly( member.hit_poly )
                if not food_eaten is False:
                    # member.network.train([member.left_track, member.right_track],[member.food_last_seen[0]. member.food_last_seen[1]])
                    self.food.remove( food )

            for toxin in self.toxins:
                toxin_seen = toxin.rect.collidepoly( member.vision_poly )
                if not toxin_seen is False:
                    dist = toxin.rect.distance(member.hit_poly)
                    member.obj_distance_x = dist[0]
                    member.obj_distance_y = dist[1]
                    member.object_type = -1
                    member.toxin_last_seen = dist

                toxin_eaten = toxin.rect.collidepoly( member.hit_poly )
                if not toxin_eaten is False:
                    # member.network.train([member.left_track, member.right_track],[member.toxin_last_seen[0]. member.toxin_last_seen[1]])
                    self.toxins.remove( toxin )


            member.move()
            member.check_bounds()

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

            # self.clock.tick(60)

            for event in pygame.event.get():
                self.events(event)

            self.update()
            self.render()

        self.cleanup()


#
#   Poulation Class
#
class Population:
    def __init__( self ):

        self.population_size = 5
        self.members = [Member( i+1 ) for i in range( self.population_size )]


#
#   Member Class
#
class Member:

    def __init__( self, number ):

        self.name           = "member " + str(number)
        self.radius         = 10
        self.color          = (random.randint(100,200), random.randint(100,200), random.randint(100,200))
        self.stroke         = (0,0,0)
        self.x              = (WIDTH / 2) - (self.radius / 2)
        self.y              = (HEIGHT / 2) - (self.radius / 2)
        self.angle          = 0.45
        self.left_track     = 0.0
        self.right_track    = 0.0
        self.velocity       = 0.0
        self.rotation_delta = 0.0
        self.food_eaten     = 0
        self.toxin_eaten    = 0

        self.obj_distance_x = 0.0
        self.obj_distance_y = 0.0
        self.object_type    = 0.0

        self.view_distance  = (self.radius * 2) * 5
        self.view_angle     = 20

        shape = [3,6,2]
        self.network = buildNetwork(shape[0], shape[1], shape[2], outclass=TanhLayer )

        rect_points = [(self.x - self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x + self.radius, self.y + self.radius)]

        self.hit_poly          = Polygon(rect_points)
        self.vision_poly       = self.calculate_vision()


    def move( self, mod = 1 ):

        output = self.network.activate([self.obj_distance_x, self.obj_distance_y, self.object_type])
        # print "%f %f -> %f %f" % (self.obj_distance_x, self.obj_distance_y, output[0], output[1])

        self.left_track, self.right_track = output

        self.rotation_delta = (self.left_track - self.right_track) / self.radius
        self.velocity       = self.left_track + self.right_track

        self.angle += self.rotation_delta
        self.x     += mod * deltaX( self.angle, self.velocity )
        self.y     += mod * deltaY( self.angle, self.velocity )
        
        rect_points = [(self.x - self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x + self.radius, self.y + self.radius)]

        self.hit_poly    = Polygon(rect_points)
        self.vision_poly = self.calculate_vision()

    def calculate_vision( self ):

        dx1 = self.x - deltaX( self.angle - (self.view_angle / 2), self.view_distance )
        dy1 = self.y - deltaY( self.angle - (self.view_angle / 2), self.view_distance )

        dx2 = self.x - deltaX( self.angle + (self.view_angle / 2), self.view_distance )
        dy2 = self.y - deltaY( self.angle + (self.view_angle / 2), self.view_distance )

        return Polygon([(self.x, self.y),(dx1, dy1 ),(dx2, dy2 )])

    # function for drawing member and member's hitbox
    def draw( self, display ):

        dx = self.x + deltaX( self.angle, self.radius )
        dy = self.y + deltaY( self.angle, self.radius )

        pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
        pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
        pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)


        if DEBUG:
            pygame.draw.polygon( display, (255,0,0), self.vision_poly, 1)
            pygame.draw.polygon( display, (200,100,100), self.hit_poly, 1)


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

class Food:
    def __init__( self, num ):

        self.radius = 5
        self.x = random.randint(self.radius, (WIDTH  - self.radius))
        self.y = random.randint(self.radius, (HEIGHT - self.radius))

        self.color  = (100,200,100)
        self.stroke = (50,100,50)

        self.name   = "Food Pellet #" + str(num)

        # food hitbox
        points = [(self.x-self.radius, self.y-self.radius),
            (self.x-self.radius, self.y+self.radius),
            (self.x+self.radius, self.y-self.radius),
            (self.x+self.radius, self.y+self.radius)]

        self.rect = Polygon(points)

    def draw( self, display ):
        pygame.draw.circle( display, self.color, (self.x, self.y), self.radius, 0)
        pygame.draw.circle( display, self.stroke, (self.x, self.y), self.radius, 1)

        if DEBUG:
            pygame.draw.polygon( display, (255,0,0), self.rect, 1)


class Toxin:
    def __init__( self, num ):

        self.radius = 5
        self.x = random.randint(self.radius, (WIDTH  - self.radius))
        self.y = random.randint(self.radius, (HEIGHT - self.radius))

        self.color  = (200,100,100)
        self.stroke = (50,100,50)

        self.name   = "Toxin Pellet #" + str(num)

        # food hitbox
        points = [(self.x-self.radius, self.y-self.radius),
            (self.x-self.radius, self.y+self.radius),
            (self.x+self.radius, self.y-self.radius),
            (self.x+self.radius, self.y+self.radius)]

        self.rect = Polygon(points)

    def draw( self, display ):
        pygame.draw.circle( display, self.color, (self.x, self.y), self.radius, 0)
        pygame.draw.circle( display, self.stroke, (self.x, self.y), self.radius, 1)

        if DEBUG:
            pygame.draw.polygon( display, (255,0,0), self.rect, 1)



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
