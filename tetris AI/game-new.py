from random import choice
import time
import os
from visual import *
import copy
from settings import *
#from utils import *

word=label(pos=vector(7,0,-60),text='Paused',height=70,color=(0.8,0.8,0.5))
scoreword=label(pos=vector(10,0,-3),text='Score :%6d'%(score),height=20,color=(1,1,1))
def game_over():
    print "GAME OVER: score {}".format(score)
    exit()


def play(t_stamp = [time.time(), 0]):
    """ play() is the core engine of this game
        This function changes the position
        every steps.
    """

    global piece, px, py, pc, focus, score,newpiece, npx, npy, npc,newboard,board,begin,focus1,piece1, px1, py1, pc1

    # Time goes on
    t_stamp[1] = time.time()
    if t_stamp[1] - t_stamp[0] > speed_rate and not scene.pause:
    
        # Descend
        if not collide(piece, px, py + 1):
            py += 1

        elif py < 0:
            # Hit the top, Game Over
            game_over()
            return

        else:
            # Hit the bottom, place the block
            place_piece(piece, px, py, pc)

            # Check if there are lines
            
            clear = clear_complete_lines()
            
            newboard=board[:]
            
            
            if clear:
                score +=100*len(clear)
                
                
        
            # Produce a new box
                
            
            piece, px, py, pc =piece1[:], 3, -2, pc1
            focus =focus1[:]
            piece1, px1, py1, pc1 = new_block(choice(block.keys()))
            focus1 = new_focus(piece1[:], pc1)
                
                
        
           

    scoreword.text='Score :%6d'%(score)
    #c=0
    if not scene.pause and py==-2:
        newpiece, npx, npy, npc =piece[:], px, py, pc
        autoplay()
        #return c
            
            
    # Change the position
    
'''
focus[i].pos <4, -1, 0> vector(px, py) <3, -2, 0> piece[i] (1, 1)
focus[i].pos <4, 0, 0> vector(px, py) <3, -2, 0> piece[i] (1, 2)
focus[i].pos <5, 0, 0> vector(px, py) <3, -2, 0> piece[i] (2, 2)
focus[i].pos <5, 1, 0> vector(px, py) <3, -2, 0> piece[i] (2, 3)'''
cannpx=0
def autoplay():
    global newpiece,npx,npy,npc,ghostdict,px,py,piece,hi_move,board,cannpx
    brandnewpiece=[0,0,0,0]
    for _ in xrange(4):
        for i in xrange(4):brandnewpiece[i]=(-(newpiece[i][1])+3,newpiece[i][0])  #rotate the newpiece, brand new piece is only for saving the parameters
        while not collide(newpiece, npx-1, npy ):                           #move to the left edge
            npx-=1
        while not collide(newpiece, npx, npy ):                             #move to the right step by step
            newpiece=brandnewpiece
            while not collide(newpiece, npx, npy+1 ):                           #move to the bottom
                npy+=1
                cannpx=0
            getscore(newpiece, npx, npy, npc,cannpx)           #getscore
            if not collide(newpiece, npx+1, npy):
                cannpx=1
                #npx+=1
                getscore(newpiece, npx+1, npy, npc,cannpx)
            if not collide(newpiece, npx-1, npy):
                cannpx=-1
                #npx+=1
                getscore(newpiece, npx-1, npy, npc,cannpx) 
            npy=py
            npx+=1                                     #move newpiece back 
        npx-=3
    
    
    py+=2
    #piece=hi_move[2][:]
    if px>=hi_move[0]:
        while  px>hi_move[0]:
            rate(100)
            px-=1
            for i in xrange(4):focus[i].pos=vector(px,py)+piece[i]
    elif px<hi_move[0]:
        while  px<hi_move[0]:
            rate(100)
            px+=1
            for i in xrange(4):focus[i].pos=vector(px,py)+piece[i]
    if hi_move[4]==1:px-=1
    if hi_move[4]==-1:px+=1
    for i in xrange(4):focus[i].pos=vector(px,py)+piece[i]
    rotatepiece=[0,0,0,0]
    while piece!=hi_move[2][:]:
        rate(100)
        for i in xrange(4):rotatepiece[i]=(-(piece[i][1])+3,piece[i][0])
        piece=rotatepiece[:]
    while py<hi_move[1]:
        rate(100)
        py+=1
        for i in xrange(4):focus[i].pos=vector(px,py)+piece[i]
    if hi_move[4]==1:px+=1
    if hi_move[4]==-1:px-=1
    for i in xrange(4):focus[i].pos=vector(px,py)+piece[i]
    #v=hi_move[:][3]
    hi_move=[0,0,0,-1000,0]
    #return v
n=3  
hi_move=[0,0,0,-1000,0]
def getscore(newpiece, npx, npy, npc,cannpx):                  #work for only 1 time
    global newboard,board,hi_move,n
    newboard=[]
    ghostscore=0
    
    for i in xrange(len(board)):newboard.append(board[i][:])
    place_newpiece(newpiece, npx, npy, npc)
    
    for y in xrange(BOARD_HEIGHT):                                  #check horizontal bondings
        for x in xrange(BOARD_WIDTH-1):
            if newboard[y][x]>0 and newboard[y][x+1]>0:ghostscore+=1
            if newboard[y][x]>0:ghostscore+=y
        if newboard[y][0]>0:ghostscore+=1
        if newboard[y][-1]>0:ghostscore+=1+y
        if not 0 in newboard[y]:ghostscore+=1000
        
    for x in xrange(BOARD_WIDTH):                                   #check vertical bondings
        for y in xrange(BOARD_HEIGHT-1):
            if newboard[y][x]>0 and newboard[y+1][x]>0:ghostscore+=1
            if newboard[y][x]>0 and newboard[y+1][x]==0:ghostscore-=100
        if newboard[-1][x]>0:ghostscore+=1
    '''while n>=0:
        rate(1)
        n-=1
        ghostscore+=play()
    while n==0:
        n=3'''
    if ghostscore>hi_move[3]:
        hi_move=[npx,npy,newpiece[:],ghostscore,cannpx]
    if ghostscore>=hi_move[3]and hi_move[4]!=0 and  cannpx==0:
        hi_move=[npx,npy,newpiece[:],ghostscore,cannpx]
    #return ghostscore
    
    #take newboard=board, then modify the 'place_piece' function to get the collided newboard
    #so we can caculate the score

def place_newpiece(newpiece, npx, npy, npc):
    """ Place the piece on the board
    @param piece   : the shape of the block
           px,py,pc: information of the block
    """
    

    for i, j in newpiece:
        x = npx + i
        y = npy + j
        if not (0 <= x < BOARD_WIDTH):
            continue
        if not (0 <= y < BOARD_HEIGHT):
            continue
        newboard[y][x] = npc

def new_board_lines(num):
    """ Produce new lines
    @param num: The number of new lines.

    @return: A list of zeros, which means a new line.
    """
    

    assert isinstance(num, int), num
    return [[0] * BOARD_WIDTH for j in range(num)]


# Initial Board information
board = new_board_lines(BOARD_HEIGHT)


def place_piece(piece, px, py, pc):
    """ Place the piece on the board
    @param piece   : the shape of the block
           px,py,pc: information of the block
    """
    

    for i, j in piece:
        x = px + i
        y = py + j
        if not (0 <= x < BOARD_WIDTH):
            continue
        if not (0 <= y < BOARD_HEIGHT):
            continue
        board[y][x] = pc


def clear_complete_lines():
    """ This function checks whether there are lines or not.

    @returns: A list recorded where the full lines are.
    """
    global board


    nb = []
    fn = []
    for idl, line in enumerate(board):
        if 0 in line:
            # Not full
            nb.append(line)
        else:
            fn.append(idl)

    if fn:
        # Update the board information
        board = new_board_lines(len(fn)) + nb
        

    # clear
    d_line = [obj for obj in scene.objects if type(obj) is box and obj.y in fn]
    for _ in xrange(10):
        rate(20)
        for obj in d_line:
            obj.opacity -= 0.1
    for obj in d_line:
        obj.visible = 0
    

    # decline
    for n in fn:
        for obj in (obj for obj in scene.objects if type(obj) is box and obj.y < n):
            obj.y += 1
    return fn


def collide(piece, px, py):
    """ Check if the position(px,py) collides with the board
    @param piece: the shape of the block
              px: x of the new position
              py: y of the new position
    @returns: True or False
    """
    for (i, j) in piece:
        x = px + i
        y = py + j
        if not (0 <= x < BOARD_WIDTH):
            return True
        if y >= BOARD_HEIGHT:
            return True
        if y < 0:
            continue
        if board[y][x]:
            return True
    return False

if __name__ == '__main__':
    os.startfile('back.mp3')
    # Place the first block
    '''piece, px, py, pc = new_block(choice(block.keys()))
    focus = new_focus(piece, pc)'''
    piece1, px1, py1, pc1 = new_block(choice(block.keys()));px1+=4
    focus1 = new_focus(piece1[:], pc1)
    piece, px, py, pc = new_block(choice(block.keys()));px,py=3,-2
    focus = new_focus(piece[:], pc)
    
    while 1:
        rate(1)
        
        play()
