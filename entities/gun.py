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
from tools import load_image
from utils.sound_manager import shoot_snd


class Gun(ABC):
    def __init__(self):
        self.damage = 0
        self.fire_rate = 0
        self.bullet_speed = 0
        self.last_shot = 0
        self.bullets = []
        self.img = load_image("assets/gun", (30, 30))
        self.dmg_type = "physical"

    # 和炮塔完全一致的寻敌规则
    def find_target(self, monsters, gate_y, px, py):
        if not monsters:
            return None
        gate_line = gate_y
        best = None
        best_dist_gate = float("inf")
        best_dist_self = float("inf")
        best_x = float("inf")

        for m in monsters:
            dist_gate = gate_line - (m.y + m.size)
            dist_self = ((m.x - px) ** 2 + (m.y - py) ** 2) ** 0.5

            if dist_gate < best_dist_gate:
                best = m
                best_dist_gate = dist_gate
                best_dist_self = dist_self
                best_x = m.x
            elif dist_gate == best_dist_gate:
                if dist_self < best_dist_self:
                    best = m
                    best_dist_self = dist_self
                    best_x = m.x
                elif dist_self == best_dist_self:
                    if m.x < best_x:
                        best = m
                        best_x = m.x
        return best

    @abstractmethod
    def shoot(self, px, py, monsters, gate_y):
        pass


class NormalGun(Gun):
    def __init__(self):
        super().__init__()
        self.damage = 8
        self.fire_rate = 300
        self.bullet_speed = 8

    def shoot(self, px, py, monsters, gate_y):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            target = self.find_target(monsters, gate_y, px, py)
            if target:
                self.last_shot = now
                dx = target.x - px
                dy = target.y - py
                dis = (dx ** 2 + dy ** 2) ** 0.5
                bullet_rect = pygame.Rect(px - 5, py - 20, 10, 10)
                self.bullets.append({
                    "rect": bullet_rect,
                    "dmg": self.damage,
                    "speed": self.bullet_speed,
                    "dir": (dx / dis, dy / dis),
                    "laser": False,
                    "dmg_type": self.dmg_type,
                    "from_tower": False
                })
                if shoot_snd:
                    shoot_snd.play()


class LaserGun(Gun):
    def __init__(self):
        super().__init__()
        self.damage = 20
        self.fire_rate = 600
        self.bullet_speed = 12

    def shoot(self, px, py, monsters, gate_y):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            target = self.find_target(monsters, gate_y, px, py)
            if target:
                self.last_shot = now
                dx = target.x - px
                dy = target.y - py
                dis = (dx ** 2 + dy ** 2) ** 0.5
                bullet_rect = pygame.Rect(px - 5, py - 20, 10, 10)
                self.bullets.append({
                    "rect": bullet_rect,
                    "dmg": self.damage,
                    "speed": self.bullet_speed,
                    "dir": (dx / dis, dy / dis),
                    "laser": True,
                    "dmg_type": self.dmg_type,
                    "from_tower": False
                })
                if shoot_snd:
                    shoot_snd.play()


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
