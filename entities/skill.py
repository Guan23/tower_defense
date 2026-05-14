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
from tools import get_font
from entities.damage_text import DamageText
from utils.sound_manager import fire_hit_snd, thunder_hit_snd, ice_hit_snd


class Skill(ABC):
    def __init__(self):
        self.cd = 0
        self.last_use = 0
        self.damage = 0
        self.range = 0
        self.dmg_type = "physical"

    @abstractmethod
    def release(self, monsters, damage_texts):
        pass

    def draw(self, screen, center_x, center_y):
        now = pygame.time.get_ticks()
        remaining = max(0, self.cd - (now - self.last_use))
        pygame.draw.circle(screen, (*self.color[:3], 60), (center_x, center_y), self.range, 2)
        font = get_font(20)
        text = font.render(f"{remaining // 1000}s", True, WHITE)
        screen.blit(text, (center_x - 15, center_y - self.range - 20))

    def upgrade(self):
        self.damage = int(self.damage * 1.35)
        self.range += 25
        self.cd = int(self.cd * 0.85)


class FireSkill(Skill):
    def __init__(self):
        super().__init__()
        self.cd = 8000
        self.damage = 30
        self.range = 150
        self.color = (255, 80, 0, 80)
        self.dmg_type = "fire"

    def release(self, monsters, damage_texts):
        now = pygame.time.get_ticks()
        if now - self.last_use > self.cd:
            self.last_use = now
            hit = False
            for m in monsters:
                if abs(m.x - W // 2) < self.range and abs(m.y - H // 2) < self.range:
                    m.hp -= self.damage
                    damage_texts.append(DamageText(m.x + m.size // 2, m.y, self.damage, self.dmg_type, False))
                    hit = True
            if hit and fire_hit_snd:
                fire_hit_snd.play()

    def upgrade(self):
        self.damage = int(self.damage * 1.35)
        self.range += 25
        self.cd = int(self.cd * 0.85)


class ThunderSkill(Skill):
    def __init__(self):
        super().__init__()
        self.cd = 12000
        self.damage = 80
        self.range = 250
        self.color = (255, 255, 0, 80)
        self.dmg_type = "electric"

    def release(self, monsters, damage_texts):
        now = pygame.time.get_ticks()
        if now - self.last_use > self.cd:
            self.last_use = now
            hit = False
            for m in monsters:
                if abs(m.x - W // 2) < self.range and abs(m.y - H // 2) < self.range:
                    m.hp -= self.damage
                    damage_texts.append(DamageText(m.x + m.size // 2, m.y, self.damage, self.dmg_type, False))
                    hit = True
            if hit and thunder_hit_snd:
                thunder_hit_snd.play()

    def upgrade(self):
        self.damage = int(self.damage * 1.35)
        self.range += 25
        self.cd = int(self.cd * 0.85)


# 新增冰系技能
class IceSkill(Skill):
    def __init__(self):
        super().__init__()
        self.cd = 10000
        self.damage = 50
        self.range = 200
        self.color = (80, 220, 255, 80)
        self.dmg_type = "ice"

    def release(self, monsters, damage_texts):
        now = pygame.time.get_ticks()
        if now - self.last_use > self.cd:
            self.last_use = now
            hit = False
            for m in monsters:
                if abs(m.x - W // 2) < self.range and abs(m.y - H // 2) < self.range:
                    m.hp -= self.damage
                    damage_texts.append(DamageText(m.x + m.size // 2, m.y, self.damage, self.dmg_type, False))
                    hit = True
            if hit and ice_hit_snd:
                ice_hit_snd.play()


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
