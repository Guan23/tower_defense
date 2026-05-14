# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : monster.py

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


class Monster(ABC):
    def __init__(self):
        self.hp = 0
        self.max_hp = 0
        self.speed = 0
        self.damage = 0
        self.size = 30
        self.x = pygame.time.get_ticks() % (W - self.size)
        self.y = -self.size
        self.color = RED
        self.img = None

    @abstractmethod
    def get_info(self):
        pass

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        # 血条
        pygame.draw.rect(screen, RED, (self.x, self.y - 6, self.size, 4))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 6, self.size * (self.hp / self.max_hp), 4))


class NormalMonster(Monster):
    def __init__(self):
        super().__init__()
        self.hp = self.max_hp = 50
        self.speed = 1.2
        self.damage = 5
        self.img = load_image("assets/monster", (self.size, self.size))

    def get_info(self):
        return "普通僵尸"


class EliteMonster(Monster):
    def __init__(self):
        super().__init__()
        self.hp = self.max_hp = 150
        self.speed = 0.8
        self.damage = 15
        self.size = 40
        self.color = PURPLE
        self.img = load_image("assets/elite", (self.size, self.size))

    def get_info(self):
        return "精英僵尸"


class BossMonster(Monster):
    def __init__(self):
        super().__init__()
        self.hp = self.max_hp = 600
        self.speed = 0.4
        self.damage = 40
        self.size = 60
        self.color = BLACK
        self.img = load_image("assets/boss", (self.size, self.size))

    def get_info(self):
        return "BOSS僵尸"


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
