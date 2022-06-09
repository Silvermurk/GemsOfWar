# -*- coding: utf-8 -*-
import random
import time

import pyautogui as pag
from log import logger

ox = 720
oy = 160
step = 160


def click(x: int, y: int):
    pag.click(x + random.randint(-5, 5),
              y + random.randint(-5, 5),
              duration=random.randint(1, 10) / 50)


def make_move(move: dict):
    logger.info(f"Making move: {move['from']['y']}, {move['from']['x']} - "
                f"{move['to']['y']}, {move['to']['x']}")
    click(ox + move['from']['y'] * step,
          oy + move['from']['x'] * step)
    click(ox + move['to']['y'] * step,
          oy + move['to']['x'] * step)


def click_ui(ui_images: dict, name: str):
    from main import UiImages
    ui_element = pag.locateCenterOnScreen(f'{UiImages}\\{ui_images[name]["file_name"]}')
    if ui_element:
        click(ui_element[0], ui_element[1])
    time.sleep(0.3)


def set_difficulty(ui_images: dict, difficulty: int):
    click_ui(ui_images, ui_images[f"Difficulty{difficulty}.png"]["file_name"])
    time.sleep(0.5)
    click_ui(ui_images, ui_images[f"Continue.png"]["file_name"])


def remove_mouse():
    logger.info('Removing mouse from field')
    pag.moveTo(random.randint(1, 100),
               random.randint(100, 1000),
               random.randint(1, 10) / 30)
