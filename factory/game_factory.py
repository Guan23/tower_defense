# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:54
# @Author   : GuanXK
# @File     : game_factory.py.py

"""
info:

"""

# system

# third_party

# custom

from abc import ABC, abstractmethod

class GameFactory(ABC):
    @abstractmethod
    def create_monster(self, wave):
        pass

    @abstractmethod
    def create_gun(self, name):
        pass

    @abstractmethod
    def create_skill(self, name):
        pass


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
