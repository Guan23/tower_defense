# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : skill.py

"""
info:

"""

# system

# third_party

# custom

from abc import ABC, abstractmethod
import pygame
from settings import *
from utils import get_font


class Skill(ABC):
    def __init__(self):
        self.cd = 0
        self.last_use = 0
        self.damage = 0
        self.range = 0

    @abstractmethod
    def release(self, monsters):
        pass

    # 绘制技能范围圈 + CD提示
    def draw(self, screen, center_x, center_y):
        now = pygame.time.get_ticks()
        remaining = max(0, self.cd - (now - self.last_use))
        ratio = remaining / self.cd

        # 范围圈
        pygame.draw.circle(screen, (*self.color[:3], 60), (center_x, center_y), self.range, 2)
        # CD文字
        font = get_font(20)
        text = font.render(f"{remaining//1000}s", True, WHITE)
        screen.blit(text, (center_x -15, center_y - self.range -20))

class FireSkill(Skill):
    def __init__(self):
        super().__init__()
        self.cd = 8000
        self.damage = 30
        self.range = 150
        self.color = (255,80,0,80)

    def release(self, monsters):
        now = pygame.time.get_ticks()
        if now - self.last_use > self.cd:
            self.last_use = now
            for m in monsters:
                if abs(m.x - W//2) < self.range and abs(m.y - H//2) < self.range:
                    m.hp -= self.damage

class ThunderSkill(Skill):
    def __init__(self):
        super().__init__()
        self.cd = 12000
        self.damage = 80
        self.range = 250
        self.color = (100,180,255,80)

    def release(self, monsters):
        now = pygame.time.get_ticks()
        if now - self.last_use > self.cd:
            self.last_use = now
            for m in monsters:
                if abs(m.x - W//2) < self.range and abs(m.y - H//2) < self.range:
                    m.hp -= self.damage



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
