# -*- coding: utf-8 -*-
import copy
import random
import time

import cv2
import numpy as np
import pyautogui as pag
from PIL import ImageGrab
from numpy import asarray

from ImageFinder import check_enemies, check_state, get_active_skills, image_to_array, get_states
from MoveMaker import click, click_ui, set_difficulty
from log import logger

locked_colors = ['bri', 'sph']


def get_uniques(board: np.ndarray):
    uniques, indexes, counts = np.unique(board,
                                         return_counts=True,
                                         return_index=True)
    return uniques, indexes, counts


def check_matches(board: np.ndarray, num_matches: int):
    for y in range(board.shape[1]):
        uniques, indexes, counts = get_uniques(board[y, :])
        if any(count >= num_matches for count in counts):
            max_match = 1
            for x in range(board.shape[0] - 1):
                if board[y, x] == board[y, x + 1]:
                    max_match += 1
                else:
                    max_match = 1
                if max_match == num_matches - 1:
                    aa = 1
                if max_match >= num_matches:
                    return board[y, x]

    for x in range(board.shape[1]):
        uniques, indexes, counts = get_uniques(board[:, x])
        if any(count >= num_matches for count in counts):
            if x == 2:
                aa = 1
            max_match = 1
            for y in range(board.shape[1] - 1):
                if board[y, x] == board[y + 1, x]:
                    max_match += 1
                else:
                    max_match = 1
                if max_match >= num_matches:
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
            future_board[x + 1, y], future_board[x, y] = \
                future_board[x, y], future_board[x + 1, y]
            color = check_matches(future_board, min_match)
            if color and color not in locked_colors:
                indexv += 1
                valid_swaps[f'{color} {indexv}V'] = {
                    'from': {'x': x, 'y': y},
                    'to': {'x': x + 1, 'y': y}}
    return valid_swaps


def predict_moves(board: np.ndarray, move: dict, color: str, length: int):
    logger.info(f'Predicting move: {move}')
    future = copy.copy(board)
    future[move['from']['x'], move['from']['y']], \
    future[move['to']['x'], move['to']['y']] = \
        future[move['to']['x'], move['to']['y']], \
        future[move['from']['x'], move['from']['y']]

    # Horizontal move
    if move['from']['x'] == move['to']['x']:
        column_f = future[:, move['from']['y']]
        column_t = future[:, move['to']['y']]
        line = future[move['from']['x'], :]

        match_line = np.where(line == color)[0]
        matches_col_f = np.where(column_f == color)[0]
        matches_col_t = np.where(column_t == color)[0]

    # Vertical move
    if move['from']['y'] == move['to']['y']:
        column = future[:, move['from']['y']]
        line_f = future[move['from']['x'], :]
        line_t = future[move['to']['x'], :]

        match_column = np.where(column == color)[0]
        matches_row_f = np.where(line_f == color)[0]
        matches_row_t = np.where(line_t == color)[0]


def get_all_moves(str_array: np.ndarray):
    valid_moves_5 = find_valid_move(str_array, 5)
    valid_moves_4 = find_valid_move(str_array, 4)
    valid_moves_3 = find_valid_move(str_array, 3)

    if valid_moves_5 != dict():
        # for move in valid_moves_5:
        #     predict_moves(str_array, valid_moves_5[move], move[:3], 5)
        logger.info(f'Moves: {valid_moves_5}')
        return valid_moves_5, 5
    if valid_moves_4 != dict():
        # for move in valid_moves_4:
        #     predict_moves(str_array, valid_moves_4[move], move[:3], 4)
        logger.info(f'Moves: {valid_moves_4}')
        return valid_moves_4, 4
    if valid_moves_3 != dict():
        # for move in valid_moves_3:
        #     predict_moves(str_array, valid_moves_3[move], move[:3], 3)
        logger.info(f'Moves: {valid_moves_3}')
        return valid_moves_3, 3
    return None


def use_skill(skill_name: dict,
              skills: dict,
              ui_images: dict,
              background: np.array,
              select_gems: bool = False,
              select_enemy: bool = False,
              accuracy: float = 0.8):
    gem_colors = ['Violet.png', 'Blue.png', 'Brown.png',
                  'Green.png', 'Red.png', 'Yellow.png']
    pos_1 = (200, 100, 650, 400)
    pos_2 = (200, 450, 650, 750)
    pos_3 = (200, 750, 650, 1100)
    pos_4 = (200, 1100, 650, 1450)
    from main import UiImages
    from main import GemTiles

    skill_img = skills[skill_name['name']]['as_array']
    image = ImageGrab.grab()
    if not check_state(ui_images['InBattle.png']['as_array'],
                       2400, 0, 2560, 200):
        return
    image_skills = image.crop(pos_1)
    skill_area = asarray(image_skills)
    result = cv2.matchTemplate(skill_img,
                               skill_area,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= accuracy:
        logger.info(f'Using skill: {skill_name}')
        click(random.randint(250, 500), random.randint(150, 350))

    if not check_state(ui_images['InBattle.png']['as_array'],
                       2400, 0, 2560, 200):
        return
    image_skills = image.crop(pos_2)
    skill_area = asarray(image_skills)
    result = cv2.matchTemplate(skill_img,
                               skill_area,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= accuracy:
        logger.info(f'Using skill: {skill_name}')
        click(random.randint(250, 500), random.randint(500, 700))

    if not check_state(ui_images['InBattle.png']['as_array'],
                       2400, 0, 2560, 200):
        return
    image_skills = image.crop(pos_3)
    skill_area = asarray(image_skills)
    result = cv2.matchTemplate(skill_img,
                               skill_area,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= accuracy:
        logger.info(f'Using skill: {skill_name}')
        click(random.randint(250, 500), random.randint(800, 1050))

    if not check_state(ui_images['InBattle.png']['as_array'],
                       2400, 0, 2560, 200):
        return
    image_skills = image.crop(pos_4)
    skill_area = asarray(image_skills)
    result = cv2.matchTemplate(skill_img,
                               skill_area,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= accuracy:
        logger.info(f'Using skill: {skill_name}')
        click(random.randint(250, 500), random.randint(1150, 1400))

    while pag.locateCenterOnScreen(f'{UiImages}\\GreyCast.png'):
        for _ in range(3):
            time.sleep(1)
            break
    cast = pag.locateCenterOnScreen(f'{UiImages}\\Cast.png')

    if cast:
        if not check_state(ui_images['InBattle.png']['as_array'],
                           2400, 0, 2560, 200):
            return
        pag.click(cast[0], cast[1], duration=random.randint(0, 10) / 30)
        time.sleep(0.5)
        if select_gems:
            for gem in gem_colors:
                if pag.locateCenterOnScreen(f'{GemTiles}\\{gem}'):
                    selected = pag.locateCenterOnScreen(f'{GemTiles}\\{gem}')
                    if selected:
                        click(selected[0], selected[1])
                        time.sleep(0.5)
                        click(selected[0], selected[1])
        if select_enemy:
            if not check_state(ui_images['InBattle.png']['as_array'],
                               2400, 0, 2560, 200):
                return
            enemies = check_enemies(background)
            for enemy_ in enemies:
                enemy = enemies[enemy_]
                if enemy['state']:
                    pag.click(enemy['position'][0],
                              enemy['position'][1],
                              duration=random.randint(0, 10) / 30)
                    return


def filter_color(moves: dict, colors: list):
    for color in colors:
        for move in moves.keys():
            if move.startswith(color):
                return moves[move]


def use_skills(skills: dict, active_skills: list,
               ui_images: dict, turn: bool = True):
    from main import AutoSkills
    skill_used = False
    while get_active_skills(skills, active_skills):
        for skill_name in AutoSkills:
            skill = AutoSkills[skill_name]
            if turn:
                if skill['turn']:
                    use_skill(skill,
                              skills,
                              ui_images,
                              ui_images['EnemyBack.png']['as_array'],
                              skill['gem'],
                              skill['enemy'])
                    skill_used = True
            else:
                use_skill(skill,
                          skills,
                          ui_images,
                          ui_images['EnemyBack.png']['as_array'],
                          skill['gem'],
                          skill['enemy'])
                skill_used = True
    return skill_used


def get_next_move(tiles: dict, ui_images: dict):
    from main import ColorPrefs
    move_set = None
    move = None
    length = 0
    str_array = image_to_array(tiles)

    while (str_array == None).any():
        str_array = image_to_array(tiles)
        time.sleep(0.5)
        if not check_state(ui_images['InBattle.png']['as_array'],
                           2400, 0, 2560, 200):
            break

    if not (str_array == None).any():
        move_set, length = get_all_moves(str_array)
    if move_set is not None:
        move = filter_color(move_set, ColorPrefs)
    return move, length


def states_loop(states: dict, ui_images: dict, difficulty: int):
    if states['in_skip']:
        click_ui(ui_images, ui_images[f'Skip.png']['file_name'])
        states = get_states(ui_images)

    if states['in_victory']:
        click_ui(ui_images, ui_images[f'Victory.png']['file_name'])
        states = get_states(ui_images)

    if states['in_explore']:
        click_ui(ui_images, ui_images['DifficultySettings.png']['file_name'])
        set_difficulty(ui_images, difficulty)
        states = get_states(ui_images)

    if states['in_difficulty']:
        click_ui(ui_images, ui_images['Continue.png']['file_name'])
        states = get_states(ui_images)

    if states['in_explore_2'] and states['in_explore_2']:
        click_ui(ui_images, ui_images['Explore.png']['file_name'])
        states = get_states(ui_images)

    if states['in_popup']:
        click_ui(ui_images, ui_images['ContinueBig.png']['file_name'])
        states = get_states(ui_images)

    if states['in_explore_mini']:
        click_ui(ui_images, ui_images['MiniBoss.png']['file_name'])
        states = get_states(ui_images)

    if states['in_battle_prepare']:
        click_ui(ui_images, ui_images['ToBattle.png']['file_name'])
        states = get_states(ui_images)

    if states['in_lvl']:
        click_ui(ui_images, ui_images['LevelUp.png']['file_name'])
        time.sleep(1)
        click(1000, 800)
        time.sleep(1)