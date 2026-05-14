# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 16:23
# @Author   : GuanXK
# @File     : demage_text.py

"""
info:

"""

# system

# third_party

# custom

import pygame
from abc import ABC
from tools import get_font

# 伤害颜色配置
DAMAGE_COLOR = {
    "physical": (255, 255, 255),   # 物理：白色
    "fire": (255, 80, 0),          # 火：橙红
    "ice": (80, 180, 255),         # 冰：浅蓝
    "electric": (255, 255, 0)      # 电：黄色
}

class DamageText(ABC):
    def __init__(self, x, y, damage, dmg_type="physical", is_crit=False):
        self.x = x
        self.y = y
        self.damage = damage
        self.dmg_type = dmg_type
        self.is_crit = is_crit

        # 字体大小：暴击放大50%
        self.base_size = 20
        self.font_size = int(self.base_size * 1.5) if self.is_crit else self.base_size
        self.color = DAMAGE_COLOR[self.dmg_type]

        self.life = 60       # 存活帧数
        self.vy = -2         # 向上飘速度
        self.font = get_font(self.font_size)

    def update(self):
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        alpha = max(0, int(255 * (self.life / 60)))
        text = f"-{self.damage}"
        surf = self.font.render(text, True, self.color)
        surf.set_alpha(alpha)
        screen.blit(surf, (self.x, self.y))


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
