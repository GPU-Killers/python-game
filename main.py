import pygame
import sys
from random import *
from pygame import K_ESCAPE as esc
from pygame import K_LSHIFT as lshift
from pygame import K_RETURN as enter
from pygame import K_RSHIFT as rshift

from keymgr import *
from textmod import *


class GameObj:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite


pygame.init()
display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
clock = pygame.time.Clock()

(width, height) = pygame.display.get_window_size()

gameData = {
    'width': width,
    'height': height,
    'sprite_size': 64,
    'sprite_center_x': width / 2 - 64 / 2,
    'sprite_center_y': height / 2 - 64 / 2,
    'com_reduce': 0.3,
    'vel': 2,
    'coins': 0,
    'points': 0
}

colors = {
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "black": (0, 0, 0)
}


class Spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:' + filename)
            raise SystemExit(message)

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey=-1):
        rect = pygame.Rect(
            (rectangle[1], rectangle[0], rectangle[2], rectangle[3]))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


ss = Spritesheet('./media/images/entity/sprites.png')

sprites_collection = {
    'spellcast_back': [
        ss.image_at((0, 0, 64, 64)),
        ss.image_at((0, 64, 64, 64)),
        ss.image_at((0, 128, 64, 64)),
        ss.image_at((0, 192, 64, 64)),
        ss.image_at((0, 256, 64, 64)),
        ss.image_at((0, 320, 64, 64)),
        ss.image_at((0, 384, 64, 64))
    ],
    'spellcast_left': [
        ss.image_at((64, 0, 64, 64)),
        ss.image_at((64, 64, 64, 64)),
        ss.image_at((64, 128, 64, 64)),
        ss.image_at((64, 192, 64, 64)),
        ss.image_at((64, 256, 64, 64)),
        ss.image_at((64, 320, 64, 64)),
        ss.image_at((64, 384, 64, 64))
    ],
    'spellcast_front': [
        ss.image_at((128, 0, 64, 64)),
        ss.image_at((128, 64, 64, 64)),
        ss.image_at((128, 128, 64, 64)),
        ss.image_at((128, 192, 64, 64)),
        ss.image_at((128, 256, 64, 64)),
        ss.image_at((128, 320, 64, 64)),
        ss.image_at((128, 384, 64, 64))
    ],
    'spellcast_right': [
        ss.image_at((192, 0, 64, 64)),
        ss.image_at((192, 64, 64, 64)),
        ss.image_at((192, 128, 64, 64)),
        ss.image_at((192, 192, 64, 64)),
        ss.image_at((192, 256, 64, 64)),
        ss.image_at((192, 320, 64, 64)),
        ss.image_at((192, 384, 64, 64))
    ],
    'thrust_back': [
        ss.image_at((256, 0, 64, 64)),
        ss.image_at((256, 64, 64, 64)),
        ss.image_at((256, 128, 64, 64)),
        ss.image_at((256, 192, 64, 64)),
        ss.image_at((256, 256, 64, 64)),
        ss.image_at((256, 320, 64, 64)),
        ss.image_at((256, 384, 64, 64)),
        ss.image_at((256, 448, 64, 64))
    ],
    'thrust_left': [
        ss.image_at((320, 0, 64, 64)),
        ss.image_at((320, 64, 64, 64)),
        ss.image_at((320, 128, 64, 64)),
        ss.image_at((320, 192, 64, 64)),
        ss.image_at((320, 256, 64, 64)),
        ss.image_at((320, 320, 64, 64)),
        ss.image_at((320, 384, 64, 64)),
        ss.image_at((320, 448, 64, 64))
    ],
    'thrust_front': [
        ss.image_at((384, 0, 64, 64)),
        ss.image_at((384, 64, 64, 64)),
        ss.image_at((384, 128, 64, 64)),
        ss.image_at((384, 192, 64, 64)),
        ss.image_at((384, 256, 64, 64)),
        ss.image_at((384, 320, 64, 64)),
        ss.image_at((384, 384, 64, 64)),
        ss.image_at((384, 448, 64, 64))
    ],
    'thrust_right': [
        ss.image_at((448, 0, 64, 64)),
        ss.image_at((448, 64, 64, 64)),
        ss.image_at((448, 128, 64, 64)),
        ss.image_at((448, 192, 64, 64)),
        ss.image_at((448, 256, 64, 64)),
        ss.image_at((448, 320, 64, 64)),
        ss.image_at((448, 384, 64, 64)),
        ss.image_at((448, 448, 64, 64))
    ],
    'walk_back': [
        ss.image_at((512, 0, 64, 64)),
        ss.image_at((512, 64, 64, 64)),
        ss.image_at((512, 128, 64, 64)),
        ss.image_at((512, 192, 64, 64)),
        ss.image_at((512, 256, 64, 64)),
        ss.image_at((512, 320, 64, 64)),
        ss.image_at((512, 384, 64, 64)),
        ss.image_at((512, 448, 64, 64)),
        ss.image_at((512, 512, 64, 64))
    ],
    'walk_left': [
        ss.image_at((576, 0, 64, 64)),
        ss.image_at((576, 64, 64, 64)),
        ss.image_at((576, 128, 64, 64)),
        ss.image_at((576, 192, 64, 64)),
        ss.image_at((576, 256, 64, 64)),
        ss.image_at((576, 320, 64, 64)),
        ss.image_at((576, 384, 64, 64)),
        ss.image_at((576, 448, 64, 64)),
        ss.image_at((576, 512, 64, 64))
    ],
    'walk_front': [
        ss.image_at((640, 0, 64, 64)),
        ss.image_at((640, 64, 64, 64)),
        ss.image_at((640, 128, 64, 64)),
        ss.image_at((640, 192, 64, 64)),
        ss.image_at((640, 256, 64, 64)),
        ss.image_at((640, 320, 64, 64)),
        ss.image_at((640, 384, 64, 64)),
        ss.image_at((640, 448, 64, 64)),
        ss.image_at((640, 512, 64, 64))
    ],
    'walk_right': [
        ss.image_at((704, 0, 64, 64)),
        ss.image_at((704, 64, 64, 64)),
        ss.image_at((704, 128, 64, 64)),
        ss.image_at((704, 192, 64, 64)),
        ss.image_at((704, 256, 64, 64)),
        ss.image_at((704, 320, 64, 64)),
        ss.image_at((704, 384, 64, 64)),
        ss.image_at((704, 448, 64, 64)),
        ss.image_at((704, 512, 64, 64))
    ],
    'slash_back': [
        ss.image_at((768, 0, 64, 64)),
        ss.image_at((768, 64, 64, 64)),
        ss.image_at((768, 128, 64, 64)),
        ss.image_at((768, 192, 64, 64)),
        ss.image_at((768, 256, 64, 64)),
        ss.image_at((768, 320, 64, 64))
    ],
    'slash_left': [
        ss.image_at((832, 0, 64, 64)),
        ss.image_at((832, 64, 64, 64)),
        ss.image_at((832, 128, 64, 64)),
        ss.image_at((832, 192, 64, 64)),
        ss.image_at((832, 256, 64, 64)),
        ss.image_at((832, 320, 64, 64))
    ],
    'slash_front': [
        ss.image_at((896, 0, 64, 64)),
        ss.image_at((896, 64, 64, 64)),
        ss.image_at((896, 128, 64, 64)),
        ss.image_at((896, 192, 64, 64)),
        ss.image_at((896, 256, 64, 64)),
        ss.image_at((896, 320, 64, 64))
    ],
    'slash_right': [
        ss.image_at((960, 0, 64, 64)),
        ss.image_at((960, 64, 64, 64)),
        ss.image_at((960, 128, 64, 64)),
        ss.image_at((960, 192, 64, 64)),
        ss.image_at((960, 256, 64, 64)),
        ss.image_at((960, 320, 64, 64))
    ],
    'smash_back': [
        ss.image_at((768, 320, 64, 64)),
        ss.image_at((768, 256, 64, 64)),
        ss.image_at((768, 192, 64, 64)),
        ss.image_at((768, 128, 64, 64)),
        ss.image_at((768, 64, 64, 64)),
        ss.image_at((768, 0, 64, 64))
    ],
    'smash_left': [
        ss.image_at((832, 320, 64, 64)),
        ss.image_at((832, 256, 64, 64)),
        ss.image_at((832, 192, 64, 64)),
        ss.image_at((832, 128, 64, 64)),
        ss.image_at((832, 64, 64, 64)),
        ss.image_at((832, 0, 64, 64))
    ],
    'smash_front': [
        ss.image_at((896, 320, 64, 64)),
        ss.image_at((896, 256, 64, 64)),
        ss.image_at((896, 192, 64, 64)),
        ss.image_at((896, 128, 64, 64)),
        ss.image_at((896, 64, 64, 64)),
        ss.image_at((896, 0, 64, 64))
    ],
    'smash_right': [
        ss.image_at((960, 320, 64, 64)),
        ss.image_at((960, 256, 64, 64)),
        ss.image_at((960, 192, 64, 64)),
        ss.image_at((960, 128, 64, 64)),
        ss.image_at((960, 64, 64, 64)),
        ss.image_at((960, 0, 64, 64))
    ],
    'shoot_back': [
        ss.image_at((1024, 0, 64, 64)),
        ss.image_at((1024, 64, 64, 64)),
        ss.image_at((1024, 128, 64, 64)),
        ss.image_at((1024, 192, 64, 64)),
        ss.image_at((1024, 256, 64, 64)),
        ss.image_at((1024, 320, 64, 64)),
        ss.image_at((1024, 384, 64, 64)),
        ss.image_at((1024, 448, 64, 64)),
        ss.image_at((1024, 512, 64, 64)),
        ss.image_at((1024, 576, 64, 64)),
        ss.image_at((1024, 640, 64, 64)),
        ss.image_at((1024, 704, 64, 64)),
        ss.image_at((1024, 768, 64, 64))
    ],
    'shoot_left': [
        ss.image_at((1088, 0, 64, 64)),
        ss.image_at((1088, 64, 64, 64)),
        ss.image_at((1088, 128, 64, 64)),
        ss.image_at((1088, 192, 64, 64)),
        ss.image_at((1088, 256, 64, 64)),
        ss.image_at((1088, 320, 64, 64)),
        ss.image_at((1088, 384, 64, 64)),
        ss.image_at((1088, 448, 64, 64)),
        ss.image_at((1088, 512, 64, 64)),
        ss.image_at((1088, 576, 64, 64)),
        ss.image_at((1088, 640, 64, 64)),
        ss.image_at((1088, 704, 64, 64)),
        ss.image_at((1088, 768, 64, 64))
    ],
    'shoot_front': [
        ss.image_at((1152, 0, 64, 64)),
        ss.image_at((1152, 64, 64, 64)),
        ss.image_at((1152, 128, 64, 64)),
        ss.image_at((1152, 192, 64, 64)),
        ss.image_at((1152, 256, 64, 64)),
        ss.image_at((1152, 320, 64, 64)),
        ss.image_at((1152, 384, 64, 64)),
        ss.image_at((1152, 448, 64, 64)),
        ss.image_at((1152, 512, 64, 64)),
        ss.image_at((1152, 576, 64, 64)),
        ss.image_at((1152, 640, 64, 64)),
        ss.image_at((1152, 704, 64, 64)),
        ss.image_at((1152, 768, 64, 64))
    ],
    'shoot_right': [
        ss.image_at((1216, 0, 64, 64)),
        ss.image_at((1216, 64, 64, 64)),
        ss.image_at((1216, 128, 64, 64)),
        ss.image_at((1216, 192, 64, 64)),
        ss.image_at((1216, 256, 64, 64)),
        ss.image_at((1216, 320, 64, 64)),
        ss.image_at((1216, 384, 64, 64)),
        ss.image_at((1216, 448, 64, 64)),
        ss.image_at((1216, 512, 64, 64)),
        ss.image_at((1216, 576, 64, 64)),
        ss.image_at((1216, 640, 64, 64)),
        ss.image_at((1216, 704, 64, 64)),
        ss.image_at((1216, 768, 64, 64))
    ],
    'hurt': [
        ss.image_at((1280, 0, 64, 64)),
        ss.image_at((1280, 64, 64, 64)),
        ss.image_at((1280, 128, 64, 64)),
        ss.image_at((1280, 192, 64, 64)),
        ss.image_at((1280, 256, 64, 64)),
        ss.image_at((1280, 320, 64, 64))
    ]
}

sprites = {
    'spell': {
        'back': sprites_collection['spellcast_back'],
        'left': sprites_collection['spellcast_left'],
        'front': sprites_collection['spellcast_front'],
        'right': sprites_collection['spellcast_right']
    },
    'thrust': {
        'back': sprites_collection['thrust_back'],
        'left': sprites_collection['thrust_left'],
        'front': sprites_collection['thrust_front'],
        'right': sprites_collection['thrust_right']
    },
    'walk': {
        'back': sprites_collection['walk_back'],
        'left': sprites_collection['walk_left'],
        'front': sprites_collection['walk_front'],
        'right': sprites_collection['walk_right']
    },
    'slash': {
        'back': sprites_collection['slash_back'],
        'left': sprites_collection['slash_left'],
        'front': sprites_collection['slash_front'],
        'right': sprites_collection['slash_right']
    },
    'smash': {
        'back': sprites_collection['smash_back'],
        'left': sprites_collection['smash_left'],
        'front': sprites_collection['smash_front'],
        'right': sprites_collection['smash_right']
    },
    'shoot': {
        'back': sprites_collection['shoot_back'],
        'left': sprites_collection['shoot_left'],
        'front': sprites_collection['shoot_front'],
        'right': sprites_collection['shoot_right']
    },
    'hurt': {
        'main': sprites_collection['hurt']
    }
}

iss = Spritesheet('./media/images/items/items.png')

items = {
    'chestplate': {
        'cp_1': iss.image_at((0, 0, 32, 32)),
        'cp_2': iss.image_at((0, 32, 32, 32)),
        'cp_3': iss.image_at((0, 64, 32, 32)),
        'cp_4': iss.image_at((0, 96, 32, 32)),
        'cp_5': iss.image_at((0, 128, 32, 32))
    },
    'arrow': {
        'ag1_1': iss.image_at((0, 160, 32, 32)),
        'ag1_2': iss.image_at((0, 192, 32, 32)),
        'ag1_3': iss.image_at((0, 224, 32, 32)),
        'ag1_4': iss.image_at((0, 256, 32, 32)),
        'ag1_5': iss.image_at((0, 288, 32, 32)),
        'ag2_1': iss.image_at((0, 320, 32, 32)),
        'ag2_2': iss.image_at((0, 352, 32, 32)),
        'ag2_3': iss.image_at((0, 384, 32, 32)),
        'ag2_4': iss.image_at((0, 416, 32, 32)),
        'ag2_5': iss.image_at((0, 448, 32, 32)),
        'ag3_1': iss.image_at((0, 480, 32, 32)),
        'ag3_2': iss.image_at((32, 0, 32, 32)),
        'ag3_3': iss.image_at((32, 32, 32, 32)),
        'ag3_4': iss.image_at((32, 64, 32, 32)),
        'ag3_5': iss.image_at((32, 96, 32, 32))
    },
    'bone': iss.image_at((32, 128, 32, 32)),
    'book': {
        'brown_1': iss.image_at((32, 160, 32, 32)),
        'brown_2': iss.image_at((32, 192, 32, 32)),
        'brown_3': iss.image_at((32, 224, 32, 32)),
        'brown_4': iss.image_at((32, 256, 32, 32)),
        'brown_5': iss.image_at((32, 288, 32, 32)),
        'brown_6': iss.image_at((32, 320, 32, 32)),
        'brown_7': iss.image_at((32, 352, 32, 32)),
        'green_1': iss.image_at((32, 384, 32, 32)),
        'green_2': iss.image_at((32, 416, 32, 32)),
        'green_3': iss.image_at((32, 448, 32, 32)),
        'green_4': iss.image_at((32, 480, 32, 32)),
        'green_5': iss.image_at((64, 0, 32, 32)),
        'green_6': iss.image_at((64, 32, 32, 32)),
        'green_7': iss.image_at((64, 64, 32, 32)),
        'red_1': iss.image_at((64, 96, 32, 32)),
        'red_2': iss.image_at((64, 128, 32, 32)),
        'red_3': iss.image_at((64, 160, 32, 32)),
        'red_4': iss.image_at((64, 192, 32, 32)),
        'red_5': iss.image_at((64, 224, 32, 32)),
        'red_6': iss.image_at((64, 256, 32, 32)),
        'red_7': iss.image_at((64, 288, 32, 32)),
        'blue_1': iss.image_at((64, 320, 32, 32)),
        'blue_2': iss.image_at((64, 352, 32, 32)),
        'blue_3': iss.image_at((64, 384, 32, 32)),
        'blue_4': iss.image_at((64, 416, 32, 32)),
        'blue_5': iss.image_at((64, 448, 32, 32)),
        'blue_6': iss.image_at((64, 480, 32, 32)),
        'blue_7': iss.image_at((96, 0, 32, 32)),
        'grey_1': iss.image_at((96, 32, 32, 32)),
        'grey_2': iss.image_at((96, 64, 32, 32)),
        'grey_3': iss.image_at((96, 96, 32, 32)),
        'grey_4': iss.image_at((96, 128, 32, 32)),
        'grey_5': iss.image_at((96, 160, 32, 32)),
        'grey_6': iss.image_at((96, 192, 32, 32)),
        'grey_7': iss.image_at((96, 224, 32, 32)),
        'black_1': iss.image_at((96, 256, 32, 32)),
        'black_2': iss.image_at((96, 288, 32, 32)),
        'black_3': iss.image_at((96, 320, 32, 32)),
        'black_4': iss.image_at((96, 352, 32, 32)),
        'black_5': iss.image_at((96, 384, 32, 32)),
        'black_6': iss.image_at((96, 416, 32, 32)),
        'black_7': iss.image_at((96, 448, 32, 32))
    },
    'shoe': {
        's_1': iss.image_at((96, 480, 32, 32)),
        's_2': iss.image_at((128, 0, 32, 32)),
        's_3': iss.image_at((128, 32, 32, 32)),
        's_4': iss.image_at((128, 64, 32, 32)),
        's_5': iss.image_at((128, 96, 32, 32))
    },
    'bow': {
        'b1_1': iss.image_at((128, 128, 32, 32)),
        'b1_2': iss.image_at((128, 160, 32, 32)),
        'b1_3': iss.image_at((128, 192, 32, 32)),
        'b1_4': iss.image_at((128, 224, 32, 32)),
        'b1_5': iss.image_at((128, 256, 32, 32)),
        'b2_1': iss.image_at((128, 288, 32, 32)),
        'b2_2': iss.image_at((128, 320, 32, 32)),
        'b2_3': iss.image_at((128, 352, 32, 32)),
        'b2_4': iss.image_at((128, 384, 32, 32)),
        'b2_5': iss.image_at((128, 416, 32, 32)),
        'b3_1': iss.image_at((128, 448, 32, 32)),
        'b3_2': iss.image_at((128, 480, 32, 32)),
        'b3_3': iss.image_at((160, 0, 32, 32)),
        'b3_4': iss.image_at((160, 32, 32, 32)),
        'b3_5': iss.image_at((160, 64, 32, 32))
    },
    "candle": {
        "out": iss.image_at((160, 96, 32, 32)),
        "lit": iss.image_at((160, 128, 32, 32))
    },
    "candy": {
        "cane_1": iss.image_at((160, 160, 32, 32)),
        "cane_2": iss.image_at((160, 192, 32, 32)),
        "cane_3": iss.image_at((160, 224, 32, 32)),
        "cane_4": iss.image_at((160, 256, 32, 32)),
        "cane_5": iss.image_at((160, 288, 32, 32)),
        "cane_6": iss.image_at((160, 320, 32, 32)),
        "cane_7": iss.image_at((160, 352, 32, 32)),
        "hard_1": iss.image_at((160, 384, 32, 32)),
        "hard_2": iss.image_at((160, 416, 32, 32)),
        "hard_3": iss.image_at((160, 448, 32, 32)),
        "hard_4": iss.image_at((160, 480, 32, 32)),
        "hard_5": iss.image_at((192, 0, 32, 32)),
        "hard_6": iss.image_at((192, 32, 32, 32)),
        "hard_7": iss.image_at((192, 64, 32, 32))
    },
    "coin": {
        "c1_1": iss.image_at((192, 96, 32, 32)),
        "c1_2": iss.image_at((192, 128, 32, 32)),
        "c1_3": iss.image_at((192, 160, 32, 32)),
        "c1_4": iss.image_at((192, 192, 32, 32)),
        "c1_5": iss.image_at((192, 224, 32, 32)),
        "c2_1": iss.image_at((192, 256, 32, 32)),
        "c2_2": iss.image_at((192, 288, 32, 32)),
        "c2_3": iss.image_at((192, 320, 32, 32)),
        "c2_4": iss.image_at((192, 352, 32, 32)),
        "c2_5": iss.image_at((192, 384, 32, 32)),
        "c3_1": iss.image_at((192, 416, 32, 32)),
        "c3_2": iss.image_at((192, 448, 32, 32)),
        "c3_3": iss.image_at((192, 480, 32, 32)),
        "c3_4": iss.image_at((224, 0, 32, 32)),
        "c3_5": iss.image_at((224, 32, 32, 32)),
        "c4_1": iss.image_at((224, 64, 32, 32)),
        "c4_2": iss.image_at((224, 96, 32, 32)),
        "c4_3": iss.image_at((224, 128, 32, 32)),
        "c4_4": iss.image_at((224, 160, 32, 32)),
        "c4_5": iss.image_at((224, 192, 32, 32)),
        "c5_1": iss.image_at((224, 224, 32, 32)),
        "c5_2": iss.image_at((224, 256, 32, 32)),
        "c5_3": iss.image_at((224, 288, 32, 32)),
        "c5_4": iss.image_at((224, 320, 32, 32)),
        "c5_5": iss.image_at((224, 352, 32, 32))
    },
    "cookie": iss.image_at((224, 384, 32, 32)),
    "cotton": iss.image_at((224, 416, 32, 32)),
    "diamond": {
        "d_1": iss.image_at((224, 448, 32, 32)),
        "d_2": iss.image_at((224, 480, 32, 32)),
        "d_3": iss.image_at((256, 0, 32, 32)),
        "d_4": iss.image_at((256, 32, 32, 32)),
        "d_5": iss.image_at((256, 64, 32, 32)),
        "d_6": iss.image_at((256, 96, 32, 32)),
        "d_7": iss.image_at((256, 128, 32, 32)),
        "d_8": iss.image_at((256, 160, 32, 32)),
        "d_9": iss.image_at((256, 192, 32, 32)),
        "d_10": iss.image_at((256, 224, 32, 32))
    },
    "soda": {
        "empty": iss.image_at((256, 256, 32, 32)),
        "full": iss.image_at((256, 288, 32, 32))
    },
    "wine": {
        "empty": iss.image_at((256, 320, 32, 32)),
        "full": iss.image_at((256, 352, 32, 32))
    },
    "fish": {
        "f_1": iss.image_at((256, 384, 32, 32)),
        "f_2": iss.image_at((256, 416, 32, 32)),
        "f_3": iss.image_at((256, 448, 32, 32)),
        "f_4": iss.image_at((256, 480, 32, 32)),
        "f_5": iss.image_at((288, 0, 32, 32))
    },
    "flower": {
        "red": iss.image_at((288, 32, 32, 32)),
        "yellow": iss.image_at((288, 64, 32, 32))
    },
    "apple": iss.image_at((288, 96, 32, 32)),
    "banana": iss.image_at((288, 128, 32, 32)),
    "gemstone": {
        "g_1": iss.image_at((288, 160, 32, 32)),
        "g_2": iss.image_at((288, 192, 32, 32)),
        "g_3": iss.image_at((288, 224, 32, 32)),
        "g_4": iss.image_at((288, 256, 32, 32)),
        "g_5": iss.image_at((288, 288, 32, 32)),
        "g_6": iss.image_at((288, 320, 32, 32)),
        "g_7": iss.image_at((288, 352, 32, 32)),
        "g_8": iss.image_at((288, 384, 32, 32)),
        "g_9": iss.image_at((288, 416, 32, 32)),
        "g_10": iss.image_at((288, 448, 32, 32))
    },
    "gift": {
        "g1_1": iss.image_at((288, 480, 32, 32)),
        "g1_2": iss.image_at((320, 0, 32, 32)),
        "g1_3": iss.image_at((320, 32, 32, 32)),
        "g1_4": iss.image_at((320, 64, 32, 32)),
        "g1_5": iss.image_at((320, 96, 32, 32)),
        "g1_6": iss.image_at((320, 128, 32, 32)),
        "g2_1": iss.image_at((320, 160, 32, 32)),
        "g2_2": iss.image_at((320, 192, 32, 32)),
        "g2_3": iss.image_at((320, 224, 32, 32)),
        "g2_4": iss.image_at((320, 256, 32, 32)),
        "g2_5": iss.image_at((320, 288, 32, 32)),
        "g2_6": iss.image_at((320, 320, 32, 32))
    },
    "glove": {
        "g_1": iss.image_at((320, 352, 32, 32)),
        "g_2": iss.image_at((320, 384, 32, 32)),
        "g_3": iss.image_at((320, 416, 32, 32)),
        "g_4": iss.image_at((320, 448, 32, 32)),
        "g_5": iss.image_at((320, 480, 32, 32))
    },
    "hat": {
        "h_1": iss.image_at((352, 0, 32, 32)),
        "h_2": iss.image_at((352, 32, 32, 32)),
        "h_3": iss.image_at((352, 64, 32, 32)),
        "h_4": iss.image_at((352, 96, 32, 32)),
        "h_5": iss.image_at((352, 128, 32, 32)),
        "h_6": iss.image_at((352, 160, 32, 32))
    },
    "helmet": {
        "h1_1": iss.image_at((352, 192, 32, 32)),
        "h1_2": iss.image_at((352, 224, 32, 32)),
        "h1_3": iss.image_at((352, 256, 32, 32)),
        "h1_4": iss.image_at((352, 288, 32, 32)),
        "h1_5": iss.image_at((352, 320, 32, 32)),
        "h2_1": iss.image_at((352, 352, 32, 32)),
        "h2_2": iss.image_at((352, 384, 32, 32)),
        "h2_3": iss.image_at((352, 416, 32, 32)),
        "h2_4": iss.image_at((352, 448, 32, 32)),
        "h2_5": iss.image_at((352, 480, 32, 32))
    },
    "ingot": {
        "i_1": iss.image_at((384, 0, 32, 32)),
        "i_2": iss.image_at((384, 32, 32, 32)),
        "i_3": iss.image_at((384, 64, 32, 32)),
        "i_4": iss.image_at((384, 96, 32, 32)),
        "i_5": iss.image_at((384, 128, 32, 32))
    },
    "key": {
        "k_1": iss.image_at((384, 160, 32, 32)),
        "k_2": iss.image_at((384, 192, 32, 32)),
        "k_3": iss.image_at((384, 224, 32, 32)),
        "k_4": iss.image_at((384, 256, 32, 32)),
        "k_5": iss.image_at((384, 288, 32, 32)),
        "k_6": iss.image_at((384, 320, 32, 32)),
        "k_7": iss.image_at((384, 352, 32, 32)),
        "k_8": iss.image_at((384, 384, 32, 32)),
        "k_9": iss.image_at((384, 416, 32, 32)),
        "k_10": iss.image_at((384, 448, 32, 32))
    },
    "leaf": iss.image_at((384, 480, 32, 32)),
    "necklace": {
        "n1_1": iss.image_at((416, 0, 32, 32)),
        "n1_2": iss.image_at((416, 32, 32, 32)),
        "n1_3": iss.image_at((416, 64, 32, 32)),
        "n1_4": iss.image_at((416, 96, 32, 32)),
        "n1_5": iss.image_at((416, 128, 32, 32)),
        "n2_1": iss.image_at((416, 160, 32, 32)),
        "n2_2": iss.image_at((416, 192, 32, 32)),
        "n2_3": iss.image_at((416, 224, 32, 32)),
        "n2_4": iss.image_at((416, 256, 32, 32)),
        "n2_5": iss.image_at((416, 288, 32, 32)),
        "n3_1": iss.image_at((416, 320, 32, 32)),
        "n3_2": iss.image_at((416, 352, 32, 32)),
        "n3_3": iss.image_at((416, 384, 32, 32)),
        "n3_4": iss.image_at((416, 416, 32, 32)),
        "n3_5": iss.image_at((416, 448, 32, 32))
    },
    "cannonball": {
        # 5 cannonballs
        "c_1": iss.image_at((416, 480, 32, 32)),
        "c_2": iss.image_at((448, 0, 32, 32)),
        "c_3": iss.image_at((448, 32, 32, 32)),
        "c_4": iss.image_at((448, 64, 32, 32)),
        "c_5": iss.image_at((448, 96, 32, 32))
    },
    "plank": iss.image_at((448, 128, 32, 32)),
    "potion": {
        # 3 types ("v","s","n"), each with 8 potions using p{type}_{number}
        # e.g. pv_1 for type "v", potion 1
        "pv_1": iss.image_at((448, 160, 32, 32)),
        "pv_2": iss.image_at((448, 192, 32, 32)),
        "pv_3": iss.image_at((448, 224, 32, 32)),
        "pv_4": iss.image_at((448, 256, 32, 32)),
        "pv_5": iss.image_at((448, 288, 32, 32)),
        "pv_6": iss.image_at((448, 320, 32, 32)),
        "pv_7": iss.image_at((448, 352, 32, 32)),
        "pv_8": iss.image_at((448, 384, 32, 32)),
        "ps_1": iss.image_at((448, 416, 32, 32)),
        "ps_2": iss.image_at((448, 448, 32, 32)),
        "ps_3": iss.image_at((448, 480, 32, 32)),
        "ps_4": iss.image_at((480, 0, 32, 32)),
        "ps_5": iss.image_at((480, 32, 32, 32)),
        "ps_6": iss.image_at((480, 64, 32, 32)),
        "ps_7": iss.image_at((480, 96, 32, 32)),
        "ps_8": iss.image_at((480, 128, 32, 32)),
        "pn_1": iss.image_at((480, 160, 32, 32)),
        "pn_2": iss.image_at((480, 192, 32, 32)),
        "pn_3": iss.image_at((480, 224, 32, 32)),
        "pn_4": iss.image_at((480, 256, 32, 32)),
        "pn_5": iss.image_at((480, 288, 32, 32)),
        "pn_6": iss.image_at((480, 320, 32, 32)),
        "pn_7": iss.image_at((480, 352, 32, 32)),
        "pn_8": iss.image_at((480, 384, 32, 32))
    },
    "ring": {
        # 3 types ("n","1","3"), each with 5 rings using r{type}_{number}
        # e.g. rn_1 for type "n", ring 1
        "rn_1": iss.image_at((480, 416, 32, 32)),
        "rn_2": iss.image_at((480, 448, 32, 32)),
        "rn_3": iss.image_at((480, 480, 32, 32)),
        "rn_4": iss.image_at((512, 0, 32, 32)),
        "rn_5": iss.image_at((512, 32, 32, 32)),
        "r1_1": iss.image_at((512, 64, 32, 32)),
        "r1_2": iss.image_at((512, 96, 32, 32)),
        "r1_3": iss.image_at((512, 128, 32, 32)),
        "r1_4": iss.image_at((512, 160, 32, 32)),
        "r1_5": iss.image_at((512, 192, 32, 32)),
        "r3_1": iss.image_at((512, 224, 32, 32)),
        "r3_2": iss.image_at((512, 256, 32, 32)),
        "r3_3": iss.image_at((512, 288, 32, 32)),
        "r3_4": iss.image_at((512, 320, 32, 32)),
        "r3_5": iss.image_at((512, 352, 32, 32))
    },
    "scroll": {
        # 8 scrolls
        "s_1": iss.image_at((512, 384, 32, 32)),
        "s_2": iss.image_at((512, 416, 32, 32)),
        "s_3": iss.image_at((512, 448, 32, 32)),
        "s_4": iss.image_at((512, 480, 32, 32)),
        "s_5": iss.image_at((544, 0, 32, 32)),
        "s_6": iss.image_at((544, 32, 32, 32)),
        "s_7": iss.image_at((544, 64, 32, 32)),
        "s_8": iss.image_at((544, 96, 32, 32))
    },
    "roundgem": {
        # 10 gems
        "g_1": iss.image_at((544, 128, 32, 32)),
        "g_2": iss.image_at((544, 160, 32, 32)),
        "g_3": iss.image_at((544, 192, 32, 32)),
        "g_4": iss.image_at((544, 224, 32, 32)),
        "g_5": iss.image_at((544, 256, 32, 32)),
        "g_6": iss.image_at((544, 288, 32, 32)),
        "g_7": iss.image_at((544, 320, 32, 32)),
        "g_8": iss.image_at((544, 352, 32, 32)),
        "g_9": iss.image_at((544, 384, 32, 32)),
        "g_10": iss.image_at((544, 416, 32, 32))
    },
    "shield": {
        # 3 gens, each with 5 shields using s{gen}_{number}
        # e.g. s1_1 for gen 1, shield 1
        "s1_1": iss.image_at((544, 448, 32, 32)),
        "s1_2": iss.image_at((544, 480, 32, 32)),
        "s1_3": iss.image_at((576, 0, 32, 32)),
        "s1_4": iss.image_at((576, 32, 32, 32)),
        "s1_5": iss.image_at((576, 64, 32, 32)),
        "s2_1": iss.image_at((576, 96, 32, 32)),
        "s2_2": iss.image_at((576, 128, 32, 32)),
        "s2_3": iss.image_at((576, 160, 32, 32)),
        "s2_4": iss.image_at((576, 192, 32, 32)),
        "s2_5": iss.image_at((576, 224, 32, 32)),
        "s3_1": iss.image_at((576, 256, 32, 32)),
        "s3_2": iss.image_at((576, 288, 32, 32)),
        "s3_3": iss.image_at((576, 320, 32, 32)),
        "s3_4": iss.image_at((576, 352, 32, 32)),
        "s3_5": iss.image_at((576, 384, 32, 32))
    },
    "skull": {
        # 2 skulls using s_{number}
        # eg s_1 for skull 1
        "s_1": iss.image_at((576, 416, 32, 32)),
        "s_2": iss.image_at((576, 448, 32, 32))
    },
    "spellbook": {
        # 3 classes, each with 5 books, class order: "c","h","b"; using b{class}_{num}
        # e.g. bc_1 for class c, book 1
        "bc_1": iss.image_at((576, 480, 32, 32)),
        "bc_2": iss.image_at((608, 0, 32, 32)),
        "bc_3": iss.image_at((608, 32, 32, 32)),
        "bc_4": iss.image_at((608, 64, 32, 32)),
        "bc_5": iss.image_at((608, 96, 32, 32)),
        "bh_1": iss.image_at((608, 128, 32, 32)),
        "bh_2": iss.image_at((608, 160, 32, 32)),
        "bh_3": iss.image_at((608, 192, 32, 32)),
        "bh_4": iss.image_at((608, 224, 32, 32)),
        "bh_5": iss.image_at((608, 256, 32, 32)),
        "bb_1": iss.image_at((608, 288, 32, 32)),
        "bb_2": iss.image_at((608, 320, 32, 32)),
        "bb_3": iss.image_at((608, 352, 32, 32)),
        "bb_4": iss.image_at((608, 384, 32, 32)),
        "bb_5": iss.image_at((608, 416, 32, 32))
    },
    "staff": {
        # 3 gens, each with 5, using s{gen}_{num}
        # eg s1_1 for gen 1, staff 1
        "s1_1": iss.image_at((608, 448, 32, 32)),
        "s1_2": iss.image_at((608, 480, 32, 32)),
        "s1_3": iss.image_at((640, 0, 32, 32)),
        "s1_4": iss.image_at((640, 32, 32, 32)),
        "s1_5": iss.image_at((640, 64, 32, 32)),
        "s2_1": iss.image_at((640, 96, 32, 32)),
        "s2_2": iss.image_at((640, 128, 32, 32)),
        "s2_3": iss.image_at((640, 160, 32, 32)),
        "s2_4": iss.image_at((640, 192, 32, 32)),
        "s2_5": iss.image_at((640, 224, 32, 32)),
        "s3_1": iss.image_at((640, 256, 32, 32)),
        "s3_2": iss.image_at((640, 288, 32, 32)),
        "s3_3": iss.image_at((640, 320, 32, 32)),
        "s3_4": iss.image_at((640, 352, 32, 32)),
        "s3_5": iss.image_at((640, 384, 32, 32))
    },
    "metal_ingot": iss.image_at((640, 416, 32, 32)),
    "sword": {
        # 3 gens, each with 5, using s{gen}_{num}
        # eg s1_1 for gen 1, sword 1
        "s1_1": iss.image_at((640, 448, 32, 32)),
        "s1_2": iss.image_at((640, 480, 32, 32)),
        "s1_3": iss.image_at((672, 0, 32, 32)),
        "s1_4": iss.image_at((672, 32, 32, 32)),
        "s1_5": iss.image_at((672, 64, 32, 32)),
        "s2_1": iss.image_at((672, 96, 32, 32)),
        "s2_2": iss.image_at((672, 128, 32, 32)),
        "s2_3": iss.image_at((672, 160, 32, 32)),
        "s2_4": iss.image_at((672, 192, 32, 32)),
        "s2_5": iss.image_at((672, 224, 32, 32)),
        "s3_1": iss.image_at((672, 256, 32, 32)),
        "s3_2": iss.image_at((672, 288, 32, 32)),
        "s3_3": iss.image_at((672, 320, 32, 32)),
        "s3_4": iss.image_at((672, 352, 32, 32)),
        "s3_5": iss.image_at((672, 384, 32, 32))
    },
    "log": iss.image_at((672, 416, 32, 32))
}


class Coin(GameObj):
    def __init__(self, x, y, amount):
        self.amount = amount
        sprite = items['coin']['c{}_4'.format(amount)]
        super().__init__(x, y, sprite)


class Shoe(GameObj):
    def __init__(self, x, y):
        self.id = randrange(1, 6)
        self.inc = (self.id / 100) + 1
        super().__init__(x, y, items['shoe']['s_{}'.format(self.id)])


class Gem(GameObj):
    def __init__(self, x, y):
        self.type = choice(['diamond', 'gemstone', 'roundgem'])
        self.id = randrange(1, 11)
        if self.type == 'diamond':
            self.selector = 'd_{}'.format(self.id)
        else:
            self.selector = 'g_{}'.format(self.id)
        super().__init__(x, y, items[self.type][self.selector])


class Player(object):
    def __init__(self, x=0, y=0, facing='front', sprite='walk', index=0):
        self.x = x
        self.y = y
        self.facing = facing
        self.sprite_name = sprite
        self.sprite = sprites[sprite][facing][index]
        self.index = index
        self.max_health = 1000
        self.current_health = 500
        self.healthbar_length = 100
        self.healthbar_ratio = self.healthbar_length / self.max_health
        self.defence = 0
        self.attack = 1

    def change_facing(self, facing):
        match facing:
            case 'left':
                self.facing = 'left'
            case 'right':
                self.facing = 'right'
            case 'front':
                self.facing = 'front'
            case 'back':
                self.facing = 'back'
            case _:
                print('Invalid facing')

    def load_sprite(self, sprite):
        if sprite == self.sprite_name:
            return
        self.index = 0
        index = self.index
        match sprite:
            case 'spell':
                self.sprite_name = 'spell'
                self.sprite = sprites['spell'][self.facing][index]
            case 'thrust':
                self.sprite_name = 'thrust'
                self.sprite = sprites['thrust'][self.facing][index]
            case 'walk':
                self.sprite_name = 'walk'
                self.sprite = sprites['walk'][self.facing][index]
            case 'slash':
                self.sprite_name = 'slash'
                self.sprite = sprites['slash'][self.facing][index]
            case 'smash':
                self.sprite_name = 'smash'
                self.sprite = sprites['smash'][self.facing][index]
            case 'shoot':
                self.sprite_name = 'shoot'
                self.sprite = sprites['shoot'][self.facing][index]
            case 'hurt':
                self.sprite_name = 'hurt'
                self.sprite = sprites['hurt']['main'][index]
            case _:
                print('Invalid sprite')

    def pos(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def animate(self):
        self.index += 1
        if self.index == len(sprites[self.sprite_name][self.facing]):
            self.index = 0
        self.sprite = sprites[self.sprite_name][self.facing][self.index]

    def setMaxHealth(self, health):
        self.max_health = health

    def addMaxHealth(self, health):
        self.max_health += health

    def reduceMaxHealth(self, health):
        self.max_health -= health

    def setHealth(self, health):
        self.current_health = health

    def addHealth(self, health):
        self.current_health += health

    def reduceHealth(self, health):
        self.current_health -= health

    def setDefence(self, defence):
        self.defence = defence

    def addDefence(self, defence):
        self.defence += defence

    def reduceDefence(self, defence):
        self.defence -= defence

    def setAttack(self, attack):
        self.attack = attack

    def addAttack(self, attack):
        self.attack += attack

    def reduceAttack(self, attack):
        self.attack -= attack

    def calc_damage(self, damage):
        defenceAmount = round(self.defence * damage)
        currentDamage = damage - defenceAmount
        return currentDamage


class Enemy(GameObj):
    def __init__(self, x, y):
        super().__init__(x, y, items['skull']['s_1'])
        self.health = 10
        self.attackDmg = 1
        self.attackCooldown = False
        self.attackCooldownTimer = 0

    def receiveDamage(self, damage):
        self.health -= damage


def pause():
    display.fill((0, 0, 0))
    message = "Press enter to respawn or h to return..."
    messageFont = pygame.font.SysFont('Sans Serif', 50)
    messageSurf = messageFont.render(message, True, (255, 255, 255))
    messageRect = messageSurf.get_rect()
    messageRect.center = (width / 2, height / 2)
    display.blit(messageSurf, messageRect)
    pygame.display.update()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[enter]:
            return False
        if keys[pygame.K_h]:
            return True


def GameMain():
    pAtkCooldown = False
    pAtkCooldownTimer = 0
    frames = 0
    floor = Spritesheet(
        '../Python Game/img/background/floor.jpg').image_at((0, 0, 1024, 1024))
    floor = pygame.transform.scale(floor, (width, height))

    player = Player(gameData['sprite_center_x'],
                    gameData['sprite_center_y'], 'front', 'walk', 0)

    display.fill(colors['black'])
    display.blit(floor, (0, 0))
    display.blit(player.sprite, (player.x, player.y))

    running = True
    coins = []
    for x in range(5000):
        amount = randrange(1, 6)
        coin = Coin(randrange(64, width - 64), randrange(64, height - 64), amount)
        coins.append(coin)
    shoes = []
    for x in range(25):
        shoe = Shoe(randrange(64, width - 64), randrange(64, height - 64))
        shoes.append(shoe)
    gems = []
    for x in range(25):
        gem = Gem(randrange(64, width - 64), randrange(64, height - 64))
        gems.append(gem)
    enemies = []
#    for x in range(3):
#        enemy = Enemy(randrange(64, width - 64), randrange(64, height - 64))
#        enemies.append(enemy)
    walking = False
    indexMem = [0, 0]
    while running:
        frames += 1
        display.fill(colors['black'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == esc:
                    pygame.quit()
                    sys.exit()
                if event.key == lshift or event.key == rshift:
                    start = pause()
                    if start:
                        continue
                    else:
                        player.pos(
                            (gameData['sprite_center_x'], gameData['sprite_center_y']))
                        player.change_facing('front')
                        player.load_sprite('walk')
                        player.index = indexMem[0]
        keys = pygame.key.get_pressed()
        val = calc_vect(keys, (gameData['com_reduce'], gameData['vel']))
        player.pos((player.x + val[0], player.y + val[1]))
        if val[2] != '':
            player.change_facing(val[2])
        if val[3]:
            if player.sprite_name == 'slash':
                indexMem[1] = player.index
                player.load_sprite('walk')
                player.index = indexMem[0]
                player.animate()
            walking = True
        elif walking and not val[3]:
            walking = False
        else:
            pass

        if player.x < 0:
            player.x = 0
        if player.x > width - 64:
            player.x = width - 64
        if player.y < 0:
            player.y = 0
        if player.y > height - 64:
            player.y = height - 64
        for coin in coins:
            if coin.x - 48 < player.x < coin.x + 16 and coin.y - 48 < player.y < coin.y + 16:
                index = coins.index(coin)
                amount = randrange(1, 6)
                newcoin = Coin(randrange(64, width - 64), randrange(64, height - 64), amount)
                coins.pop(index)
                gameData['coins'] += coin.amount
                coins.insert(index, newcoin)
        for shoe in shoes:
            if shoe.x + 16 > player.x > shoe.x-48 and shoe.y - 48 < player.y < shoe.y:
                index = shoes.index(shoe)
                newshoe = Shoe(randrange(64, width - 64), randrange(64, height - 64))
                shoes.pop(index)
                gameData['vel'] *= shoe.inc
                gameData['vel'] = float(round(gameData['vel'], 2))
                shoes.insert(index, newshoe)
        for gem in gems:
            if gem.x + 16 > player.x > gem.x - 48 and gem.y - 48 < player.y < gem.y + 16:
                index = gems.index(gem)
                newgem = Gem(randrange(64, width - 64), randrange(64, height - 64))
                gems.pop(index)
                gameData['points'] += 1
                gems.insert(index, newgem)
        for enemy in enemies:
            if enemy.x - 48 < player.x < enemy.x + 16 and enemy.y - 48 < player.y < enemy.y + 16:
                if player.sprite_name == 'walk':
                    indexMem[0] = player.index
                    player.load_sprite('slash')
                    player.index = indexMem[1]
                    player.animate()
                else:
                    pass
                if not enemy.attackCooldown:
                    player.current_health -= player.calc_damage(enemy.attackDmg)
                    enemy.attackCooldown = True
                    enemy.attackCooldownTimer = 0
                else:
                    enemy.attackCooldownTimer += 1
                    if enemy.attackCooldownTimer == 30:
                        enemy.attackCooldown = False
                        enemy.attackCooldownTimer = 0
                if not pAtkCooldown:
                    enemy.receiveDamage(player.attack)
                    pAtkCooldown = True
                    pAtkCooldownTimer = 0
                else:
                    pAtkCooldownTimer += 1
                    if pAtkCooldownTimer == 30:
                        pAtkCooldown = False
                        pAtkCooldownTimer = 0
                if enemy.health <= 0:
                    index = enemies.index(enemy)
                    newenemy = Enemy(randrange(64, width - 64), randrange(64, height - 64))
                    enemies.pop(index)
                    gameData['points'] += 1
                    enemies.insert(index, newenemy)
                    pAtkCooldown = False
                    pAtkCooldownTimer = 0
                walking = False
            elif player.sprite_name == 'slash':
                indexMem[1] = player.index
                player.load_sprite('walk')
                player.index = indexMem[0]
                player.animate()
        if player.sprite_name == 'slash' and frames % 30 == 0:
            player.animate()
            indexMem[1] = player.index
        elif player.sprite_name == 'walk' and walking and frames % 4 == 0:
            player.animate()
            indexMem[0] = player.index

        display.blit(floor, (0, 0))
        for x in coins:
            display.blit(x.sprite, (x.x, x.y))
        for x in shoes:
            display.blit(x.sprite, (x.x, x.y))
        for x in gems:
            display.blit(x.sprite, (x.x, x.y))
        for x in enemies:
            display.blit(x.sprite, (x.x, x.y))
        display.blit(player.sprite, (player.x, player.y))

        coinmsg = "Coins: {cc} coins".format(cc=gameData['coins'])
        velmsg = "Velocity: {vol}".format(vol=gameData['vel'])
        pointmsg = "Points: {points}".format(points=gameData['points'])
        messageFont = pygame.font.SysFont('Sans Serif', 32)
        coinSurf = messageFont.render(coinmsg, True, (255, 255, 255), (0, 0, 0, 0.3))
        coinRect = coinSurf.get_rect()
        velSurf = messageFont.render(velmsg, True, (255, 255, 255), (0, 0, 0, 0.3))
        velRect = velSurf.get_rect()
        pointSurf = messageFont.render(pointmsg, True, (255, 255, 255), (0, 0, 0, 0.3))
        pointRect = pointSurf.get_rect()
        coinRect.center = (100, 50)
        velRect.center = (100, 100)
        pointRect.center = (100, 150)
        display.blit(coinSurf, coinRect)
        display.blit(velSurf, velRect)
        display.blit(pointSurf, pointRect)
        pygame.draw.rect(display, (0, 0, 0), (width - player.healthbar_length, 0, player.healthbar_length, 20))
        pygame.draw.rect(display, (255, 0, 0),
                         (width - player.healthbar_length, 0, player.current_health * player.healthbar_ratio, 20))
        pygame.display.update()
        clock.tick(60)


def main():
    titleText = 'Welcome to the game'
    titleFont = pygame.font.SysFont('Sans Serif', 75)
    message = 'Press any key to start or ESC to exit'
    messageFont = pygame.font.SysFont('Sans Serif', 45)
    messageSurf = messageFont.render(message, True, colors['white'])
    messageRect = messageSurf.get_rect()
    messageRect.center = (width / 2, height / 2 + 75)
    section = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == esc:
                    pygame.quit()
                    sys.exit()
                else:
                    run = False
                    GameMain()
        rainbowColor = rainbow(section)
        section = rainbowColor[1]
        titleSurf = titleFont.render(titleText, True, rainbowColor[0])
        titleRect = titleSurf.get_rect()
        titleRect.center = (width / 2, height / 2 - 75)
        display.blit(titleSurf, titleRect)
        display.blit(messageSurf, messageRect)
        pygame.display.update()
        clock.tick(20)


main()
