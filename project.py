import random, math, sys
import pygame, shelve
from pygame.locals import *
from pylygon import Polygon

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import TanhLayer, LinearLayer, SigmoidLayer, FullConnection, FeedForwardNetwork

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.classification import SupervisedDataSet


WIDTH  = 1200
HEIGHT = 900
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
        self.generation = 1

        self.food = []

        self.clock = pygame.time.Clock()
        self.font  = pygame.font.SysFont("arial", 10)
 
    # events handler
    def events( self, event ):
        if event.type == pygame.QUIT:
            self.running = False

    # update loop
    def update( self ):

        if len(self.food) == 0:
            for i in range(100):
                self.food.append(Food(i+1))

        if len(self.population.members) == 0:

            self.food = []
            for i in range(100):
                self.food.append(Food(i+1))

            self.population.populate()
            self.generation += 1

        for member in self.population.members:

            if member.energy == 0:
                self.population.score( member )
                self.population.members.remove( member )
                pass

            member.obj_distance_x = 0
            member.obj_distance_y = 0
            member.obj_type       = 0

            for food in self.food:
                food_seen = food.rect.collidepoly(member.triangle)
                if not food_seen is False:
                    dist = food.rect.distance(member.rect)
                    member.obj_distance_x = dist[0]
                    member.obj_distance_y = dist[1]
                    member.obj_type       = 1

                food_eaten = food.rect.collidepoly(member.rect)
                if not food_eaten is False:
                    member.food_eaten += 1
                    member.energy     += (member.max_energy / 20)

                    member.food_memories.addSample(
                        [member.obj_distance_x, member.obj_distance_y, member.obj_type, member.angle, member.energy],
                        [member.left_track, member.right_track]
                    )
                    member.train()

                    self.food.remove( food )
                else:
                    pass

            member.move()
            member.check_bounds()

    # render function
    def render( self ):

        self.display.fill((255,255,255))

        font_color = (0,0,0)
        label_pop = self.font.render("Generation: " + str(self.generation), 1, font_color )
        self.display.blit( label_pop, (10,10))  

        for food in self.food:
            food.draw( self.display )

        for member in self.population.members:
            member.draw( self.display, self.font )

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

            self.clock.tick(120)

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

        self.overall_max = 0
        self.pop_max     = 0
        self.fittest = []
        self.population_size = 10
        self.populate()

    def score( self, member ):
        if member.food_eaten > self.pop_max:
            self.pop_max = member.food_eaten
            self.fittest = member

            if self.pop_max > self.overall_max:
                self.overall_max = self.pop_max


        print "current member: %i   pop max: %i     overall max: %i" %( member.food_eaten, self.pop_max, self.overall_max )

    def populate( self ):

        mutation_rate = .1
        self.pop_max = 0

        print "next generation"

        if self.fittest:
            members = []
            for i in range(self.population_size):
                if random.random() <= mutation_rate:
                    members.append( Member( len(members) + 1, None, None ))
                else:
                    members.append( Member( len(members) + 1, self.fittest.network, self.fittest.color ))
            self.members = members
            # self.fittest = []
        else:
            self.members = [Member( i+1, None, None ) for i in range( self.population_size )]

#
#   Member Class
#
class Member:

    def __init__( self, number, network, color ):

        self.name           = "member " + str(number)
        self.radius         = 15

        if color:
            self.color = color
        else:
            self.color          = (random.randint(50,255), random.randint(50,255), random.randint(50,255))

        self.stroke         = (0,0,0)

        self.x = random.randint( self.radius, WIDTH - self.radius )
        self.y = random.randint( self.radius, HEIGHT - self.radius )

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
        self.energy         = self.max_energy

        self.view_distance  = (self.radius * 2) * 5
        self.view_width     = 50

        self.food_memories  = SupervisedDataSet(5,2)

        if network == None:
            shape = [5,15,2]
            self.network = buildNetwork(shape[0], shape[1], shape[2], outclass=TanhLayer, bias=True )
        else:
            self.network = network

        rect_points = [(self.x - self.radius, self.y - self.radius),
            (self.x - self.radius, self.y + self.radius),
            (self.x + self.radius, self.y - self.radius),
            (self.x + self.radius, self.y + self.radius)]

        self.rect           = Polygon(rect_points)
        self.triangle       = Polygon([(self.x, self.y), (self.x + self.view_width, self.y + self.view_distance), (self.x-self.view_width, self.y+self.view_distance)])

    # function that calculates new position based on angle, speed, radius, and current position
    def move( self, mod = 1 ):

        if self.energy != 0:

            self.left_track, self.right_track = self.network.activate(
                [self.obj_distance_x, self.obj_distance_y, self.obj_type, self.angle, self.energy ]
            )

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

    # function for drawing member and member's hitbox
    def draw( self, display, font ):

        dx = self.x + deltaX( self.angle, self.radius )
        dy = self.y + deltaY( self.angle, self.radius )

        #   Draw member
        pygame.draw.circle( display, self.color, (toFixed(self.x), toFixed(self.y)), self.radius, 0)
        pygame.draw.circle( display, self.stroke, (toFixed(self.x), toFixed(self.y)), self.radius, 1)
        pygame.draw.line( display, self.stroke, (toFixed(self.x), toFixed(self.y)), (toFixed(dx), toFixed(dy)), 1)

        if self.energy > 0:
            #   Draw energy bar

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

            bar_fill_x = bar_x + (bar_fill_amount + 1)
            if bar_fill_x > (bar_x + bar_width):
                bar_fill_x = bar_x + bar_width

            bar_fill = Polygon([
                (bar_x, bar_y),
                (bar_x, (bar_y - bar_height)),
                (toFixed(bar_fill_x), bar_y),
                (toFixed(bar_fill_x), (bar_y - bar_height))
            ])

            pygame.draw.polygon( display, (100,200,100), bar_fill, 0)
            pygame.draw.polygon( display, (0,0,0), bar_rect, 1)

            if DEBUG:

                pygame.draw.polygon( display, (255,0,0), self.triangle, 1)
                pygame.draw.polygon( display, (200,100,100), self.rect, 1)

                #   Draw information panel
                pane_width  = ((self.radius * 2) * 4) + 15
                pane_height = 100

                pane_x = (self.x - pane_width / 2)
                pane_y = (self.y - 35)

                pane_rect = Polygon([
                    (pane_x, pane_y),
                    (pane_x, (pane_y - pane_height)),
                    (pane_x + pane_width, pane_y),
                    (pane_x + pane_width, (pane_y - pane_height))
                ])

                font_color = (0,0,0)
                label_lt = font.render("LT: " + str(self.left_track), 1, font_color )
                label_rt = font.render("RT: " + str(self.right_track), 1, font_color )
                label_ox = font.render("OX: " + str(self.obj_distance_x), 1, font_color )
                label_oy = font.render("OY: " + str(self.obj_distance_y), 1, font_color )
                label_ot = font.render("OT: " + str(self.obj_type), 1, font_color )
                label_an = font.render("ANGLE: " + str(self.angle), 1, font_color )
                label_en = font.render("ENERGY: " + str(self.energy), 1, font_color )
                label_fo = font.render("FOOD: " + str(self.food_eaten), 1, font_color )

                pygame.draw.polygon( display, (255,255,255), pane_rect, 0)
                pygame.draw.polygon( display, (0,0,0), pane_rect, 1)

                display.blit( label_lt, (pane_x + 5, pane_y - (pane_height - 5)))    
                display.blit( label_rt, (pane_x + 5, pane_y - (pane_height - 15)))
                display.blit( label_ox, (pane_x + 5, pane_y - (pane_height - 35)))
                display.blit( label_oy, (pane_x + 5, pane_y - (pane_height - 45)))
                display.blit( label_ot, (pane_x + 5, pane_y - (pane_height - 55)))
                display.blit( label_an, (pane_x + 5, pane_y - (pane_height - 65)))
                display.blit( label_en, (pane_x + 5, pane_y - (pane_height - 75)))
                display.blit( label_fo, (pane_x + 5, pane_y - (pane_height - 85)))

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

    def train( self ):
        trainer = BackpropTrainer(self.network, self.food_memories)
        trainer.trainEpochs( len(self.food_memories) )


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
