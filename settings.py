# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:53
# @Author   : GuanXK
# @File     : settings.py

"""
info:

"""

# system

# third_party

# custom

# 屏幕
W = 480
H = 800
FPS = 60

WHITE = (255,255,255)
RED = (220,30,30)
GREEN = (30,200,30)
BLUE = (30,80,220)
YELLOW = (255,200,0)
GRAY = (40,40,40)
BLACK = (0,0,0)
PURPLE = (180,0,180)
ORANGE = (255,120,0)
ICE_BLUE = (80, 220, 255)

# 大门80%宽度
GATE_W = int(W * 0.8)
GATE_Y = H - 180

# 7等分，中间1格人物位，左右各3格建造
CELL_TOTAL = 7          # 7等分
CELL_BUILD = 6          # 实际可建造6格
CELL_W = GATE_W // CELL_TOTAL
CELL_START_X = (W - GATE_W) // 2
MIDDLE_CELL_IDX = 3     # 第4格为中间人物位(0~6)

# 音效配置
SOUND_PATHS = {
    "bullet_hit": "sounds/bullet_hit",
    "fire_hit": "sounds/fire_hit",
    "thunder_hit": "sounds/thunder_hit",
    "gate_hit": "sounds/gate_hit"
}


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
