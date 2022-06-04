# -*- coding: utf-8 -*-
import time
from os import getcwd

from AIBrain import get_all_moves, use_skill, filter_color
from ImageFinder import image_to_array, get_active_skills, is_my_turn, check_value, max_battles
from MoveMaker import make_move, remove_mouse, get_into_batle, next_battle, level_up, reset_exploration
from conftest import load_files
import pyautogui as pag
from log import logger
from PIL import ImageGrab

GemTiles = f'{getcwd()}\\GemTiles'
SkillTiles = f'{getcwd()}\\SkillTiles'
UiImages = f'{getcwd()}\\UiImages'
AutoSkills = [
    'PopWeasel.png',
    'ShadowStrike.png',
    'QuickSand.png']
ColorPrefs = ['sku', 'red', 'bro', 'blu', 'vio', 'yel', 'gre']

if __name__ == '__main__':
    tiles = load_files(GemTiles)
    skills = load_files(SkillTiles)
    ui_images = load_files(UiImages)
    time.sleep(1)

    # Main loop
    while True:
        # if not is_my_turn():
        #     time.sleep(1)
        #     continue
        # remove_mouse()
        time.sleep(0.3)
        image = ImageGrab.grab()
        while get_active_skills(image, skills):
            for skill in AutoSkills:
                use_skill(skill)
                time.sleep(0.3)
        time.sleep(1)
        image = ImageGrab.grab()
        str_array = image_to_array(image, tiles, 'Board.png')
        move_set, length = get_all_moves(str_array)
        move = None
        if move_set is not None:
            move = filter_color(move_set, ColorPrefs)
        else:
            exit(1)
        if length == 5:
            logger.info('Checking 5 moves')
            make_move(move)
        if length == 4:
            logger.info('Checking 4 moves')
            make_move(move)
        if length == 3:
            logger.info('Checking 3 moves')
            make_move(move)
        if check_value('Skip.png'):
            break
