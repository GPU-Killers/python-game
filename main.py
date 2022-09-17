import pygame
import sys
import os
from random import *
from pygame import K_ESCAPE as esc
from pygame import K_LSHIFT as lshift
from pygame import K_RETURN as enter
from pygame import K_RSHIFT as rshift

from keymgr import *
from textmod import *

class GameObj:
    def __init__(self,x,y,sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        

pygame.init()
display = pygame.display.set_mode((0,0), pygame.RESIZABLE)
clock = pygame.time.Clock()

(width, height) = pygame.display.get_window_size()

gameData = {
    'width': width,
    'height': height,
    'sprite_size': 64,
    'sprite_center_x': width / 2 - 64 / 2,
    'sprite_center_y': height / 2 - 64 / 2,
    'com_reduct': 0,
    'vol': 2,
    'coins': 0
}

colors = {
    "white": (255, 255, 255),
    "blue": (0, 0, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "black": (0, 0, 0)
}

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print('Unable to load spritesheet image:' + filename)
            raise SystemExit(message)
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey=-1):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(
            (rectangle[1], rectangle[0], rectangle[2], rectangle[3]))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[1]+rect[2]*x, rect[0], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

ss = spritesheet('./media/images/entity/sprites.png')

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

iss = spritesheet('./media/images/items/items.png')

items = {
    'chessplate': {
        'cp_1': iss.image_at((0,0,32,32)),
        'cp_2': iss.image_at((0,32,32,32)),
        'cp_3': iss.image_at((0,64,32,32)),
        'cp_4': iss.image_at((0,96,32,32)),
        'cp_5': iss.image_at((0,128,32,32))
    },
    'arrow': {
        'ag1_1': iss.image_at((0,160,32,32)),
        'ag1_2': iss.image_at((0,192,32,32)),
        'ag1_3': iss.image_at((0,224,32,32)),
        'ag1_4': iss.image_at((0,256,32,32)),
        'ag1_5': iss.image_at((0,288,32,32)),
        'ag2_1': iss.image_at((0,320,32,32)),
        'ag2_2': iss.image_at((0,352,32,32)),
        'ag2_3': iss.image_at((0,384,32,32)),
        'ag2_4': iss.image_at((0,416,32,32)),
        'ag2_5': iss.image_at((0,448,32,32)),
        'ag3_1': iss.image_at((0,480,32,32)),
        'ag3_2': iss.image_at((32,0,32,32)),
        'ag3_3': iss.image_at((32,32,32,32)),
        'ag3_4': iss.image_at((32,64,32,32)),
        'ag3_5': iss.image_at((32,96,32,32))
    },
    'bone': iss.image_at((32,128,32,32)),
    'book': {
        'brown_1': iss.image_at((32,160,32,32)),
        'brown_2': iss.image_at((32,192,32,32)),
        'brown_3': iss.image_at((32,224,32,32)),
        'brown_4': iss.image_at((32,256,32,32)),
        'brown_5': iss.image_at((32,288,32,32)),
        'brown_6': iss.image_at((32,320,32,32)),
        'brown_7': iss.image_at((32,352,32,32)),
        'green_1': iss.image_at((32,384,32,32)),
        'green_2': iss.image_at((32,416,32,32)),
        'green_3': iss.image_at((32,448,32,32)),
        'green_4': iss.image_at((32,480,32,32)),
        'green_5': iss.image_at((64,0,32,32)),
        'green_6': iss.image_at((64,32,32,32)),
        'green_7': iss.image_at((64,64,32,32)),
        'red_1': iss.image_at((64,96,32,32)),
        'red_2': iss.image_at((64,128,32,32)),
        'red_3': iss.image_at((64,160,32,32)),
        'red_4': iss.image_at((64,192,32,32)),
        'red_5': iss.image_at((64,224,32,32)),
        'red_6': iss.image_at((64,256,32,32)),
        'red_7': iss.image_at((64,288,32,32)),
        'blue_1': iss.image_at((64,320,32,32)),
        'blue_2': iss.image_at((64,352,32,32)),
        'blue_3': iss.image_at((64,384,32,32)),
        'blue_4': iss.image_at((64,416,32,32)),
        'blue_5': iss.image_at((64,448,32,32)),
        'blue_6': iss.image_at((64,480,32,32)),
        'blue_7': iss.image_at((96,0,32,32)),
        'grey_1': iss.image_at((96,32,32,32)),
        'grey_2': iss.image_at((96,64,32,32)),
        'grey_3': iss.image_at((96,96,32,32)),
        'grey_4': iss.image_at((96,128,32,32)),
        'grey_5': iss.image_at((96,160,32,32)),
        'grey_6': iss.image_at((96,192,32,32)),
        'grey_7': iss.image_at((96,224,32,32)),
        'black_1': iss.image_at((96,256,32,32)),
        'black_2': iss.image_at((96,288,32,32)),
        'black_3': iss.image_at((96,320,32,32)),
        'black_4': iss.image_at((96,352,32,32)),
        'black_5': iss.image_at((96,384,32,32)),
        'black_6': iss.image_at((96,416,32,32)),
        'black_7': iss.image_at((96,448,32,32))
    },
    'shoe': {
        's_1': iss.image_at((96,480,32,32)),
        's_2': iss.image_at((128,0,32,32)),
        's_3': iss.image_at((128,32,32,32)),
        's_4': iss.image_at((128,64,32,32)),
        's_5': iss.image_at((128,96,32,32))
    },
    'bow': {
        'b1_1': iss.image_at((128,128,32,32)),
        'b1_2': iss.image_at((128,160,32,32)),
        'b1_3': iss.image_at((128,192,32,32)),
        'b1_4': iss.image_at((128,224,32,32)),
        'b1_5': iss.image_at((128,256,32,32)),
        'b2_1': iss.image_at((128,288,32,32)),
        'b2_2': iss.image_at((128,320,32,32)),
        'b2_3': iss.image_at((128,352,32,32)),
        'b2_4': iss.image_at((128,384,32,32)),
        'b2_5': iss.image_at((128,416,32,32)),
        'b3_1': iss.image_at((128,448,32,32)),
        'b3_2': iss.image_at((128,480,32,32)),
        'b3_3': iss.image_at((160,0,32,32)),
        'b3_4': iss.image_at((160,32,32,32)),
        'b3_5': iss.image_at((160,64,32,32))
    },
    "candle": {
        "out": iss.image_at((160,96,32,32)),
        "lit": iss.image_at((160,128,32,32))
    },
    "candy": {
        "cane_1": iss.image_at((160,160,32,32)),
        "cane_2": iss.image_at((160,192,32,32)),
        "cane_3": iss.image_at((160,224,32,32)),
        "cane_4": iss.image_at((160,256,32,32)),
        "cane_5": iss.image_at((160,288,32,32)),
        "cane_6": iss.image_at((160,320,32,32)),
        "cane_7": iss.image_at((160,352,32,32)),
        "hard_1": iss.image_at((160,384,32,32)),
        "hard_2": iss.image_at((160,416,32,32)),
        "hard_3": iss.image_at((160,448,32,32)),
        "hard_4": iss.image_at((160,480,32,32)),
        "hard_5": iss.image_at((192,0,32,32)),
        "hard_6": iss.image_at((192,32,32,32)),
        "hard_7": iss.image_at((192,64,32,32))
    },
    "coin": {
        "c1_1": iss.image_at((192,96,32,32)),
        "c1_2": iss.image_at((192,128,32,32)),
        "c1_3": iss.image_at((192,160,32,32)),
        "c1_4": iss.image_at((192,192,32,32)),
        "c1_5": iss.image_at((192,224,32,32)),
        "c2_1": iss.image_at((192,256,32,32)),
        "c2_2": iss.image_at((192,288,32,32)),
        "c2_3": iss.image_at((192,320,32,32)),
        "c2_4": iss.image_at((192,352,32,32)),
        "c2_5": iss.image_at((192,384,32,32)),
        "c3_1": iss.image_at((192,416,32,32)),
        "c3_2": iss.image_at((192,448,32,32)),
        "c3_3": iss.image_at((192,480,32,32)),
        "c3_4": iss.image_at((224,0,32,32)),
        "c3_5": iss.image_at((224,32,32,32)),
        "c4_1": iss.image_at((224,64,32,32)),
        "c4_2": iss.image_at((224,96,32,32)),
        "c4_3": iss.image_at((224,128,32,32)),
        "c4_4": iss.image_at((224,160,32,32)),
        "c4_5": iss.image_at((224,192,32,32)),
        "c5_1": iss.image_at((224,224,32,32)),
        "c5_2": iss.image_at((224,256,32,32)),
        "c5_3": iss.image_at((224,288,32,32)),
        "c5_4": iss.image_at((224,320,32,32)),
        "c5_5": iss.image_at((224,352,32,32))
    },
    "cookie": iss.image_at((224,384,32,32)),
    "cotton": iss.image_at((224,416,32,32)),
    "diamond": {
        "d_1": iss.image_at((224,448,32,32)),
        "d_2": iss.image_at((224,480,32,32)),
        "d_3": iss.image_at((256,0,32,32)),
        "d_4": iss.image_at((256,32,32,32)),
        "d_5": iss.image_at((256,64,32,32)),
        "d_6": iss.image_at((256,96,32,32)),
        "d_7": iss.image_at((256,128,32,32)),
        "d_8": iss.image_at((256,160,32,32)),
        "d_9": iss.image_at((256,192,32,32)),
        "d_10": iss.image_at((256,224,32,32))
    },
    "soda": {
        "empty": iss.image_at((256,256,32,32)),
        "full": iss.image_at((256,288,32,32))
    },
    "wine": {
        "empty": iss.image_at((256,320,32,32)),
        "full": iss.image_at((256,352,32,32))
    },
    "fish": {
        "f_1": iss.image_at((256,384,32,32)),
        "f_2": iss.image_at((256,416,32,32)),
        "f_3": iss.image_at((256,448,32,32)),
        "f_4": iss.image_at((256,480,32,32)),
        "f_5": iss.image_at((288,0,32,32))
    },
    "flower": {
        "red": iss.image_at((288,32,32,32)),
        "yellow": iss.image_at((288,64,32,32))
    },
    "apple": iss.image_at((288,96,32,32)),
    "banana": iss.image_at((288,128,32,32)),
}

class Coin(GameObj):
    def __init__(self, x, y, ammount):
        self.ammount = ammount
        sprite = items['coin'][('c{}_4').format(ammount)]
        super().__init__(x, y, sprite)

class Player(object):
    def __init__(self, x=0, y=0, facing='front', sprite='walk', index=0):
        self.x = x
        self.y = y
        self.facing = facing
        self.sprite_name = sprite
        self.sprite = sprites[sprite][facing][index]
        self.index = index

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
        self.index = self.index + 1
        if self.index == len(sprites[self.sprite_name][self.facing]):
            self.index = 0
        self.sprite = sprites[self.sprite_name][self.facing][self.index]

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
            paused = False
            return False
        if keys[pygame.K_h]:
            paused = False
            return True

def GameMain():
    floor = spritesheet(
        '../Python Game/img/background/floor.jpg').image_at((0, 0, 1024, 1024))
    floor = pygame.transform.scale(floor, (width, height))

    player = Player(gameData['sprite_center_x'],
                    gameData['sprite_center_y'], 'front', 'walk', 0)

    display.fill(colors['black'])
    display.blit(floor, (0, 0))
    display.blit(player.sprite, (player.x, player.y))

    running = True
    coins = []
    for x in range(100):
        ammount = randrange(1,6)
        coin = Coin(randrange(64,width-64),randrange(64,height-64),ammount)
        coins.append(coin)
    while running:
        display.fill(colors['black'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == esc:
                    pygame.quit()
                    sys.exit()
                if event.key == lshift:
                    start = pause()
                    if start:
                        continue
                    else:
                        player.pos(
                            (gameData['sprite_center_x'], gameData['sprite_center_y']))
                        player.change_facing('front')
                        player.load_sprite('walk')
                if event.key == rshift:
                    start = pause()
                    if start:
                        continue
                    else:
                        player.pos(
                            (gameData['sprite_center_x'], gameData['sprite_center_y']))
                        player.change_facing('front')
                        player.load_sprite('walk')
        keys = pygame.key.get_pressed()
        val = calc_vect(keys, (gameData['com_reduct'], gameData['vol']))
        player.pos((player.x + val[0], player.y + val[1]))
        if val[2] == '':
            pass
        else:
            player.change_facing(val[2])
        if val[3] == False:
            pass
        else:
            player.animate()

        if player.x < 0:
            player.x = 0
        if player.x > width-64:
            player.x = width-64
        if player.y < 0:
            player.y = 0
        if player.y > height-64:
            player.y = height-64
        for coin in coins:
            if (player.x > coin.x - 48 and player.x < coin.x + 16 and player.y > coin.y - 48 and player.y < coin.y + 16):
                index = coins.index(coin)
                ammount = randrange(1,6)
                newcoin = Coin(randrange(64,width-64),randrange(64,height-64),ammount)
                coins.pop(index)
                gameData['coins'] += coin.ammount
                coins.insert(index,newcoin)

        display.blit(floor, (0, 0))
        display.blit(player.sprite, (player.x, player.y))
        for x in coins:
            display.blit(x.sprite,(x.x,x.y))
        message = "Coins: {} coins".format(gameData['coins'])
        messageFont = pygame.font.SysFont('Sans Serif', 32)
        messageSurf = messageFont.render(message, True, (255, 255, 255),(0,0,0,0.3))
        messageRect = messageSurf.get_rect()
        messageRect.center = (100, 50)
        display.blit(messageSurf, messageRect)
        pygame.display.update()
        clock.tick(60)


def main():
    titleText = 'Welcome to the game'
    titleFont = pygame.font.SysFont('Sans Serif', 75)
    message = 'Press any key to start or ESC to exit'
    messageFont = pygame.font.SysFont('Sans Serif', 45)
    messageSurf = messageFont.render(message, True, colors['white'])
    messageRect = messageSurf.get_rect()
    messageRect.center = (width/2, height/2+75)
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
        rcolor = rainbow(section)
        section = rcolor[1]
        titleSurf = titleFont.render(titleText, True, rcolor[0])
        titleRect = titleSurf.get_rect()
        titleRect.center = (width/2, height/2-75)
        display.blit(titleSurf, titleRect)
        display.blit(messageSurf, messageRect)
        pygame.display.update()
        clock.tick(30)


main()