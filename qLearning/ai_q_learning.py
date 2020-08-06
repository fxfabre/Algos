#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import pandas
import logging
import numpy as np
from game_grid import GameGrid

ALPHA = 0.5
GAMMA = 1.0
EPSILON = 0.5       # 1 means move at random
REWARD_MOVE = -0.04


class Qlearning:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.info("Init Q learning")
        self._moves_list = ['left', 'right', 'up', 'down']

        self.q_values = pandas.DataFrame()

        self.epsilon = EPSILON
        self.alpha = ALPHA
        self.gamma = GAMMA
        self.reward_move = REWARD_MOVE

    def init(self, file_pattern):
        self.q_values = pandas.DataFrame(index=range(12), columns=self._moves_list)
        if not self.load_states(file_pattern):
            self.q_values.fillna(0, inplace=True)
            self.init_end_states()
        self._logger.info('Init Q learning success : %s', self.q_values.shape)

    def init_end_states(self):
        self.q_values.iloc[3, :] = [ 1] * 4
        self.q_values.iloc[7, :] = [-1] * 4

    def get_move(self, current_grid : GameGrid, current_state):
        available_moves = [move for move in self._moves_list if current_grid.canMove(move, current_state)]

        # self._logger.debug('From state %s : available moves : %s', current_state, available_moves)
        if len(available_moves) == 1:
            # self._logger.debug("One move available : %s", available_moves[0])
            return available_moves[0]       # Don't waste time running AI
        if len(available_moves) == 0:
            # self._logger.debug("No move available.")
            return self._moves_list[0]      # whatever, it wont't move !

        if (self.epsilon > 0) and (random.uniform(0, 1) < self.epsilon):
            self._logger.debug("Randomly choose move")
            return random.choice(available_moves)

        current_q_val = self.q_values.iloc[current_state, :][available_moves]

        max_val = current_q_val.max()
        optimal_moves = current_q_val[current_q_val == max_val].index.tolist()
        self._logger.debug("Optimal moves : %s", optimal_moves)

        if len(optimal_moves) == 0:     # shouldn't happen
            raise Exception("No optimal move in Get move function, %s", max_val)
        elif len(optimal_moves) == 1:
            return optimal_moves[0]
        else:
            return random.choice(optimal_moves)

    def record_state(self, s, s_prime, move):
        a = self._moves_list.index(move)
        q_value_s = self.q_values.iloc[s, a]
        q_value_s_prime = self.q_values.iloc[s_prime, :].max()

        self._logger.debug("Update q values from state %s, value %s", s, self.q_values.iloc[s, a])
        value_to_add = self.alpha * (self.reward_move + self.gamma * q_value_s_prime - q_value_s)
        self.q_values.iloc[s, a] += value_to_add
        self._logger.debug("To state %s, %s, value %s", s_prime, move, self.q_values.iloc[s, a])
        return value_to_add

    def save_states(self, name):
        file_name = name + '_qValues.csv'
        self._logger.info("Saving file to %s", file_name)
        self.q_values.to_csv(file_name, sep='|')

    def load_states(self, name):
        file_name = name + '_qValues.csv'
        current_shape = self.q_values.shape
        if os.path.exists(file_name):
            self._logger.info("Read Q values file from %s", file_name)
            self.q_values = pandas.read_csv(file_name, sep='|', index_col=0)
            self._moves_list = self.q_values.columns.tolist()
            assert current_shape == self.q_values.shape
            return True
        return False

    def state_values(self):
        v = np.zeros(12)
        for s in range(12):
            v[s] = self.q_values.iloc[s, :].max()
        return str(v.reshape([3, 4]))

