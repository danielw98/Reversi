

import time
import copy
import numpy as np
A = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H"}
B = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7}
def game_over(gc,player):
    return len(gc.get_moves(player)) == 0

def static_evaluation(gc,player):
    return gc.score[player]

def minimax_init(player, gc, depth, alpha_beta=False):
    best_move_score = float('inf')
    best_move_idx = -1
    available_moves = gc.get_moves(player)
    print(available_moves)
    children = gc.get_children(player)

    for i, child in enumerate(children):
        # presupun ca am facut miscarea available_moves[i]
        # vreau scorul maxim pe care il pot obtine
        # simulez randul celuilalt, care incearca sa isi maximizeze scorul
        # ma intereseaza care este paguba lui maxima, adica scorul minim
        # pe care il poate obtine, incercand sa obtina scor maxim
        score = minimax(other(player),child,depth,True,alpha_beta)
        if score < best_move_score:
            best_move_score = score
            best_move_idx = i
    if best_move_idx != -1:
        return available_moves[best_move_idx], best_move_score
    return None, float('-inf')


def minimax(player, gc, depth, maximizingPlayer, using_alpha_beta, alpha=float('-inf'), beta=float('+inf')):
    if depth == 0 or game_over(gc,player):
        return gc.score[player]
    if maximizingPlayer:
        max_eval = float('-inf')
        for child in gc.get_children(player):
            current  = minimax(other(player), child, depth-1, False, using_alpha_beta, alpha, beta)
            max_eval = max(max_eval,current)
            if using_alpha_beta:
                alpha = max(alpha,current)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for child in gc.get_children(player):
            current = minimax(other(player), child, depth-1, True, using_alpha_beta, alpha, beta)
            min_eval = min(min_eval,current)
            if using_alpha_beta:
                beta = min(beta,current)
                if beta <= alpha:
                    break
        return min_eval

def initial_board():
        my_list = list()
        my_list.append("    a b c d e f g h")
        my_list.append("    ---------------")
        my_list.append(" 0 |# # # # # # # #")
        my_list.append(" 1 |# # # # # # # #")
        my_list.append(" 2 |# # # # # # # #")
        my_list.append(" 3 |# # # n a # # #")
        my_list.append(" 4 |# # # a n # # #")
        my_list.append(" 5 |# # # # # # # #")
        my_list.append(" 6 |# # # # # # # #")
        my_list.append(" 7 |# # # # # # # #")

        return my_list


def initial_used():
    used = np.empty((8,8), dtype='str')
    used[3][3] = used[4][4] = 'n'
    used[3][4] = used[4][3] = 'a'
    place_piece(3,3,0)
    place_piece(4,4,0)
    place_piece(4,3,1)
    place_piece(3,4,1)
    pg.display.flip()
    return used


def other(player):
    return (player+1) % 2


class GameController:
    def __init__(self):
        self.board = initial_board()
        self.used = initial_used()
        self.colors = ['n', 'a']
        self.score = [2,2]

    def print_board(self):
        print("\n".join(self.board))

    def set_board(self, i, j, k,gui=None):
        pos = 4 + 2*j
        text = self.board[i+2]
        text = text[:pos] + self.colors[k] + text[pos+1:]
        self.board[i+2] = text
        if self.used[i][j] == self.colors[other(k)]:
            self.score[other(k)] -= 1
        self.used[i][j] = self.colors[k]
        self.score[k] += 1

        if gui:
            place_piece(i,j,k)
            pg.display.flip()



    def get_board(self,i,j):
        return self.board[i+2][4+2*j]

    def get_moves(self, player):
        moves = list()
        for i in range(8):
            for j in range(8):
                if not self.used[i][j]:
                    m1 = self.possible_move(i, j, -1,-1, player)
                    m2 = self.possible_move(i, j, -1, 0, player)
                    m3 = self.possible_move(i, j, -1, 1, player)

                    m4 = self.possible_move(i, j, 0,-1, player)
                    m5 = self.possible_move(i, j, 0, 1, player)

                    m6 = self.possible_move(i, j, 1,-1, player)
                    m7 = self.possible_move(i, j, 1, 0, player)
                    m8 = self.possible_move(i, j, 1, 1, player)

                    if m1 or m2 or m3 or m4 or m5 or m6 or m7 or m8:
                        moves.append((i,A[j]))
        return moves

    def check_stuff(self,i,j,off_i,off_j,player):
        if i + off_i < 0 or i + off_i > 7:
            return False
        if j + off_j < 0 or j + off_j > 7:
            return False
        if self.get_board(i+off_i,j+off_j) != self.colors[other(player)]:
            return False
        if i + off_i + off_i < 0 or i + off_i + off_i > 7:
            return False
        if j + off_j + off_j < 0 or j + off_j + off_j > 7:
            return False
        return True

    def possible_move(self,i,j,off_i,off_j,player):
        if not self.check_stuff(i,j,off_i,off_j,player):
            return False
        return self.explore(i+off_i+off_i,j+off_j+off_j,off_i,off_j,player)

    def explore(self, i, j, off_i, off_j,player):
        if not self.used[i][j]:
            return False
        if self.get_board(i,j) == self.colors[player]:
            return True
        if i + off_i < 0 or i + off_i > 7:
            return False
        if j + off_j < 0 or j + off_j > 7:
            return False
        return self.explore(i+off_i,j+off_j,off_i,off_j,player)

    def flip_line(self,i,j,off_i,off_j,player,gui):
        if i + off_i < 0 or i + off_i > 7:
            return False
        if j + off_j < 0 or j + off_j > 7:
            return False
        if not self.used[i+off_i][j+off_j]:
            return False
        if self.used[i+off_i][j+off_j] == self.colors[player]:
            return True
        else:
            if self.flip_line(i+off_i,j+off_j,off_i,off_j,player,gui):
                self.set_board(i+off_i,j+off_j,player,gui)
                if gui:
                    place_piece(i,j,player)
                    pg.display.flip()
                return True
            else:
                return False


    def flip_board(self,i,j,player,gui):
        self.flip_line(i, j, -1, -1, player,gui)
        self.flip_line(i, j, -1, 0, player,gui)
        self.flip_line(i, j, -1, 1, player,gui)

        self.flip_line(i, j, 0, -1, player,gui)
        self.flip_line(i, j, 0, 1, player,gui)

        self.flip_line(i, j, 1, -1, player,gui)
        self.flip_line(i, j, 1, 0, player,gui)
        self.flip_line(i, j, 1, 1, player,gui)

    def print_score(self):
        print(self.score)
        print(sum(self.score))

    def get_children(self,player):
        moves = self.get_moves(player)
        my_list = []
        for move in moves:
            current_gc = copy.deepcopy(self)
            i,j = move
            current_gc.make_move(i,j,player,None)
            my_list.append(current_gc)
        return my_list

    def make_move(self,i,j,player,gui):
        self.set_board(i, B[j], player,gui)
        self.flip_board(i, B[j], player,gui)


    '''def neighbours(self,player):
        neighbours_list = list()
        for i in range(8):
            for j in range(8):
                if self.get_board(i,j) == self.colors[other(player)]:
                    for off_i in [-1, 0, 1]:
                        for off_j in [-1, 0, 1]:
                            if (off_i, off_j) == (0,0):
                                continue
                            new_i, new_j = i + off_i, j + off_j
                            if new_i < 0 or new_i > 7:
                                continue
                            if new_j < 0 or new_j > 7:
                                continue
                            if not self.used[new_i][new_j] \
                                    and (new_i, new_j) not in neighbours_list:
                                neighbours_list.append((new_i, new_j))
        return neighbours_list'''


def show_suggested_moves(possible_moves):
    for move in possible_moves:
        x, y = move
        print(x,B[y])

def play_round(player,gc,gui=None):
    possible_moves = gc.get_moves(player)
    if possible_moves:
        print(possible_moves)
        if gui:
            show_suggested_moves(possible_moves)
    else:
        return
    while True:
        move_x = int(input("Introduceti miscarea(x): "))
        move_y = str(input("Introduceti miscarea(y): "))
        if (move_x, move_y) in possible_moves:
            print("ok")
            gc.make_move(move_x,move_y,player)
            return

def play_computer(player,gc,depth,almost_lost,gui):
    evaluation, score = minimax_init(player, gc, depth, True)
    if sum(gc.score) == 64:
        return True
    if not evaluation:
        if almost_lost[player]:
            return True
        almost_lost[player] = True
        return False
    else:
        almost_lost[player] = False
    print("Best move is:", evaluation, "with expected score", score)
    move_x, move_y = evaluation
    gc.make_move(move_x, move_y, player,gui)
    return False




import pygame as pg
import sys
import random

TILESIZE = 48
BGCOLOR = 11, 68, 9
BOARD = 0, 0, 0
WIDTH = 800
HEIGHT = 600

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))
background = BGCOLOR
board = pg.Surface((400,400))
screen.fill(BGCOLOR)


colors = [(33,138,28),(31,130,26)]
piece_color = [(200,200,200),(40,40,40)]
def draw_board():
    color = 0
    for i in range(8):
        if i%2 == 0:
            color = 0
        else:
            color = 1
        for j in range(8):
            color = (color + 1) % 2
            place_tile(i, j, color)

def place_tile(i,j,color):
    pg.draw.rect(screen,colors[color],(50*i,50*j,48,48))


def place_piece(i,j,player_idx):
    pg.draw.circle(screen,piece_color[player_idx],(50*i+25,50*j+25),22)
    pg.time.delay(200)

draw_board()
pg.display.flip()


def pg_event():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            sys.exit()


gui = 1
def playGame():
    gc = GameController()
    player_idx = 0
    me = 0
    gameOver = False
    almost_lost = [False,False]
    name = ["Player","Computer"]
    initial_time = time.time()
    while not gameOver:
        pg_event()
        gc.print_board()
        gc.print_score()
        if player_idx == me: # Player
            #play_round(player_idx,gc,gui=1)
            gameOver = play_computer(player_idx, gc, 2, almost_lost,gui)
        else: # Computer
            # play_round(player_idx)
            gameOver = play_computer(player_idx, gc, 4, almost_lost,gui)
        player_idx = (player_idx + 1) % 2
    dt = time.time() - initial_time
    print("A trecut", dt)
    winner = gc.score.index(max(gc.score))
    print("Winner is", name[winner], "with score", gc.score[winner], "vs", gc.score[other(winner)])

playGame()