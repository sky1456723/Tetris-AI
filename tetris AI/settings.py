from visual import *


""" These are basic settings for the game
    Change the numbers for fun!
"""
BOARD_WIDTH = 15
BOARD_HEIGHT = 20
speed_rate = 1


##########################################
# Below are core settings, do not change #
##########################################

score = 0

""" initialize the board """
scene.center = ((BOARD_WIDTH + 1) / 2, (BOARD_HEIGHT - 1) / 2)
scene.width = BOARD_WIDTH * 40
scene.height = BOARD_HEIGHT * 35
scene.forward = (0, 0, +1)
scene.up = 0, -1, 0
scene.lights = \
  [distant_light(direction=(0.22, 0.44, -0.88), color=color.gray(0.8)),
   distant_light(direction=(-0.88, -0.22, +0.44), color=color.gray(0.3))]
scene.autoscale = False
scene.pause = False

points(pos=[(x, y) for x in xrange(BOARD_WIDTH) for y in xrange(BOARD_HEIGHT)])


""" The six types of different blocks """
block = { 0b1111:(0, 0, 1), 
          0b101110:(0, 1, 1), 
          0b100111:(0, 1, 0), 
          0b1000111:(1, 0, 1), 
          0b11000110:(1, 0, 0),
          0b1101100:(1, 1, 0), 
          0b1100110:(1, 0.6, 0) }

side_length = 0.9

new_block = lambda pc: ([((z/4) + 1, z%4) for z in xrange(16) if (pc >> z) & 1], 3, -2, pc)
new_focus = lambda piece, pc: [box(pos=vector(p)+vector(BOARD_WIDTH,0), color=block[pc], size=(side_length, side_length, side_length)) for p in piece]
