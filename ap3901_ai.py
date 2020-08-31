#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 3

An AI player for Othello. This is the template file that you need to  
complete and submit. 

@author: ANTON PRIYANKA P(ap3901)
"""

import random
import sys
import time
import heapq

# You can use the functions in othello_shared to write your AI
from othello_shared import get_possible_moves, play_move, compute_utility

############ MINIMAX ###############################

"""
Computes the minimax value of a MAX node
"""


def minimax_max_node(board):
    possible_moves = get_possible_moves(board, 1)
    if not possible_moves:
        return compute_utility(board)

    v = -sys.maxsize - 1

    for a in possible_moves:
        v = max(v, minimax_min_node(play_move(board, 1, a[0], a[1])))
    return v


"""
Computes the minimax value of a MIN node
"""


def minimax_min_node(board):
    possible_moves = get_possible_moves(board, 2)
    if not possible_moves:
        return compute_utility(board)

    v = sys.maxsize

    for a in possible_moves:
        v = min(v, minimax_max_node(play_move(board, 2, a[0], a[1])))
    return v


"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""


def select_move_minimax(board, color):
    possible_moves = get_possible_moves(board, color)
    move = (-1, -1)

    if color == 1:
        v = -sys.maxsize - 1
        prev_v = -sys.maxsize - 1
    else:
        v = sys.maxsize
        prev_v = sys.maxsize

    for a in possible_moves:
        if color == 1:
            v = max(v, minimax_min_node(play_move(board, color, a[0], a[1])))
        elif color == 2:
            v = min(v, minimax_max_node(play_move(board, color, a[0], a[1])))
        if v != prev_v:
            move = (a[0], a[1])
            prev_v = v
    return move


############ ALPHA-BETA PRUNING #####################

"""
Computes the minimax value of a MAX node with alpha-beta pruning
"""


def alphabeta_max_node(board, alpha, beta, level=1, limit=float("inf")):
    possible_moves = []
    moves_prioritized = []
    if level <= limit:
        possible_moves = get_possible_moves(board, 1)

    if not possible_moves:
        return compute_utility(board)

    level = level + 1
    for a in possible_moves:
        heapq.heappush(moves_prioritized, ((-1) * compute_utility(play_move(board, 1, a[0], a[1])), a))

    v = -sys.maxsize - 1
    for i in range(len(moves_prioritized)):
        _, a = heapq.heappop(moves_prioritized)
        v = max(v, alphabeta_min_node(play_move(board, 1, a[0], a[1]), alpha, beta, level, limit))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


"""
Computes the minimax value of a MIN node with alpha-beta pruning
"""


def alphabeta_min_node(board, alpha, beta, level=1, limit=float("inf")):
    possible_moves = []
    moves_prioritized = []

    if level <= limit:
        possible_moves = get_possible_moves(board, 2)

    if not possible_moves:
        return compute_utility(board)

    level = level + 1
    for a in possible_moves:
        heapq.heappush(moves_prioritized, (compute_utility(play_move(board, 2, a[0], a[1])), a))

    v = sys.maxsize
    for i in range(len(moves_prioritized)):
        _, a = heapq.heappop(moves_prioritized)
        v = min(v, alphabeta_max_node(play_move(board, 2, a[0], a[1]), alpha, beta, level, limit))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v


"""
Given a board and a player color, decide on a move. 
The return value is a tuple of integers (i,j), where
i is the column and j is the row on the board.  
"""


def select_move_alphabeta(board, color, limit=float("inf")):
    possible_moves = get_possible_moves(board, color)
    move = (-1, -1)

    if color == 1:
        v = -sys.maxsize - 1
        prev_v = -sys.maxsize - 1
    else:
        v = sys.maxsize
        prev_v = sys.maxsize

    alpha = -sys.maxsize - 1
    beta = sys.maxsize

    for a in possible_moves:
        if color == 1:
            v = max(v, alphabeta_min_node(play_move(board, color, a[0], a[1]), alpha, beta, level=2, limit=6))
        elif color == 2:
            v = min(v, alphabeta_max_node(play_move(board, color, a[0], a[1]), alpha, beta, level=2, limit=6))
        if v != prev_v:
            move = (a[0], a[1])
            prev_v = v
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI")  # First line is the name of this AI
    color = int(input())  # Then we read the color: 1 for dark (goes first),
    # 2 for light.

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager 
            # movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
