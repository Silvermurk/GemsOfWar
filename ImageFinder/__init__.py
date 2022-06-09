# -*- coding: utf-8 -*-
import random
import time
from os import getcwd

import cv2
import numpy as np
import pyautogui as pag
from conftest import image_to_string, split_image
from log import logger
from numpy import asarray
from PIL import Image, ImageGrab


def image_to_array(tiles: dict, img_shot: str = None):
    image = ImageGrab.grab()
    image_board = image.crop((640, 100, 1920, 1380))
    if img_shot:
        image_board = Image.open(f'{getcwd()}\\Presets\\{img_shot}')
    img_grid = split_image(image_board, 160)
    img_array = asarray(img_grid).reshape((8, 8))
    str_array = image_to_string(img_array, tiles)
    return str_array


def get_active_skills(skills: dict,
                      active_skills: list,
                      accuracy: float = 0.7) -> bool:
    image = ImageGrab.grab()
    image_skills = image.crop((0, 0, 640, 1480))
    skill_list = asarray(image_skills)
    for skill in skills:
        # logger.info(f'Checking skill {skill}')
        skill_img = skills[skill]['as_array']
        result = cv2.matchTemplate(skill_img,
                                   skill_list,
                                   cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= accuracy:
            active_skills.append(skill)
            return True
    return False


def check_state(state: np.ndarray,
                xf: int = 0, yf: int = 0,
                xt: int = 2560, yt: int = 1440,
                accuracy: float = 0.7,
                debug: bool = False):
    image = ImageGrab.grab()
    if debug:
        image.crop((xf, yf, xt, yt)).show()
        time.sleep(4)
    area = asarray(image.crop((xf, yf, xt, yt)))
    result = cv2.matchTemplate(state,
                               area,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= accuracy:
        return True
    return False


def check_enemies(background: np.ndarray):
    pos_1 = (1900, 100, 2400, 400)
    pos_2 = (1900, 450, 2400, 750)
    pos_3 = (1900, 750, 2400, 1100)
    pos_4 = (1900, 1100, 2400, 1450)
    result = dict()
    result[f'pos_1'] = {'state': not check_state(background,
                                                 pos_1[0], pos_1[1],
                                                 pos_1[2], pos_1[3],
                                                 0.4),
                        'position': (random.randint(2200, 2300),
                                     random.randint(150, 350))}
    result[f'pos_2'] = {'state': not check_state(background,
                                                 pos_2[0], pos_2[1],
                                                 pos_2[2], pos_2[3],
                                                 0.4),
                        'position': (random.randint(2200, 2300),
                                     random.randint(550, 650))}
    result[f'pos_3'] = {'state': not check_state(background,
                                                 pos_3[0], pos_3[1],
                                                 pos_3[2], pos_3[3],
                                                 0.4),
                        'position': (random.randint(2200, 2300),
                                     random.randint(850, 1000))}
    result[f'pos_4'] = {'state': not check_state(background,
                                                 pos_4[0], pos_4[1],
                                                 pos_4[2], pos_4[3],
                                                 0.4),
                        'position': (random.randint(2200, 2300),
                                     random.randint(1200, 1300))}

    return result


def get_states(ui_images: dict):
    result = dict()
    result['in_battle'] = check_state(
        ui_images['InBattle.png']['as_array'], 2400, 0, 2560, 200)
    result['in_skip'] = check_state(
        ui_images['Skip.png']['as_array'], 200, 1200, 2560, 1440)
    result['in_victory'] = check_state(
        ui_images['Victory.png']['as_array'], 200, 1200, 2560, 1440)
    result['in_lvl'] = check_state(
        ui_images['LevelUp.png']['as_array'], 200, 1200, 2560, 1440)
    result['in_explore'] = check_state(
        ui_images['DifficultySettings.png']['as_array'], 400, 500, 700, 800) \
        and not check_state(ui_images['ExploreText.png']['as_array'], 700, 1100, 1000, 1250)
    result['in_difficulty'] = check_state(
        ui_images['ExploreDifficulty.png']['as_array'], 600, 150, 2000, 400)
    result['in_explore_2'] = check_state(
        ui_images['Explore.png']['as_array'], 700, 500, 1100, 800) \
        and check_state(ui_images['ExploreText.png']['as_array'], 700, 1100, 1000, 1250)
    result['in_battle_prepare'] = check_state(
        ui_images['ToBattle.png']['as_array'], 200, 1200, 2560, 1440)
    result['in_popup'] = check_state(
        ui_images['ContinueBig.png']['as_array'], 1100, 850, 2000, 1050)
    result['in_explore_mini'] = check_state(
        ui_images['MiniBoss.png']['as_array'], 1100, 500, 1500, 800) \
        and check_state(ui_images['MiniBossText.png']['as_array'], 700, 1100, 1200, 1250)
    logger.info(f'States: {result}')
    return result
