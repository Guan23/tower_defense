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
from entities.damage_text import DamageText
from utils.sound_manager import bullet_hit_snd

class Tower(ABC):
    def __init__(self, x, y, cell_idx):
        self.x = x
        self.y = y
        self.cell_idx = cell_idx       # 所在格子索引
        self.size = 45
        self.range = 180
        self.damage = 12
        self.fire_rate = 800
        self.last_shot = 0
        self.color = (80,80,80)
        self.img = load_image("assets/tower", (self.size, self.size))
        self.level = 1
        self.dmg_type = "physical"
        self.bullets = []
        self.total_cost = 0  # 建造+升级总花费，用于摧毁返还

    @abstractmethod
    def get_info(self):
        pass

    def upgrade_cost(self):
        return int(40 * (self.level ** 1.3))

    def upgrade(self):
        cost = self.upgrade_cost()
        self.level += 1
        self.damage = int(self.damage * 1.4)
        self.range += 20
        self.fire_rate = int(self.fire_rate * 0.9)
        self.total_cost += cost
        return cost

    # 统一寻敌逻辑：离大门最近 → 离自身最近 → 靠左
    def find_target(self, monsters, gate_y):
        if not monsters:
            return None
        gate_line = gate_y
        best = None
        best_dist_gate = float("inf")
        best_dist_self = float("inf")
        best_x = float("inf")

        for m in monsters:
            dist_gate = gate_line - (m.y + m.size)
            dist_self = ((m.x - self.x)**2 + (m.y - self.y)**2)**0.5
            if dist_self > self.range:
                continue
            # 优先级判断
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

    def shoot(self, monsters, gate_y):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.fire_rate:
            target = self.find_target(monsters, gate_y)
            if target:
                self.last_shot = now
                dx = target.x - self.x
                dy = target.y - self.y
                dis = (dx**2 + dy**2)**0.5
                spd = 7
                bullet_rect = pygame.Rect(self.x-5, self.y-20, 10,10)
                self.bullets.append({
                    "rect": bullet_rect,
                    "dmg": self.damage,
                    "speed": spd,
                    "dir": (dx/dis, dy/dis),
                    "laser": False,
                    "dmg_type": self.dmg_type,
                    "from_tower": True
                })

    def draw(self, screen):
        if self.img:
            screen.blit(self.img, (self.x-self.size//2, self.y-self.size//2))
        else:
            pygame.draw.circle(screen, self.color, (self.x,self.y), self.size//2)
        pygame.draw.circle(screen, (*self.color,40), (self.x,self.y), self.range, 1)

# 普通炮塔 物理
class NormalTower(Tower):
    def __init__(self,x,y,cell_idx):
        super().__init__(x,y,cell_idx)
        self.dmg_type = "physical"
        self.color = (100,100,100)
    def get_info(self): return "普通炮塔"

# 冰炮塔
class IceTower(Tower):
    def __init__(self,x,y,cell_idx):
        super().__init__(x,y,cell_idx)
        self.dmg_type = "ice"
        self.damage = 10
        self.range = 200
        self.color = ICE_BLUE
    def get_info(self): return "冰炮塔"

# 火炮塔
class FireTower(Tower):
    def __init__(self,x,y,cell_idx):
        super().__init__(x,y,cell_idx)
        self.dmg_type = "fire"
        self.damage = 18
        self.range = 160
        self.color = (255,80,0)
    def get_info(self): return "火炮塔"



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
