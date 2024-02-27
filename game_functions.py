import sys
import pygame
import math
import time

def distance_to_object(character, obj):
    char_x, char_y = character.rect.center
    dx = max(obj.rect.x, min(char_x, obj.rect.x + obj.rect.width)) - char_x
    dy = max(obj.rect.y, min(char_y, obj.rect.y + obj.rect.height)) - char_y
    return math.sqrt(dx ** 2 + dy ** 2)