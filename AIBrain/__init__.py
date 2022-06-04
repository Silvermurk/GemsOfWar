# -*- coding: utf-8 -*-
import copy
import random
import time

import numpy as np
import pyautogui as pag
from log import logger
locked_colors = ['bri', 'sph']


def get_uniques(board: np.ndarray):
    counts = 0
    uniques = 0
    indexes = 0
    retries = 0
    while isinstance(counts, int) and counts == 0:
        try:
            uniques, indexes, counts = np.unique(board,
                                                 return_counts=True,
                                                 return_index=True)
        except TypeError:
            logger.info(f'Bad column, retrying {retries}')
            time.sleep(0.1)
            retries += 1
            board[board is None] = 'X'
        if retries > 5:
            logger.info('Max count, bad image :(\n'
                        f'{board}')
            return 0, 0, 0

    return uniques, indexes, counts


def check_matches(board: np.ndarray, num_matches: int):
    for y in range(board.shape[1]):
        # logger.info(f'board[y, :]:{board[y, :]}')
        uniques, indexes, counts = get_uniques(board[y, :])
        if any(count >= num_matches for count in counts):
            # logger.info(f'board[y, :]:{board[y, :]}')
            max_match = 1
            for x in range(board.shape[0] - 1):
                if board[y, x] == board[y, x + 1]:
                    # logger.info(f'board[y, :]:{board[y, :]}')
                    max_match += 1
                else:
                    max_match = 1
                if max_match == num_matches - 1:
                    aa = 1
                if max_match >= num_matches:
                    # logger.info(f'board[y, :]:{board[y, :]}')
                    return board[y, x]

    for x in range(board.shape[1]):
        # logger.info(f'board[:, x]:{board[:, x]}')
        uniques, indexes, counts = get_uniques(board[:, x])
        if any(count >= num_matches for count in counts):
            if x == 2:
                aa = 1
            # logger.info(f'board[:, x]:{board[:, x]}')
            max_match = 1
            for y in range(board.shape[1] - 1):
                if board[y, x] == board[y + 1, x]:
                    # logger.info(f'board[:, x]:{board[:, x]}')
                    max_match += 1
                else:
                    max_match = 1
                if max_match >= num_matches:
                    # logger.info(f'board[:, x]:{board[:, x]}')
                    return board[y, x]
    return None


def find_valid_move(board: np.ndarray, min_match: int = 3):
    # Test Horizontal swaps
    valid_swaps = dict()
    indexh = 0
    indexv = 0
    for x in range(board.shape[0]):
        for y in range(board.shape[1] - 1):
            future_board = copy.copy(board)
            future_board[x, y], future_board[x, y + 1] = \
                future_board[x, y + 1], future_board[x, y]
            # logger.info(f'Swap: {[x, y + 1]} {future_board[x, y + 1]} - '
            #             f'{[x, y]} {future_board[x, y]}')
            # logger.info(f'\nFuture board: {show_str_array(future_board)}')
            color = check_matches(future_board, min_match)
            if color and color not in locked_colors:
                indexh += 1
                valid_swaps[f'{color} {indexh}H'] = {
                    'from': {'x': x, 'y': y},
                    'to': {'x': x, 'y': y + 1}}

    # Test Vertical swaps
    for x in range(board.shape[0] - 1):
        for y in range(board.shape[1]):
            future_board = copy.copy(board)
            future_board[x + 1, y], future_board[x, y] = future_board[x, y], future_board[x + 1, y]
            # logger.info(f'Swap: {[x + 1, y]} {future_board[x + 1, y]} - '
            #             f'{[x, y]} {future_board[x, y]}')
            # logger.info(f'\nFuture board: {show_str_array(future_board)}')
            color = check_matches(future_board, min_match)
            if color and color not in locked_colors:
                indexv += 1
                valid_swaps[f'{color} {indexv}V'] = {
                    'from': {'x': x, 'y': y},
                    'to': {'x': x + 1, 'y': y}}
    return valid_swaps


def predict_moves(board: np.ndarray, move: dict):
    logger.info(f'Predicting move: {move}')
    future = copy.copy(board)
    future[move['from'][x], move['from'][y]] = 
    aa = 1


def get_all_moves(str_array: np.ndarray):
    valid_moves_5 = find_valid_move(str_array, 5)
    valid_moves_4 = find_valid_move(str_array, 4)
    valid_moves_3 = find_valid_move(str_array, 3)

    if valid_moves_5 != dict():
        for move in valid_moves_5:
            predict_moves(str_array, valid_moves_5[move])
        return valid_moves_5, 5
    if valid_moves_4 != dict():
        for move in valid_moves_4:
            predict_moves(str_array, valid_moves_4[move])
        return valid_moves_4, 4
    if valid_moves_3 != dict():
        for move in valid_moves_3:
            predict_moves(str_array, valid_moves_3[move])
        return valid_moves_3, 3
    return None


def use_skill(skill: str):
    logger.info(f'Using skill: {skill}')
    from main import SkillTiles
    from main import UiImages
    skill = pag.locateCenterOnScreen(f'{SkillTiles}\\{skill}')
    if skill is not None:
        time.sleep(0.5)
        pag.click(skill[0] + random.randint(0, 10),
                  skill[1] + random.randint(0, 10),
                  duration=random.randint(1, 10) / 30)
        cast = pag.locateCenterOnScreen(f'{UiImages}\\Cast.png')
        while cast is None:
            time.sleep(0.5)
            pag.click(skill[0] + random.randint(0, 10),
                      skill[1] + random.randint(0, 10),
                      duration=random.randint(1, 10) / 30)
            cast = pag.locateCenterOnScreen(f'{UiImages}\\Cast.png')
        while pag.locateCenterOnScreen(f'{UiImages}\\GreyCast.png'):
            time.sleep(1)
        pag.click(cast[0], cast[1], duration=random.randint(0, 10) / 30)
        time.sleep(1)


def filter_color(moves: dict, colors: list):
    for color in colors:
        for move in moves.keys():
            if move.startswith(color):
                return moves[move]