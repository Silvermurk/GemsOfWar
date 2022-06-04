# -*- coding: utf-8 -*-
import random
import time

import pyautogui as pag

from ImageFinder import check_value
from conftest import random_circle
from log import logger

rx, ry = random_circle(0, 0)
ox = 720
oy = 160
step = 160


def click(x: int, y: int):
    pag.click(x + random.randint(-5, 5),
              y + random.randint(-5, 5),
              duration=random.randint(1, 10) / 30)


def make_move(move: dict):
    logger.info(f"Making move: {move['from']['y']}, {move['from']['x']} - "
                f"{move['to']['y']}, {move['to']['x']}")
    click(ox + move['from']['y'] * step,
          oy + move['from']['x'] * step)
    click(ox + move['to']['y'] * step,
          oy + move['to']['x'] * step)


def remove_mouse():
    logger.info('Removing mouse from field')
    pag.moveTo(random.randint(1, 100),
               random.randint(100, 1000),
               random.randint(1, 10) / 30)


def get_into_batle(first: bool = True):
    from main import UiImages
    explore_in_city = pag.locateCenterOnScreen(f'{UiImages}\\Explore.png')
    if explore_in_city is not None:
        logger.info('In city, exploring')
        click(explore_in_city[0], explore_in_city[1])
        pag.sleep(1)
    if first:
        x, y = pag.locateCenterOnScreen(f'{UiImages}\\DifficultySettings.png')
        click(x, y)
        pag.sleep(1)
        # x, y = pag.locateCenterOnScreen(f'{UiImages}\\Difficulty2.png')
        # click(x, y)
        # pag.sleep(1)
        x, y = pag.locateCenterOnScreen(f'{UiImages}\\Continue.png')
        click(x, y)
    pag.sleep(2)
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\ExploreInner.png')
    click(x, y)
    pag.sleep(1)
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\ToBattle.png')
    click(x, y)
    time.sleep(5)
    logger.info('Battle start')
    return check_value('InBattle.png')


def next_battle():
    from main import UiImages
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\Victory.png')
    click(x, y)


def level_up():
    from main import UiImages
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\LevelUp.png')
    click(x, y)
    time.sleep(1)
    click(800, 600)
    weapon = pag.locateCenterOnScreen(f'{UiImages}\\Victory.png')
    if weapon:
        click(weapon[0], weapon[1])
    time.sleep(1)


def reset_exploration():
    from main import UiImages
    pag.press('esc')
    pag.sleep(1)
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\Retreat.png')
    click(x, y)
    pag.sleep(1)
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\Yes.png')
    click(x, y)
    pag.sleep(3)
    x, y = pag.locateCenterOnScreen(f'{UiImages}\\Okay.png')
    click(x, y)
    pag.sleep(3)
