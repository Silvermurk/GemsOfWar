# -*- coding: utf-8 -*-
import os
import random
from itertools import product
from os import listdir

import cv2
import numpy as np
from PIL import Image
from numpy import asarray


def load_files(path: str) -> dict:
    tile_list = dict()
    for file in listdir(path):
        if file.endswith('.png'):
            tile_list[file] = dict()
            tile_list[file]['name'] = file[:3]
            tile_list[file]['image'] = Image.open(f'{path}\\{file}')
            tile_list[file]['as_array'] = asarray(tile_list[file]['image'])
    return tile_list


def split_image(image: Image, d: int) -> list:
    w, h = image.size
    img_list = list()

    grid = product(range(0, h - h % d, d), range(0, w - w % d, d))
    for i, j in grid:
        box = (j, i, j + d, i + d)
        img_crop = image.crop(box)
        img_list.append(img_crop)
    return img_list


def image_to_string(img_array: np.ndarray,
                    tile_list: dict,
                    accuracy: float = 0.7) -> np.ndarray:
    str_array = np.ndarray((8, 8), dtype=object)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            array_img = asarray(img_array[i, j])
            for tile in tile_list:
                tile_img = tile_list[tile]['as_array']
                result = cv2.matchTemplate(tile_img,
                                           array_img,
                                           cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val >= accuracy:
                    str_array[i, j] = str(tile.lower()[:3])
                    if str_array[i, j] == 'dem' or str_array[i, j] == 'gla':
                        str_array[i, j] = 'sku'
    return str_array


def show_str_array(board: np.ndarray):
    result = str()
    for x in range(board.shape[0]):
        result += '\n'
        for y in range(board.shape[1]):
            result += f'{board[x, y]} '
    return result


def random_circle(x: int, y: int, size: int = 5):
    return x + random.randint(-size, size), y + random.randint(-size, size)
