import copy
import sys #(helps to quit the application)
import pygame
from constants import *
import numpy as np
import random
#pygame setup
pygame.init()# to initialize
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(bg_color)

# drawing the lines
class Board:
    def __init__(self):
        self.squares=np.zeros((rows,cols))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0
    def final_state(self,show=False):
        #vertical wins
        for col in range(cols):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                if show:
                    color=circ_colo if self.squares[0][col]==2 else cross_color
                    iPos=(col*sqsize+sqsize//2,20)
                    fPos=(col*sqsize+sqsize//2,height-20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)

                return self.squares[0][col]
        #horizontal wins
        for row in range(rows):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                if show:
                    color=circ_colo if self.squares[0][col]==2 else cross_color
                    iPos=(20,row*sqsize+sqsize//2)
                    fPos=(width-20,row*sqsize+sqsize//2)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
                return self.squares[row][0]
        #desc diagonal
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            if show:
                    color=circ_colo if self.squares[1][1]==2 else cross_color
                    iPos=(20,20)
                    fPos=(width-20,height-20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
            return self.squares[1][1]
        #asc diagonal
        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2]!=0:
            if show:
                    color=circ_colo if self.squares[1][1]==2 else cross_color
                    iPos=(20,height-20)
                    fPos=(width-20,20)
                    pygame.draw.line(screen,color,iPos,fPos,line_width)
            return self.squares[1][1]  
        #no win
        return 0
    def mark_sqrt(self,row,cols,player):
        self.squares[row][cols]=player
        self.marked_sqrs+=1
    def empty_sqrt(self,rows,cols):
        return self.squares[rows][cols]==0
    def isfull(self):
        return self.marked_sqrs==9
    def isempty(self):
        return self.marked_sqrs==0
    def get_empty_sqrs(self):

        empty_sqrs=[]
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqrt(row,col): 
                    empty_sqrs.append((row,col))
        return empty_sqrs


class AI:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player
    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))
        return empty_sqrs[idx]

    def minimax(self,board,maximizing):
        #terminal ends
        case=board.final_state()
        #player 1 wins
        if(case==1):
            return 1,None
        if(case==2):
            return -1,None
        elif (board.isfull()):
            return 0,None
        if maximizing:
            max_eval=-100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for(rows,cols) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqrt(rows,cols,1)
                eval=self.minimax(temp_board,False)[0]
                if(eval>max_eval):
                    max_eval=eval
                    best_move=(rows,cols)
            return max_eval,best_move
        
        elif not maximizing:
            min_eval=100
            best_move=None
            empty_sqrs=board.get_empty_sqrs()
            for(rows,cols) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqrt(rows,cols,self.player)
                eval=self.minimax(temp_board,True)[0]
                if(eval<min_eval):
                    min_eval=eval
                    best_move=(rows,cols)
            return min_eval,best_move


        
    def eval(self,main_board):
        if self.level==0:
            #random choice
            eval='random'
            move=self.rnd(main_board)

        else:
            #minmax alogo choice
            eval,move=self.minimax(main_board,False)
        print(f'AI has chosen to mark in the pos{move} with an eval of :{eval}')
        return move #row col
class Game:
    def __init__(self):
        self.board=Board()
        self.ai=AI()
        self.player=2
        #1-x---------2-O
        
        self.gamemode='pvp'#pvp or ai
        self.running=True
        self.show_lines()
    
    def make_move(self,rows,cols):
        self.board.mark_sqrt(rows,cols,self.player)
        self.draw_fig(rows,cols)
        self.next_turn()


    def show_lines(self):
        screen.fill(bg_color)
        #vertical
        pygame.draw.line(screen,line_color,(sqsize,0),(sqsize,height),line_width)
        pygame.draw.line(screen,line_color,(width-sqsize,0),(width-sqsize,height),line_width)
        #horizontal
        pygame.draw.line(screen,line_color,(0,sqsize),(width,sqsize),line_width)
        pygame.draw.line(screen,line_color,(0,height-sqsize),(width,height-sqsize),line_width)
    
    def draw_fig(self,rows,cols):
        if self.player==1:
            #draw cross
            #desc line
            start_desc=(cols*sqsize+offset,rows*sqsize+offset)
            end_desc=(cols*sqsize+sqsize-offset,rows*sqsize+sqsize-offset)
            pygame.draw.line(screen,cross_color,start_desc,end_desc,cross_width)
            #asec line
            start_asc=(cols*sqsize+offset,rows*sqsize+sqsize-offset)
            end_asc=(cols*sqsize+sqsize-offset,rows*sqsize+offset)
            pygame.draw.line(screen,cross_color,start_asc,end_asc,cross_width)
        elif self.player==2:
            #draw O
            centre=(cols*sqsize+sqsize//2,rows*sqsize+sqsize//2)
            pygame.draw.circle(screen,circ_colo,centre,radius,circ_width)
    
    def next_turn(self):
        self.player=self.player%2+1
    def change_gamemode(self):

        if self.gamemode=='pvp': 
            self.gamemode='ai'
        else:
            self.gamemode='pvp'
    def reset(self):
        self.__init__()
    def isover(self):
        return self.board.final_state(show=True) !=0 or self.board.isfull()
 
#MAIN FUNCTION
def main():
    game=Game()
    board=game.board
    ai=game.ai
    #mainloop
    while True:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_g:
                    game.change_gamemode()
                if event.key==pygame.K_r:
                    game.reset()
                    board=game.board
                    ai=game.ai
                if event.key==pygame.K_0:
                    ai.level=0
                if event.key==pygame.K_1:
                    ai.level=1

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                rows=pos[1]//sqsize
                cols=pos[0]//sqsize
                if board.empty_sqrt(rows,cols):
                    game.make_move(rows,cols)
                    if game.isover():
                        game.running=False
            
        if game.gamemode=="ai" and game.player==ai.player and game.running:
            pygame.display.update() 
            rows,cols=ai.eval(board)
            game.make_move(rows,cols)
            if game.isover():
                game.running=False
                
        #updating the screen after every move
        pygame.display.update()

main()