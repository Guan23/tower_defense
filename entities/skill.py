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

class Skill(ABC):
    def __init__(self):
        self.damage = 0
        self.range = 0
        self.cooldown = 0
        self.last_use = 0

    def can_use(self):
        return pygame.time.get_ticks() - self.last_use > self.cooldown

    def upgrade(self):
        self.damage = int(self.damage * SKILL_UPGRADE_DMG)
        self.range += SKILL_UPGRADE_RANGE
        self.cooldown = int(self.cooldown * SKILL_UPGRADE_CD)

    @abstractmethod
    def release(self, monsters, damage_texts):
        pass

    def draw(self, screen, x, y):
        pygame.draw.circle(screen, (*COLOR_WHITE, 30), (x, y), self.range, 1)

# 火焰
class FireSkill(Skill):
    def __init__(self):
        super().__init__()
        self.damage = SKILL_FIRE_BASE_DMG
        self.range = SKILL_FIRE_BASE_RANGE
        self.cooldown = SKILL_FIRE_BASE_CD

    def release(self, monsters, damage_texts):
        if not self.can_use(): return
        self.last_use = pygame.time.get_ticks()
        cx, cy = SCREEN_W//2, SCREEN_H//2
        for m in monsters:
            if ((m.x-cx)**2 + (m.y-cy)**2)**0.5 < self.range:
                m.hp -= self.damage
                damage_texts.append(pygame.sprite.Sprite()) # 占位，保持兼容

# 雷电
class ThunderSkill(Skill):
    def __init__(self):
        super().__init__()
        self.damage = SKILL_THUNDER_BASE_DMG
        self.range = SKILL_THUNDER_BASE_RANGE
        self.cooldown = SKILL_THUNDER_BASE_CD

    def release(self, monsters, damage_texts):
        if not self.can_use(): return
        self.last_use = pygame.time.get_ticks()
        for m in monsters:
            m.hp -= self.damage
            damage_texts.append(pygame.sprite.Sprite())

# 冰
class IceSkill(Skill):
    def __init__(self):
        super().__init__()
        self.damage = SKILL_ICE_BASE_DMG
        self.range = SKILL_ICE_BASE_RANGE
        self.cooldown = SKILL_ICE_BASE_CD

    def release(self, monsters, damage_texts):
        if not self.can_use(): return
        self.last_use = pygame.time.get_ticks()



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
