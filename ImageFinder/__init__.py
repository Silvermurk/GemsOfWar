# -*- coding: utf-8 -*-
from os import getcwd

import cv2
import pyautogui as pag
from conftest import image_to_string, split_image
from numpy import asarray
from PIL import Image, ImageGrab

from log import logger


def image_to_array(image: Image, tiles: dict, img_shot: str = None):
    image_board = image.crop((640, 100, 1920, 1380))
    if img_shot:
        image_board = Image.open(f'{getcwd()}\\Presets\\{img_shot}')
    img_grid = split_image(image_board, 160)
    img_array = asarray(img_grid).reshape((8, 8))
    str_array = image_to_string(img_array, tiles)
    return str_array


def get_active_skills(image: Image,
                      skills: dict,
                      accuracy: float = 0.7) -> dict:
    image_skills = image.crop((0, 0, 640, 1480))
    skill_list = asarray(image_skills)
    ready_skills = dict()
    for skill in skills:
        skill_img = skills[skill]['as_array']
        result = cv2.matchTemplate(skill_img,
                                   skill_list,
                                   cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= accuracy:
            ready_skills[image] = True
    return ready_skills


def is_my_turn():
    from main import UiImages
    image = ImageGrab.grab()
    turn = asarray(image.crop((320, 0, 500, 150)))
    turn_value = asarray(Image.open(f'{UiImages}\\MyTurn.png'))
    result = cv2.matchTemplate(turn_value,
                               turn,
                               cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= 0.8:
        return True
    return False


def check_value(image: str, many: bool = False):
    from main import UiImages
    in_battle = 0
    out_battle = 0
    if many:
        while in_battle < 3 and out_battle < 3:
            battle = pag.locateCenterOnScreen(f'{UiImages}\\{image}')
            if battle:
                in_battle += 1
                logger.info(f'{image}')
                pag.sleep(0.1)
            else:
                out_battle += 1
                logger.info(f'Not {image}')
                pag.sleep(0.1)
        if in_battle >= 3:
            return True
        if out_battle >= 3:
            return False
    else:
        battle = pag.locateCenterOnScreen(f'{UiImages}\\{image}')
        if battle:
            logger.info(f'{image}')
            return True
        else:
            logger.info(f'Not {image}')
            return False

def max_battles():
    from main import UiImages
    battles = pag.locateCenterOnScreen(f'{UiImages}\\MaxBattles.png')
    if battles:
        logger.info('Max battles')
        return True
    logger.info('Not max battles')
    return False
