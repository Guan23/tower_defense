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
from entities.skill import FireSkill, ThunderSkill
import random


class ZombieGameFactory(GameFactory):
    def create_monster(self, wave):
        if wave < 3:
            return NormalMonster()
        elif wave < 6:
            return EliteMonster()
        else:
            if random.random() < 0.08:
                return BossMonster()
            return EliteMonster()

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


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
