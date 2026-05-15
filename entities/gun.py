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
import math
from settings import *
from tools import load_image
from utils.sound_manager import shoot_snd

class Gun(ABC):
    def __init__(self):
        self.damage = GUN_INIT_DAMAGE
        self.fire_rate = GUN_INIT_ATK_SPEED   # 射速永久不变
        self.speed = BULLET_SPEED_PLAYER_NORMAL
        self.last_shot = 0
        self.bullets = []
        self.img = load_image("assets/gun", (30, 30))
        self.dmg_type = "physical"

        self.level = 1
        self.ballistic = GUN_INIT_BALLISTIC   # 并行子弹数：一轮内同时射出的扇形子弹
        self.burst = GUN_INIT_BURST           # 串行轮数：先后发射多轮完整并行扇形
        self.burst_shot_times = []            # 记录每一轮串行发射时间

    def upgrade_cost(self):
        return int(GUN_UPGRADE_COST_BASE * (self.level ** GUN_UPGRADE_COST_MULTI))

    def normal_upgrade(self):
        """普通升级：**只提升攻击力**，射速、弹道、连发完全不变"""
        self.level += 1
        self.damage = int(self.damage * GAN_UPGRADE_DMG)

    def add_ballistic(self):
        """弹道+1：一轮内并行扇形子弹数量+1"""
        self.level += 1
        self.ballistic += 1

    def add_burst(self):
        """连发+1：串行发射轮数+1"""
        self.level += 1
        self.burst += 1

    def find_target(self, monsters, gate_y):
        if not monsters:
            return None
        best = None
        best_dist_gate = float('inf')
        for m in monsters:
            dist_gate = gate_y - (m.y + m.size)
            if dist_gate < best_dist_gate:
                best = m
                best_dist_gate = dist_gate
        return best

    def shoot(self, px, py, monsters, gate_y):
        now = pygame.time.get_ticks()

        # 规则1：场上无怪物 → 完全不发射，清空连发队列
        target = self.find_target(monsters, gate_y)
        if target is None:
            self.burst_shot_times.clear()
            return

        # 清理过期的连发时间记录
        self.burst_shot_times = [t for t in self.burst_shot_times if now - t < self.fire_rate]

        # 主发射冷却结束 → 开启新一轮【burst 轮】串行发射
        if len(self.burst_shot_times) == 0 and now - self.last_shot > self.fire_rate:
            self.last_shot = now
            # 生成 burst 轮的发射时间：每轮间隔 GUN_BURST_DELAY_MS
            self.burst_shot_times = [now + i * GUN_BURST_DELAY_MS for i in range(self.burst)]

        # 找出当前时间应该发射的轮次
        fire_indices = [i for i, t in enumerate(self.burst_shot_times) if now >= t]
        for idx in fire_indices:
            # 预测怪物，获得基础发射角度
            dx = target.x - px
            dy = target.y - py
            dis = math.hypot(dx, dy) or 1
            fly_time = dis / self.speed
            px_t = target.x + target.speed_x * fly_time
            py_t = target.y + target.speed * fly_time
            base_angle = math.degrees(math.atan2(py_t - py, px_t - px))

            # 规则3：一轮内发射【ballistic 个并行扇形子弹】，对称偏移
            angle_step = GUN_BALLISTIC_ANGLE_STEP
            # 计算起始角度，保证整体对称
            start_angle = base_angle - (self.ballistic - 1) * angle_step
            for b_idx in range(self.ballistic):
                current_angle = start_angle + b_idx * 2 * angle_step
                rad = math.radians(current_angle)
                dir_x = math.cos(rad)
                dir_y = math.sin(rad)

                bullet_rect = pygame.Rect(px - 5, py - 5, BULLET_SIZE_W, BULLET_SIZE_H)
                self.bullets.append({
                    "rect": bullet_rect,
                    "dmg": self.damage,
                    "speed": self.speed,
                    "dir": (dir_x, dir_y),
                    "laser": False,
                    "dmg_type": self.dmg_type,
                    "from_tower": False
                })

            # 移除已发射的这一轮
            self.burst_shot_times.pop(idx)
            if shoot_snd:
                shoot_snd.play()

class NormalGun(Gun):
    def __init__(self):
        super().__init__()
        self.dmg_type = "physical"

class LaserGun(Gun):
    def __init__(self):
        super().__init__()
        self.damage = 40
        self.fire_rate = 800
        self.speed = BULLET_SPEED_PLAYER_LASER
        self.dmg_type = "electric"



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
