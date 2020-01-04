

import time
import copy
import numpy as np

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

    def set_board(self, i, j, k):
        pos = 4 + 2*j
        text = self.board[i+2]
        text = text[:pos] + self.colors[k] + text[pos+1:]
        self.board[i+2] = text
        if self.used[i][j] == self.colors[other(k)]:
            self.score[other(k)] -= 1
        self.used[i][j] = self.colors[k]
        self.score[k] += 1

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
                        moves.append((i,j))
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

    def flip_line(self,i,j,off_i,off_j,player):
        if i + off_i < 0 or i + off_i > 7:
            return False
        if j + off_j < 0 or j + off_j > 7:
            return False
        if not self.used[i+off_i][j+off_j]:
            return False
        if self.used[i+off_i][j+off_j] == self.colors[player]:
            return True
        else:
            if self.flip_line(i+off_i,j+off_j,off_i,off_j,player):
                self.set_board(i+off_i,j+off_j,player)
                return True
            else:
                return False

    def flip_board(self,i,j,player):
        self.flip_line(i, j, -1, -1, player)
        self.flip_line(i, j, -1, 0, player)
        self.flip_line(i, j, -1, 1, player)

        self.flip_line(i, j, 0, -1, player)
        self.flip_line(i, j, 0, 1, player)

        self.flip_line(i, j, 1, -1, player)
        self.flip_line(i, j, 1, 0, player)
        self.flip_line(i, j, 1, 1, player)

    def print_score(self):
        print(self.score)
        print(sum(self.score))

    def get_children(self,player):
        moves = self.get_moves(player)
        my_list = []
        for move in moves:
            current_gc = copy.deepcopy(self)
            i,j = move
            current_gc.make_move(i,j,player)
            my_list.append(current_gc)
        return my_list

    def make_move(self,i,j,player):
        self.set_board(i, j, player)
        self.flip_board(i, j, player)

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

def play_round(player,gc):
    possible_moves = gc.get_moves(player)
    if possible_moves:
        print(possible_moves)
    else:
        return
    while True:
        move_x = int(input("Introduceti miscarea(x): "))
        move_y = int(input("Introduceti miscarea(y): "))
        if (move_x, move_y) in possible_moves:
            print("ok")
            gc.make_move(move_x,move_y,player)
            return

def play_computer(player,gc,depth,almost_lost):
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
    gc.make_move(move_x, move_y, player)
    return False

def playGame():
    gc = GameController()
    player_idx = 0
    me = 0
    gameOver = False
    almost_lost = [False,False]
    name = ["Player","Computer"]
    initial_time = time.time()
    while not gameOver:
        gc.print_board()
        gc.print_score()
        if player_idx == me: # Player
            #play_round(player_idx,gc)
            gameOver = play_computer(player_idx, gc, 2, almost_lost)
        else: # Computer
            # play_round(player_idx)
            gameOver = play_computer(player_idx, gc, 4, almost_lost)
        player_idx = (player_idx + 1) % 2
    dt = time.time() - initial_time
    print("A trecut", dt)
    winner = gc.score.index(max(gc.score))
    print("Winner is", name[winner], "with score", gc.score[winner], "vs", gc.score[other(winner)])

playGame()