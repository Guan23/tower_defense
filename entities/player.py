# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : player.py

"""
info:

"""

# system

# third_party

# custom
from abc import ABC, abstractmethod
import pygame
from settings import *
from tools import load_image

class Player(ABC):
    def __init__(self):
        # 固定在7等分中间格子中心
        self.x = CELL_START_X + MIDDLE_CELL_INDEX * int(CELL_RAW_W) + CELL_FINAL_W // 2
        self.y = SCREEN_H - 80  # 底部位置
        self.size = PLAYER_SIZE
        self.color = COLOR_BLUE
        self.gold = PLAYER_INIT_GOLD
        self.img = load_image("assets/player", (self.size, self.size))

    @abstractmethod
    def get_info(self):
        pass

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x - self.size//2, self.y - self.size//2))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size//2)

class NormalPlayer(Player):
    def __init__(self):
        super().__init__()
        self.hp = PLAYER_INIT_HP
        self.max_hp = PLAYER_INIT_HP

    def get_info(self):
        return "普通主角"



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
