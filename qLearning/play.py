#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import logging
import traceback

from ai_q_learning import Qlearning
from game_grid import GameGrid


class PlayGame:

    def __init__(self):
        self._logger = self.init_logger()

        self._ai = Qlearning()
        self._ai.init()

    def Simulate(self):
        file_pattern = 'test'
        self._ai.load_states(file_pattern)

        try:
            nb_iter = 0
            while True:
                nb_iter += 1
                self.playGame()

                if nb_iter % 500000 == 0:
                    self._ai.save_states(file_pattern + '_' + str(nb_iter / 1e6))
                if nb_iter % 50 == 0:
                    print(nb_iter)
                    print(self._ai.state_values())
                self._logger.debug('')
                if self._logger.isEnabledFor(logging.DEBUG):
                    raise Exception("end game")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
        self._ai.save_states(file_pattern)

    def playGame(self):
        current_grid = GameGrid()
        current_state = 8

        while not current_grid.is_game_over(current_state):
            old_state = current_state
            next_move = self._ai.get_move(current_grid, current_state)
            current_state = current_grid.go_to(next_move, current_state)
            self._logger.debug("Moving %s from %s to %s", next_move, old_state, current_state)
            self._ai.record_state(old_state, current_state, next_move)
            self._logger.debug('\n    %s', self._ai.q_values)

    def init_logger(self):
        log_filename = os.path.join('/tmp', "2048_" + str(int(time.time())) + ".log")
        log_format = '%(asctime)-15s %(message)s'
        logging.basicConfig(format=log_format, level=logging.INFO)
        return logging.getLogger(__name__)


if __name__ == '__main__':
    game = PlayGame()
    game.Simulate()
