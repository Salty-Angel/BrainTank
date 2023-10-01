from dataclasses import dataclass

'''
Functions available to brains:
    memory() - returns [symbol], a read only copy of queued commands
    forget() - clear all queued brain commands
    face(symbol) - change tank facing to symbol UP, DOWN, LEFT, or RIGHT
    forward() - move tank forward one space
    backward() - move tank backward one space
    shoot() - fire tank's weapon with current facing
    radar(x,y) - get a tuple (tile, item) from the map's x,y coordinate
    kill() - self destruct tank

Variables available to brains:
    color - string, tank color
    position - tuple (x,y), current tank grid position
    facing - symbol UP, DOWN, LEFT, RIGHT, current tank facing
    direction - tuple (x,y), unit vector representing tank facing
    shots - how many shots have been fired
    tanks - list of other tanks in map
    tank_positions - [(x,y)] other tank positions
    tank_states - list of other tank states (see Tank States)
'''

'''
1. Find out where the other tank is
    - Above us, to the right, left, below
2. If in the same row or column as us, face them and fire
3. If they are more than one rows/cols away, figure out which direction is closest and move that way
4. if they are within one rows/cols, face them and fire (bullets take time to get there)
'''

'''
Edge cases: 
   - dont drive into water
   - what if we cannot move close to them?
'''

@dataclass
class Position:
    x: int
    y: int

@dataclass
class Tile:
    terrain: str
    object: str

def think(game):
    if game.state == game.IDLE:
        navigate(game)
        chase(game)


def get_relative_position(game):
    other_tank_position = Position(*game.tank_positions[0])
    our_tank_position = Position(*game.position)

    print('other tank', other_tank_position)
    print('our tank', our_tank_position)

    relative_x = other_tank_position.x - our_tank_position.x
    relative_y = other_tank_position.y - our_tank_position.y

    return Position(relative_x, relative_y)

def human_readable_relative(position, game):
    if position.x > 0:
        horizontal = game.RIGHT
    else:
        horizontal = game.LEFT

    if position.y > 0:
        vertical = game.DOWN
    else:
        vertical = game.UP

    return Position(horizontal, vertical)

def navigate(game):
    our_tank_position = Position(*game.position)
    relative_position = get_relative_position(game)
    hrrel_pos = human_readable_relative(relative_position, game)

    if game.facing == game.UP:
        tile = Tile(*game.radar(our_tank_position.x, our_tank_position.y - 1))
        if tile.terrain is not None:
            game.face(hrrel_pos.x)
    if game.facing == game.DOWN:
        tile = Tile(*game.radar(our_tank_position.x, our_tank_position.y + 1))
        if tile.terrain is not None:
            game.face(hrrel_pos.x)
    if game.facing == game.LEFT:
        tile = Tile(*game.radar(our_tank_position.x - 1 , our_tank_position.y))
        if tile.terrain is not None:
            game.face(hrrel_pos.y)
    if game.facing == game.RIGHT:
        tile = Tile(*game.radar(our_tank_position.x + 1, our_tank_position.y))
        if tile.terrain is not None:
            game.face(hrrel_pos.y)

    game.forward()
    

def chase(game):
    print('memory (before):', game.memory)

    relative_position = get_relative_position(game)

    # which way should we face
    new_facing = None
    if abs(relative_position.x) > abs(relative_position.y):
        # move up/down
        if relative_position.y > 0:
            new_facing = game.DOWN
        elif relative_position.y < 0:
            new_facing = game.UP
        elif relative_position.y == 0:
            if relative_position.x > 0:
                new_facing = game.RIGHT
            if relative_position.x < 0:
                new_facing = game.LEFT
    else:
        # move right/left
        if relative_position.x > 0:
            new_facing = game.RIGHT
        elif relative_position.x < 0:
            new_facing = game.LEFT
        elif relative_position.x == 0:
            if relative_position.y > 0:
                new_facing = game.DOWN
            if relative_position.y < 0:
                new_facing = game.UP
        
    if new_facing != game.facing:
        game.face(new_facing)

    # move in that direction
    game.forward()

    print('memory (after):', game.memory)