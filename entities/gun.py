# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : gun.py

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

class Gun(ABC):
    def __init__(self):
        self.damage = 0
        self.fire_rate = 0
        self.bullet_speed = 0
        self.last_shot = 0
        self.bullets = []
        self.img = load_image("assets/gun", (30, 30))

    @abstractmethod
    def shoot(self, px, py):
        pass

class NormalGun(Gun):
    def __init__(self):
        super().__init__()
        self.damage = 8
        self.fire_rate = 300
        self.bullet_speed = 8

    def shoot(self, px, py):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            bullet_rect = pygame.Rect(px-5, py-20, 10, 10)
            self.bullets.append({"rect": bullet_rect, "dmg": self.damage, "speed": self.bullet_speed, "laser": False})

class LaserGun(Gun):
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.fire_rate = 600
        self.bullet_speed = 12

    def shoot(self, px, py):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            self.last_shot = now
            bullet_rect = pygame.Rect(px-5, py-20, 10, 10)
            self.bullets.append({"rect": bullet_rect, "dmg": self.damage, "speed": self.bullet_speed, "laser": True})





if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
