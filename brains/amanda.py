#!/usr/bin/python
# -*- coding: utf-8 -*-

###############################################################################
# Python AI Battle
#
# Copyright 2011 Matthew Thompson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

'''
Wander Brain

This is a sample wandering brain. It just drives until it
hits an obstacle then chooses a new direction. It also changes
direction periodically.

Variables available to brains:
    color - string, tank color
    position - tuple (x,y), current tank grid position
    facing - symbol UP, DOWN, LEFT, RIGHT, current tank facing
    direction - tuple (x,y), unit vector representing tank facing
    shots - how many shots have been fired
    tanks - list of other tanks in map
    tank_positions - [(x,y)] other tank positions
    tank_states - list of other tank states (see Tank States)

Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Facings:
    UP, DOWN, LEFT, RIGHT,

Brain Commands:
    FORWARD, BACKWARD, SHOOT

Tank States:
    IDLE, MOVING, TURNING, SHOOTING, DEAD

Tiles:
    GRASS, DIRT, PLAIN, WATER
    SAFE_TILES = (GRASS, DIRT, PLAIN) - can be driven on safely
    UNSAFE_TILES = (WATER,) - will destroy your tank if you drive into them

Items:
    ROCK, TREE - blocking items that can be destroyed
    TANK_BLUE, TANK_RED - tanks located on a tile

Lookup Helper Dictionaries:
    FACING_TO_VEC - takes a facing symbol and returns the (x,y) unit vector

'''

import random

counter = 1


def think(game):
    x, y = game.position
    dx, dy = game.direction

    global counter
    #     print("counter is", counter)
    counter += 1

    tile, item = game.radar(x + dx, y + dy)
    #     print("at", x, y, "and facing", game.facing)
    #     print("will be moving into:", tile, item)

    def new_facing_def():
        # out of all facing possibilities, choose one we don't have currently
        #         new_facing = [game.UP, game.DOWN, game.LEFT, game.RIGHT]
        #         new_facing.remove(game.facing)
        print(game.tank_positions)
        enemy = game.tank_positions[0]
        # Randomly decide to move either vertically or horizontally
        mynum = random.randint(0, 1)
        print(f'MY NUM: {mynum}')
        vertical = False
        if mynum == 0:
            # Move horizontal
            if game.position[0] > enemy[0]:
                new_facing = [game.LEFT]
            elif game.position[0] < enemy[0]:
                new_facing = [game.RIGHT]
            else:
                # We are on the same row, move vertical
                vertical = True

        if mynum == 1 or vertical:
            if game.position[1] > enemy[1]:
                new_facing = [game.UP]
            elif game.position[1] < enemy[1]:
                new_facing = [game.DOWN]
            else:
                new_facing = []

        # evaluate the possible facings and remove ones that will block tank
        good_facing = []
        for f in new_facing:
            v = game.FACING_TO_VEC[f]
            nt, ni = game.radar(x + v[0], y + v[1])
            if ni is None and nt not in (None, game.WATER):
                good_facing.append(f)

        print(f"GOOD FACING : {good_facing}")
        print(f"NEW FACING : {new_facing}")

        if game.facing in good_facing:
            game.shoot()
            return game.facing

        if good_facing:
            return good_facing[0]
        else:
            game.shoot()
            return random_facing()

    def random_facing():
        # out of all facing possibilities, choose one we don't have currently
        new_facing = [game.UP, game.DOWN, game.LEFT, game.RIGHT]
        new_facing.remove(game.facing)

        # evaluate the possible facings and remove ones that will block tank
        good_facing = []
        for f in new_facing:
            v = game.FACING_TO_VEC[f]
            nt, ni = game.radar(x + v[0], y + v[1])
            print(nt, ni)
            if ni is None and nt not in (None, game.WATER):
                good_facing.append(f)

        return random.choice(good_facing or new_facing)

    # avoid moving into blocking items
    if item is not None or tile in (game.WATER, None):
        game.forget()
        x = new_facing_def()
        game.face(x)
        game.shoot()

    elif random.randint(0, 2) == 0:
        # 1 out of 5 times choose a new direction
        x = new_facing_def()
        game.face(x)
        game.shoot()

    if random.randint(0, 2) == 0:
        game.shoot()

    if game.FORWARD not in game.memory:
        game.forward()

    print("brain queue:", game.memory)
