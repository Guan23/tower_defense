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
from utils import load_image

class Player(ABC):
    def __init__(self):
        self.hp = 0
        self.max_hp = 0
        self.damage = 0
        self.x = W//2
        self.y = H - 80  # 玩家在门后面
        self.size = 40
        self.color = BLUE
        self.gold = 100
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
        self.hp = self.max_hp = 100
        self.damage = 10

    def get_info(self):
        return "普通主角"



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
