import random, math, sys
import pygame
from pygame.locals import *
from pylygon import Polygon

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import FeedForwardNetwork
from pybrain.structure import TanhLayer, LinearLayer, SigmoidLayer
from pybrain.structure import FullConnection

WIDTH  = 700
HEIGHT = 700
DEBUG  = True

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

        self.clock = pygame.time.Clock()
 
    # events handler
    def events( self, event ):
        if event.type == pygame.QUIT:
            self.running = False

    # update loop
    def update( self ):

        if len(self.food) == 0:
            for i in range(50):
                self.food.append(Food(i+1))

        for member in self.population.members:

            member.obj_distance_x = 0
            member.obj_distance_y = 0
            member.obj_type       = 1

            for food in self.food:
                food_seen = food.rect.collidepoly(member.triangle)
                if not food_seen is False:

                    food.color = member.color

                    dist = food.rect.distance(member.rect)
                    member.obj_distance_x = dist[0]
                    member.obj_distance_y = dist[1]
                    member.obj_type       = 1
                else:
                    food.color = (100,200,100)
                    pass

                food_eaten = food.rect.collidepoly(member.rect)
                if not food_eaten is False:
                    member.food_eaten += 1
                    member.energy     += (member.max_energy / 25)
                    self.food.remove( food )
                else:
                    pass

            member.move()
            member.check_bounds()

    # render function
    def render( self ):
        self.display.fill((255,255,255))

        for food in self.food:
            food.draw( self.display )

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

            self.clock.tick(30)

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

        self.population_size = 2
        self.members = [Member( i+1 ) for i in range( self.population_size )]


#
#   Member Class
#
class Member:

    def __init__( self, number ):

        self.name           = "member " + str(number)
        self.radius         = 20
        self.color          = (random.randint(100,200), random.randint(100,200), random.randint(100,200))
        self.stroke         = (0,0,0)
        self.x              = (WIDTH / 2) - (self.radius / 2)
        self.y              = (HEIGHT / 2) - (self.radius / 2)
        self.angle          = 0.0
        self.left_track     = 0.0
        self.right_track    = 0.0
        self.velocity       = 0.0
        self.rotation_delta = 0.0
        self.food_eaten     = 0
        self.toxin_eaten    = 0

        self.obj_distance_x = 0.0
        self.obj_distance_y = 0.0
        self.obj_type       = 0

        self.max_energy     = 1000
        self.energy         = 1000

        self.view_distance  = (self.radius * 2) * 5
        self.view_width     = 50

        shape = [4,10,2]
        self.network = buildNetwork(shape[0], shape[1], shape[2], outclass=TanhLayer, hiddenclass=SigmoidLayer )

        rect_points = [(self.x - self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x + self.radius, self.y + self.radius)]

        self.rect           = Polygon(rect_points)
        self.triangle       = Polygon([(self.x, self.y), (self.x + self.view_width, self.y + self.view_distance), (self.x-self.view_width, self.y+self.view_distance)])

    # function that calculates new position based on angle, speed, radius, and current position
    def move( self, mod = 1 ):

        if self.energy != 0:
            self.left_track, self.right_track = self.network.activate([ self.obj_distance_x, self.obj_distance_y, self.obj_type, self.energy ])

            self.rotation_delta = (self.left_track - self.right_track) / self.radius
            self.velocity       = self.left_track + self.right_track

            self.angle += self.rotation_delta
            self.x     += mod * deltaX( self.angle, self.velocity )
            self.y     += mod * deltaY( self.angle, self.velocity )
            
            rect_points = [(self.x - self.radius, self.y - self.radius),
                (self.x - self.radius, self.y + self.radius),
                (self.x + self.radius, self.y - self.radius),
                (self.x + self.radius, self.y + self.radius)]

            self.rect = Polygon(rect_points)

            dx1 = self.x - deltaX( self.angle - 10, self.view_distance )
            dy1 = self.y - deltaY( self.angle - 10, self.view_distance )

            dx2 = self.x - deltaX( self.angle + 10, self.view_distance )
            dy2 = self.y - deltaY( self.angle + 10, self.view_distance )

            self.triangle = Polygon([(self.x, self.y),(dx1, dy1 ),(dx2, dy2 )])

            self.energy -= 1
        else:
            self.color = (100,100,100)

    # function for drawing member and member's hitbox
    def draw( self, display ):

        bar_height  = 5
        bar_width   = self.radius * 2

        bar_y       = self.y - self.radius - 5
        bar_x       = self.x - self.radius

        bar_rect = Polygon([
            (bar_x, bar_y),
            (bar_x, bar_y - bar_height),
            (bar_x + bar_width, bar_y),
            (bar_x + bar_width, bar_y - bar_height)
        ])

        energy_percent   = (float(self.energy) / float(self.max_energy))
        bar_fill_amount  = (float(self.radius * 2)) * energy_percent

        bar_fill_x = bar_x + bar_fill_amount

        bar_fill = Polygon([
            (bar_x, bar_y),
            (bar_x, (bar_y - bar_height)),
            (toFixed(bar_fill_x), bar_y),
            (toFixed(bar_fill_x), (bar_y - bar_height))
        ])

        dx = self.x + deltaX( self.angle, self.radius )
        dy = self.y + deltaY( self.angle, self.radius )

        #   Draw member
        pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
        pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
        pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

        if self.energy:
            #   Draw energy bar
            pygame.draw.polygon( display, (100,200,100), bar_fill, 0)
            pygame.draw.polygon( display, (0,0,0), bar_rect, 1)


        if DEBUG:
            pygame.draw.polygon( display, (255,0,0), self.triangle, 1)
            pygame.draw.polygon( display, (200,100,100), self.rect, 1)


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
