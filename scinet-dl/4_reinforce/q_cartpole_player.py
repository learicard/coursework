#!/usr/bin/env python
#
# Advanced neural networks: reinforcement learning.
# Given at SciNet, 13 November 2017, by Erik Spence.
#
# This file, q_cartpole_player.py, contains code used for lecture 4.
# It is a script which implements a Q-learning strategy to learn the
# 'cartpole' game.
#


#######################################################################


"""
q_cartpole_player.py contains a script which implements a
Q-learning strategy to learn the 'cartpole' game.  This code was
inspired by
https://github.com/finklabs/deepcartpole/blob/master/1_random_cartpole_player.py
and
https://github.com/DanielSlater/PyGamePlayer/blob/master/examples/deep_q_half_pong_player.py

"""

#######################################################################


# This code is inspired by
# https://github.com/finklabs/deepcartpole/blob/master/1_random_cartpole_player.py
# https://github.com/DanielSlater/PyGamePlayer/blob/master/examples/deep_q_half_pong_player.py
# as well as contributions from PyGamePlayer.


#######################################################################

import random

import pygame
from pygame.constants import K_LEFT, K_RIGHT, QUIT, KEYDOWN, KEYUP

import cartpole

import keras.models as km
import keras.layers as kl
import keras.optimizers as ko

import numpy as np
import os


#################################################################


# This code is stolen straight out of the PyGamePlayer package.

def function_intercept(intercepted_func, intercepting_func):
    """Intercepts a method call and calls the supplied intercepting_func
    with the result of it's call and it's arguments.  Stolen wholesale
    from PyGamePlayer.

    - param intercepted_func: The function we are going to intercept
    :param intercepting_func: The function that will get called after
    the intercepted func. It is supplied the return value of the
    intercepted_func as the first argument and it's args and kwargs.
    :return: a function that combines the intercepting and intercepted
    function, should normally be set to the intercepted_functions
    location

    """

    def wrap():
        # call the function we are intercepting and get it's result
        real_results = intercepted_func()

         # call our own function a
        intercepted_results = intercepting_func(real_results) 
        return intercepted_results

    return wrap



##################################################################


class QCartPolePlayer(object):

    def __init__(self):
        """
        Plays CartPole by implementing a NN Q-learning strategy.
        """

        # The future discount rate.        
        self.future_reward_discount = 0.99

        # The number of possible actions (left, right, no move)
        self.num_actions = 3

        # The probabilities of using a random move, instead of one
        # from the NN.
        self.initial_random_prob = 1.0
        self.final_random_prob = 0.05
        self.random_action_prob = self.initial_random_prob

        # Variables for holding information about the previous
        # timestep.
        self.last_score = 0
        self.last_state = cartpole.get_state()
        self.last_action = np.array([1.0, 0.0, 0.0])

        # Variables for dealing with pressed keys.
        self.keys_pressed = []
        self.last_keys_pressed = []

        # Build the neural network.
        self.build_model()

        # Size of the observations collection.
        self.max_obs_length = 10000
        self.observations = []
        
        # Number of observations to gather before starting training of
        # the NN.
        self.min_obs_steps = 3000

        # Number of observations over which to decrease the
        # probability of using a random move, rather than a move from
        # the NN.
        self.explore_steps = 5000

        # The mini-batch size.
        self.mini_batch_size = self.max_obs_length / 8

        # Have we starting training the NN yet?
        self.started_training = False
        

    ####################################    

    
    def build_model(self):

        # This function builds the NN.
        
        # The two inputs.
        input_state = kl.Input(shape = (4,))
        input_actions = kl.Input(shape = (self.num_actions,))

        # Create a NN with three fully connected hidden layers.
        x = kl.Dense(64, activation = 'tanh')(input_state)
        x = kl.Dropout(0.4)(x)
        x = kl.Dense(32, activation = 'tanh')(x)
        x = kl.Dense(16, activation = 'tanh')(x)

        # The regular output layer, for the standard forward pass
        # of the input_state.
        q = kl.Dense(self.num_actions, activation = 'relu')(x)

        # An alternative output layer, used for training.  Here we
        # just multiply the regular output with a 3-element
        # input_action variable and take the sum.
        action_q = kl.Dot(1)([q, input_actions])

        # Create two models, one for each output layer, sharing
        # the same hidden layers.
        self.q_model = km.Model(inputs = input_state, outputs = q)
        self.applied_action_model = km.Model(inputs = [input_state,
                                                       input_actions],
                                             outputs = action_q)

        # We compile the model that is actually used for training.
        self.applied_action_model.compile(optimizer = ko.SGD(lr = 1e-5),
                                          loss = "mean_squared_error",
                                          metrics = ['accuracy'])
        
            
    ####################################


    def choose_next_action(self):

        # This code chooses the next action.  This means either
        # choosing a random action, based on the current probability
        # value, or use the NN to generate the next action.
        
        new_action = np.zeros([self.num_actions])

        # Check to see if we are going to use a random action or not.
        if (random.random() < self.random_action_prob):

            action_index = random.randrange(0, self.num_actions)

        else:

            # If not, run the forward model on self.last_state, which
            # should currently contain the current state.
            readout_t = self.q_model.predict(self.last_state.reshape(1, -1))
            action_index = np.argmax(readout_t)

        new_action[action_index] = 1

        return new_action, action_index
    

    ####################################
        

    def train_model(self):

        # This function trains the NN.

        # Tell us when we train for the first time.
        if (not self.started_training):
            print 'Begin training'
            print 'The score is', cartpole.get_score()
            self.started_training = True

        # Sample a mini-batch of observations on which to train.
        mini_batch = random.sample(self.observations, self.mini_batch_size)

        # Take the mini-batch apart.
        previous_states = np.array([d[0] for d in mini_batch])
        actions = np.array([d[1] for d in mini_batch])
        rewards = np.array([d[2] for d in mini_batch])
        current_states = np.array([d[3] for d in mini_batch])

        # The variable which will hold the data against which we will train.
        agents_expected_reward = []

        # Run the forward pass on the current states, to get
        # Q(a_{t+1}, s_{t+1}).
        agents_reward_per_action = self.q_model.predict(current_states)

        # Now build the training data.
        for i in range(self.mini_batch_size):
            agents_expected_reward.append(rewards[i] +
                                          self.future_reward_discount *
                                          np.max(agents_reward_per_action[i]))

        # Train the NN on the mini-batch.
        loss = self.applied_action_model.train_on_batch([previous_states, actions],
                                                        np.array(agents_expected_reward))

            
    ####################################
                             
        
    def get_keys_pressed(self, reward):

        # This is the real work horse of the code.  Here is where the
        # actual work gets done.
        
        # Get the current state of the game.
        current_state = cartpole.get_state()

        # Append the latest observation to the collection of
        # observations.
        self.observations.append([self.last_state, self.last_action,
                                  reward, current_state])

        # We can't keep all observations.  If there are too many then
        # pop off the oldest.
        if (len(self.observations) > self.max_obs_length):
            self.observations = self.observations[1:]

        # If we have collected enough observations, train.
        if (len(self.observations) > self.min_obs_steps):
            self.train_model()

        # Reset the last state, and get the next action.
        self.last_state = current_state
        self.last_action, action_index = self.choose_next_action()

        # If we are out of the randomness-only regime, reduce the
        # current probability for a random move.
        if ((self.random_action_prob > self.final_random_prob) and
            (len(self.observations) > self.min_obs_steps)):
            self.random_action_prob -= ((self.initial_random_prob -
                                         self.final_random_prob) /
                                        self.explore_steps)

        # Set the move to take, based on the action.
        if action_index == 0:
            action = [K_LEFT]
        elif action_index == 1:
            action = []
        else:
            action = [K_RIGHT]

        return action


    ####################################        
    
    
    def get_reward(self):
        
        # Get the difference in scores between this and the last
        # frame.
        score_change = cartpole.get_score() - self.last_score
        self.last_score = cartpole.get_score()

        return float(score_change)

                             
    ####################################

                             
    def start(self):

        # This code intercepts the regular pygame commands for
        # updating the screen, and getting keyboard inputs, and
        # redirects them to commands in this file.
        
        pygame.display.flip = function_intercept(pygame.display.flip,
                                                 self.on_screen_update)
        pygame.event.get = function_intercept(pygame.event.get,
                                              self.on_event_get)

        # Run the game.
        cartpole.run()

                             
    ####################################

                             
    def on_event_get(self, _):

        # This code is the custom modification of the pygame.event.get
        # command.  It merely processes the current collection of
        # moves.
        
        key_up_events = []

        if len(self.last_keys_pressed) > 0:
            diff_list = list(set(self.last_keys_pressed) -
                             set(self.keys_pressed))
            key_up_events = [pygame.event.Event(KEYUP, {"key": x})
                             for x in diff_list] 

        key_down_events = [pygame.event.Event(KEYDOWN, {"key": x})
                           for x in self.keys_pressed]

        result = key_down_events + key_up_events

        for e in _:
            if e.type == QUIT:
                result.append(e)

        return result

    
    ####################################

    
    def on_screen_update(self, _):

        # This function handles the latest information from the
        # 'player'.
        
        reward  = self.get_reward()

        keys = self.get_keys_pressed(reward)
        self.last_keys_pressed = self.keys_pressed
        self.keys_pressed = keys


##############################################################

# Run it!
if __name__ == '__main__':
    player = QCartPolePlayer()
    player.start()
