# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:54
# @Author   : GuanXK
# @File     : zombie_factory.py.py

"""
info:

"""

# system

# third_party

# custom

from factory.game_factory import GameFactory
from entities.monster import NormalMonster, EliteMonster, BossMonster
from entities.gun import NormalGun, LaserGun
from entities.skill import FireSkill, ThunderSkill, IceSkill
from entities.tower import NormalTower, IceTower, FireTower, ElectricTower
import random
from settings import *


class ZombieGameFactory(GameFactory):
    def create_monster(self, wave):
        x = random.randint(50, SCREEN_W - 50)
        if wave < 3:
            return NormalMonster(x)
        elif wave < 6:
            return EliteMonster(x)
        else:
            if random.random() < 0.1:
                return BossMonster(x)
            return EliteMonster(x)

    def create_gun(self, name):
        if name == "normal":
            return NormalGun()
        elif name == "laser":
            return LaserGun()

    def create_skill(self, name):
        if name == "fire":
            return FireSkill()
        elif name == "thunder":
            return ThunderSkill()
        elif name == "ice":
            return IceSkill()

    # 加入电塔
    def create_tower(self, type_name, x, y, cell_idx):
        if type_name == "normal":
            return NormalTower(x, y, cell_idx)
        elif type_name == "ice":
            return IceTower(x, y, cell_idx)
        elif type_name == "fire":
            return FireTower(x, y, cell_idx)
        elif type_name == "electric":
            return ElectricTower(x, y, cell_idx)


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
