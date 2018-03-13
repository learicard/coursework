#!/usr/bin/env python

#
# Advanced neural networks: reinforcement learning.
# Given at SciNet, 13 November 2017, by Erik Spence.
#
# This file, cartpole.py, contains code used for lecture 4.  It is a
# script which implements a version of the 'cartpole' game.
#


#######################################################################


"""
cartpole.py contains a script which implements a version of the
'cartpole' game, using the pygame and Box2D packages.  This code was
heavily inspired by
https://github.com/finklabs/deepcartpole/blob/master/cartpole.py

"""

#######################################################################


# This code is heavily based upon
# https://github.com/finklabs/deepcartpole/blob/master/cartpole.py,
# which is heavily inspired by
# http://www.cs.colostate.edu/~anderson/cs645/index.html/lib/exe/fetch.php?media=notes:cartpole.py.
#
# This is now a dead link, however.


#######################################################################


from Box2D import b2
import math

import numpy as np

import pygame
from pygame.locals import K_RIGHT, K_LEFT, KEYDOWN, KEYUP


#############################################


# These are global variables which are needed to interface with the NN
# training code.
score = 0
state = (0., 0., 0., 0.)


#############################################


# Our cartpole object.
class CartPole(object):


    # The constructor for our object.
    def __init__(self):

        # Holds the score for the game.
        self.score = 0

        # Dimensions for the parts of the game.
        self.trackWidth = 5.0
        self.cartWidth = 0.3
        self.cartHeight = 0.2
        self.cartMass = 0.5
        self.poleMass = 0.05
        self.trackThickness = self.cartHeight
        self.poleLength = self.cartHeight * 4
        self.poleThickness = 0.05

        self.force = 0.2

        # Size of the screen, and Box2D world.
        self.screenSize = (640, 480)
        self.worldSize = (float(self.trackWidth),
                          float(self.trackWidth))

        # Initialize the Box2D world.
        self.world = b2.world(gravity = (0, -10), doSleep = True)

        # Used for dynamics update and for graphics update.
        self.framesPerSecond = 30
        self.velocityIterations = 8
        self.positionIterations = 6

        # Colours and fonts.
        self.trackColor = (100, 100, 100)
        self.arrowColor = (50, 50, 250)
        self.font = pygame.font.SysFont("monospace", 30)
        

        ####################################

        # Now build the world.

        poleCategory = 0x0002

        f = b2.fixtureDef(shape =
                          b2.polygonShape(box = (self.trackWidth / 2,
                                                 self.trackThickness / 2)),
                          friction = 0.001, categoryBits = 0x0001,
                          maskBits = (0xFFFF & ~poleCategory))
        self.track = self.world.CreateStaticBody(position = (0,0), 
                                                 fixtures = f,
                                                 userData={'color':
                                                           self.trackColor})
        self.trackTop = self.world.CreateStaticBody(position =
                                                    (0,
                                                     self.trackThickness +
                                                     self.cartHeight * 1.1),
                                                    fixtures = f)
        
        f = b2.fixtureDef(shape =
                          b2.polygonShape(box = (self.trackThickness / 2,
                                                 self.trackThickness / 2)),
                          friction = 0.001, categoryBits = 0x0001,
                          maskBits = (0xFFFF & ~poleCategory))
        self.wallLeft = self.world.CreateStaticBody(position =
                                                    (-self.trackWidth / 2 +
                                                     self.trackThickness / 2,
                                                     self.trackThickness),
                                                    fixtures = f,
                                                    userData = {'color':
                                                                self.trackColor})
        self.wallRight = self.world.CreateStaticBody(position =
                                                     (self.trackWidth / 2 -
                                                      self.trackThickness / 2,
                                                      self.trackThickness),
                                                     fixtures = f,
                                                     userData = {'color':
                                                                 self.trackColor})
        
        # Make the cart body and fixture.
        f = b2.fixtureDef(shape = b2.polygonShape(box = (self.cartWidth / 2,
                                                         self.cartHeight / 2)),
                          density = self.cartMass, friction = 0.001,
                          restitution = 0.5, categoryBits = 0x0001,
                          maskBits = (0xFFFF & ~poleCategory))
        self.cart = self.world.CreateDynamicBody(position =
                                                 (0,
                                                  self.trackThickness),
                                                 fixtures = f,
                                                 userData = {'color':
                                                             (20, 200, 0)})
        
        # Make the pole body and fixture.  Initially the pole is hanging
        # down, which defines the zero angle.
        f = b2.fixtureDef(shape = b2.polygonShape(box = (self.poleThickness / 2,
                                                         self.poleLength / 2)),
                          density=self.poleMass, categoryBits = poleCategory)
        self.pole = self.world.CreateDynamicBody(position =
                                                 (0,
                                                  self.trackThickness +
                                                  self.cartHeight / 2 +
                                                  self.poleThickness -
                                                  self.poleLength / 2),
                                                 fixtures = f,
                                                 userData = {'color':
                                                             (200, 20, 0)})
        
        # Make the pole-cart joint.
        self.world.CreateRevoluteJoint(bodyA = self.pole, bodyB = self.cart,
                                       anchor = (0, self.trackThickness +
                                                 self.cartHeight / 2 +
                                                 self.poleThickness))

        
    #############################################

    
    def sense(self):
        """The sense function returns the current state of the game."""

        x = self.cart.position[0]
        xdot = self.cart.linearVelocity[0]

        # Because the pole is defined with angle zero being straight down.
        a = self.pole.angle + math.pi
        # convert to range -pi to pi
        if a > 0:
            a = a - 2 * math.pi * math.ceil(a / (2 * math.pi))
        a = math.fmod(a - math.pi, 2 * math.pi) + math.pi
        adot = self.pole.angularVelocity

        return x, xdot, a, adot


    #############################################

    
    def act(self, action):
        """The act function applies the action to the game."""

        self.action = action

        # Calculate the force on the cart.
        f = (self.force * action, 0)

        p = self.cart.GetWorldPoint(localPoint = (0.0, self.cartHeight / 2))

        # Apply the force.
        self.cart.ApplyForce(f, p, True)

        # Take a timestep.
        timeStep = 1.0 / self.framesPerSecond
        self.world.Step(timeStep, self.velocityIterations,
                        self.positionIterations)
        self.world.ClearForces()

        # The pole angle is cummulative.  Reduce it down to the range
        # -2pi < a < 2pi so that we can calculate the score.
        a = self.pole.angle
        while (a > 2 * math.pi): a -= 2 * math.pi
        while (a < -2 * math.pi): a += 2 * math.pi
        
        if ((a > math.pi / 2) and (a < 3 * math.pi / 2)) or \
           ((a < -math.pi / 2) and (a > -3 * math.pi / 2)):
            self.score += 1

            
    #############################################

    # These two functions are needed to update the values of the
    # global variables, so that they can be used by the NN training
    # code.
    def get_score(self):
        return self.score
    
    def get_state(self):
        return self.sense()

    
    #############################################

    
    def initDisplay(self):

        # This code initializes the display, and sets the initial
        # clock.
        self.screen = pygame.display.set_mode(self.screenSize, 0, 32)
        pygame.display.set_caption('Cartpole')
        self.clock = pygame.time.Clock()


    #############################################

    
    def draw(self):
        """The draw function draws the screen and all the parts of the game."""
        
        # Clear screen
        self.screen.fill((250, 250, 250))

        # Draw circle for the joint. Do so before the cart, so that
        # the joint will appear as a half circle.
        jointCoord = self.w2p(self.cart.GetWorldPoint((0,
                                                       self.cartHeight / 2)))
        junk, radius = self.dw2dp((0, 2 * self.poleThickness))
        pygame.draw.circle(self.screen, self.cart.userData['color'],
                           jointCoord, radius, 0)

        # Draw the other bodies
        for body in (self.track, self.wallLeft, self.wallRight,
                     self.cart, self.pole):
            for fixture in body.fixtures:
                shape = fixture.shape
                # Assume polygon shapes!!!
                vertices = [self.w2p((body.transform * v))
                            for v in shape.vertices]
                pygame.draw.polygon(self.screen, body.userData['color'],
                                    vertices)

        # Draw the arrow showing the force.    
        if self.action != 0:
            cartCenter = self.w2p(self.cart.GetWorldPoint((0, 0)))
            arrowEnd = (cartCenter[0] + self.action * 20, cartCenter[1])
            pygame.draw.line(self.screen, self.arrowColor,
                             cartCenter, arrowEnd, 3)
            pygame.draw.line(self.screen, self.arrowColor, arrowEnd,
                             (arrowEnd[0]-self.action * 5, arrowEnd[1] + 5), 3)
            pygame.draw.line(self.screen, self.arrowColor, arrowEnd,
                             (arrowEnd[0]-self.action * 5, arrowEnd[1] - 5), 3)


        # Add the score and time text.
        score_label = self.font.render("Score: " + str(self.score),
                                       1, (0, 0, 255))
        self.screen.blit(score_label, (10, 10))

        time_label = self.font.render("Time: " +
                                      str(round(pygame.time.get_ticks() /
                                                1000., 1)), 1, (0, 0, 255))
        self.screen.blit(time_label, (10, 440))
        
        # Update the display.
        pygame.display.flip()

        # Update the internal clock.
        self.clock.tick(self.framesPerSecond)

        
    #############################################

    
    # These are helper functions used to update the display.

    def w2p(self,(x,y)):
        """ Convert world coordinates to screen (pixel) coordinates"""
        return (int(0.5 + (x + self.worldSize[0] / 2) /
                    self.worldSize[0] * self.screenSize[0]),
                int(0.5 +
                    self.screenSize[1] - (y + self.worldSize[1] / 2) /
                    self.worldSize[1] * self.screenSize[1]))


    def dw2dp(self,(dx,dy)):
        """ Convert delta world coordinates to delta screen (pixel) coordinates"""
        return (int(0.5+dx/self.worldSize[0] * self.screenSize[0]),
                int(0.5+dy/self.worldSize[1] * self.screenSize[1]))

    
#####################################################################


def run():
    """The run function runs the cartpole game."""

    # Declare the global variables.  These are needed to interface
    # with the NN training code.
    global score
    global state

    # Initialize the pygame.
    pygame.init()
    
    # Initialize the cartpole object, and initialize the screen.
    cartpole = CartPole()
    cartpole.initDisplay()

    # Start the event loop.
    action = 0
    running = True
    reps = 0
    while running:
        
        reps += 1

        # Set action to -1, 1, or 0 by pressing left or right arrow or
        # nothing.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    action = 1
                elif event.key == K_LEFT:
                    action = -1
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_LEFT:
                    action = 0

        # Apply action to cartpole simulation
        cartpole.act(action)

        # Redraw cartpole in new state
        cartpole.draw()

        # Update the global variables.
        score = cartpole.get_score()
        state = cartpole.get_state()

    # If we're done, quit.
    pygame.quit()

    
#####################################################################

# Functions needed to interface the global variables with the NN
# training code.
def get_state():
    return np.array(state).reshape(-1)


def get_score():
    return score


#####################################################################

# Play the game by hand, if you like.
if __name__ == "__main__":
    run()
