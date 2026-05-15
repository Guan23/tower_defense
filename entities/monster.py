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
import random


class Monster(ABC):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 0
        self.max_hp = 0
        self.speed = MONSTER_BASE_SPEED
        self.speed_x = random.uniform(-0.0, 0.0)
        self.size = MONSTER_SIZE
        self.color = COLOR_RED
        self.img = load_image("assets/monster", (self.size, self.size))

        # ========== 四系抗性（0~1） ==========
        self.phys_resist = 0.0
        self.fire_resist = 0.0
        self.ice_resist = 0.0
        self.elec_resist = 0.0

    def move(self):
        self.y += self.speed
        self.x += self.speed_x

    def update(self):
        self.move()

    @abstractmethod
    def get_info(self):
        pass

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x - self.size // 2, self.y - self.size // 2))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)


class NormalMonster(Monster):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.hp = MONSTER_NORMAL_HP
        self.max_hp = MONSTER_NORMAL_HP
        self.phys_resist = MONSTER_NORMAL_PHYS_RES
        self.fire_resist = MONSTER_NORMAL_FIRE_RES
        self.ice_resist = MONSTER_NORMAL_ICE_RES
        self.elec_resist = MONSTER_NORMAL_ELEC_RES

    def get_info(self): return "普通怪物"


class EliteMonster(Monster):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.hp = MONSTER_ELITE_HP
        self.max_hp = MONSTER_ELITE_HP
        self.speed *= 0.8
        self.color = (200, 0, 200)
        self.phys_resist = MONSTER_ELITE_PHYS_RES
        self.fire_resist = MONSTER_ELITE_FIRE_RES
        self.ice_resist = MONSTER_ELITE_ICE_RES
        self.elec_resist = MONSTER_ELITE_ELEC_RES

    def get_info(self): return "精英怪物"


class BossMonster(Monster):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.hp = MONSTER_BOSS_HP
        self.max_hp = MONSTER_BOSS_HP
        self.speed *= 0.5
        self.size = 50
        self.color = (255, 100, 0)
        self.phys_resist = MONSTER_BOSS_PHYS_RES
        self.fire_resist = MONSTER_BOSS_FIRE_RES
        self.ice_resist = MONSTER_BOSS_ICE_RES
        self.elec_resist = MONSTER_BOSS_ELEC_RES

    def get_info(self): return "BOSS怪物"


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
