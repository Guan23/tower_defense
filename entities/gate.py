# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : gate.py

"""
info:

"""

# system

# third_party

# custom

import pygame
from settings import *


class HomeGate:
    def __init__(self):
        self.w = GATE_W
        self.h = 30
        self.x = (SCREEN_W - self.w) // 2
        self.y = GATE_Y
        self.hp = 500
        self.max_hp = 500
        self.color = COLOR_GRAY

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
        # 血条
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, COLOR_RED, (self.x, self.y - 10, self.w, 6))
        pygame.draw.rect(screen, COLOR_GREEN, (self.x, self.y - 10, self.w * ratio, 6))


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
