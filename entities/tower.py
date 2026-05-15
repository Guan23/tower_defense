# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 17:26
# @Author   : GuanXK
# @File     : tower.py

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


class Tower(ABC):
    def __init__(self, x, y, cell_idx):
        self.x = x
        self.y = y
        self.cell_idx = cell_idx
        self.size = TOWER_BASE_SIZE
        self.range = 0
        self.damage = 0
        self.fire_rate = 0
        self.last_shot = 0
        self.color = (100, 100, 100)
        self.img = load_image("assets/tower", (self.size, self.size))
        self.level = 1
        self.dmg_type = "physical"  # physical / fire / ice / electric
        self.bullets = []
        self.total_cost = 0

    @abstractmethod
    def get_info(self):
        pass

    def upgrade_cost(self):
        return int(40 * self.level * 1.2)

    def upgrade_stat(self):
        self.damage = int(self.damage * TOWER_UPGRADE_DMG)
        self.range += TOWER_UPGRADE_RANGE
        self.fire_rate = int(self.fire_rate * TOWER_UPGRADE_ATK_SPEED)

    def find_target(self, monsters, gate_y):
        if not monsters:
            return None
        best = None
        best_dist_gate = float('inf')
        for m in monsters:
            dist_self = ((m.x - self.x) ** 2 + (m.y - self.y) ** 2) ** 0.5
            if dist_self > self.range: continue
            dist_gate = gate_y - (m.y + m.size)
            if dist_gate < best_dist_gate:
                best = m
                best_dist_gate = dist_gate
        return best

    def shoot(self, monsters, gate_y):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            target = self.find_target(monsters, gate_y)
            if target:
                self.last_shot = now
                dx = target.x - self.x
                dy = target.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5 or 1
                fly_time = distance / BULLET_SPEED_TOWER
                px = target.x + target.speed_x * fly_time
                py = target.y + target.speed * fly_time
                pdx = px - self.x
                pdy = py - self.y
                pdis = (pdx ** 2 + pdy ** 2) ** 0.5 or 1

                bullet_rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)
                self.bullets.append({
                    "rect": bullet_rect, "dmg": self.damage,
                    "speed": BULLET_SPEED_TOWER,
                    "dir": (pdx / pdis, pdy / pdis),
                    "laser": False,
                    "dmg_type": self.dmg_type,
                    "from_tower": True
                })

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x - self.size // 2, self.y - self.size // 2))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size // 2)
        pygame.draw.circle(screen, (*self.color, 40), (self.x, self.y), self.range, 1)


# 普通塔 = 物理
class NormalTower(Tower):
    def __init__(self, x, y, cell_idx):
        super().__init__(x, y, cell_idx)
        self.range = TOWER_NORMAL_RANGE
        self.damage = TOWER_NORMAL_DAMAGE
        self.fire_rate = TOWER_NORMAL_ATK_SPEED
        self.color = (100, 100, 100)
        self.dmg_type = "physical"

    def get_info(self): return "普通炮塔"


# 冰塔 = 冰
class IceTower(Tower):
    def __init__(self, x, y, cell_idx):
        super().__init__(x, y, cell_idx)
        self.range = TOWER_ICE_RANGE
        self.damage = TOWER_ICE_DAMAGE
        self.fire_rate = TOWER_ICE_ATK_SPEED
        self.color = COLOR_ICE_BLUE
        self.dmg_type = "ice"

    def get_info(self): return "冰炮塔"


# 火塔 = 火
class FireTower(Tower):
    def __init__(self, x, y, cell_idx):
        super().__init__(x, y, cell_idx)
        self.range = TOWER_FIRE_RANGE
        self.damage = TOWER_FIRE_DAMAGE
        self.fire_rate = TOWER_FIRE_ATK_SPEED
        self.color = (255, 80, 0)
        self.dmg_type = "fire"

    def get_info(self): return "火炮塔"


# 电塔 = 电（新增）
class ElectricTower(Tower):
    def __init__(self, x, y, cell_idx):
        super().__init__(x, y, cell_idx)
        self.range = TOWER_ELEC_RANGE
        self.damage = TOWER_ELEC_DAMAGE
        self.fire_rate = TOWER_ELEC_ATK_SPEED
        self.color = COLOR_ELEC
        self.dmg_type = "electric"

    def get_info(self): return "电炮塔"


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
