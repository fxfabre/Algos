#!/usr/bin/python3
# -*- coding: utf-8 -*-


class GameGrid:

    ###############
    # Moves
    ###############
    def go_to(self, direction, current_state):
        direction = direction.lower()
        if direction == 'left':
            return self.moveLeft(current_state)
        elif direction == 'right':
            return self.moveRight(current_state)
        elif direction == 'up':
            return self.moveUp(current_state)
        elif direction == 'down':
            return self.moveDown(current_state)
        return False

    def moveLeft(self, current_state):
        possible_moves = {
            0 : 0,
            1 : 0,
            2 : 1,
            3 : 3,
            4 : 4,
            6 : 6,
            7 : 7,
            8 : 8,
            9 : 8,
            10 : 9,
            11 : 10
        }
        if current_state in possible_moves:
            return possible_moves.get(current_state)
        return ''

    def moveRight(self, current_state):
        possible_moves = {
            0 : 1,
            1 : 2,
            2 : 3,
            3 : 3,
            4 : 4,
            6 : 7,
            7 : 7,
            8 : 9,
            9 : 10,
            10 : 11,
            11 : 11
        }
        if current_state in possible_moves:
            return possible_moves.get(current_state)
        return ''

    def moveUp(self, current_state):
        possible_moves = {
            0 : 0,
            1 : 1,
            2 : 2,
            3 : 3,
            4 : 0,
            6 : 2,
            7 : 7,
            8 : 4,
            9 : 9,
            10 : 6,
            11 : 7
        }
        if current_state in possible_moves:
            return possible_moves.get(current_state)
        return ''

    def moveDown(self, current_state):
        possible_moves = {
            0 : 4,
            1 : 1,
            2 : 6,
            3 : 3,
            4 : 8,
            6 : 10,
            7 : 7,
            8 : 8,
            9 : 9,
            10 : 10,
            11 : 11
        }
        if current_state in possible_moves:
            return possible_moves.get(current_state)
        return ''

    ###############
    # Can move
    ###############
    def canMove(self, direction, current_state):
        if direction == 'left':
            return self.canMoveLeft(current_state)
        if direction == 'right':
            return self.canMoveRight(current_state)
        if direction == 'up':
            return self.canMoveUp(current_state)
        if direction == 'down':
            return self.canMoveDown(current_state)
        raise Exception("Unknown direction " + str(direction))

    def canMoveLeft(self, current_state):
        return self.moveLeft(current_state) != ''

    def canMoveUp(self, current_state):
        return self.moveUp(current_state) != ''

    def canMoveDown(self, current_state):
        return self.moveDown(current_state) != ''

    def canMoveRight(self, current_state):
        return self.moveRight(current_state) != ''

    ################
    def is_game_over(self, current_state):
        return current_state in [3, 7]

