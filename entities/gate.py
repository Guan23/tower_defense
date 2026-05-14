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
from abc import ABC, abstractmethod
import pygame
from settings import *
from utils import load_image

class Gate(ABC):
    def __init__(self):
        self.hp = 0
        self.max_hp = 0
        self.x = W // 2
        self.y = H - 180
        self.w = int(W * 0.8)   # 宽度 = 屏幕80%
        self.h = 60
        self.color = YELLOW
        self.img = load_image("assets/gate", (self.w, self.h))

    @abstractmethod
    def get_info(self):
        pass

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x - self.w//2, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x - self.w//2, self.y, self.w, self.h))
        # 血条
        bar_w = self.w
        bar_h = 6
        pygame.draw.rect(screen, RED, (self.x - self.w//2, self.y-10, bar_w, bar_h))
        pygame.draw.rect(screen, GREEN, (self.x - self.w//2, self.y-10, bar_w*(self.hp/self.max_hp), bar_h))

class HomeGate(Gate):
    def __init__(self):
        super().__init__()
        self.hp = self.max_hp = 500

    def get_info(self):
        return "基地大门"





if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
