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
# ==============================================
# 塔防游戏 - 全局配置文件（100% 可配置 + 自适应屏幕）
# ==============================================

# -------------------------- 屏幕基础（仅这2个是定值） --------------------------
SCREEN_W = 480              # 屏幕宽度（固定值）
SCREEN_H = 800              # 屏幕高度（固定值）
FPS = 60                   # 游戏刷新帧率

# -------------------------- 颜色配置 --------------------------
COLOR_WHITE  = (255, 255, 255)   # 白色
COLOR_RED    = (220, 30, 30)     # 红色
COLOR_GREEN  = (30, 200, 30)     # 绿色
COLOR_BLUE   = (30, 80, 220)     # 蓝色
COLOR_YELLOW = (255, 200, 0)     # 黄色
COLOR_GRAY   = (40, 40, 40)      # 灰色
COLOR_BLACK  = (0, 0, 0)         # 黑色
COLOR_ORANGE = (255, 120, 0)     # 橙色
COLOR_ICE_BLUE = (80, 220, 255)  # 冰蓝色
COLOR_ELEC = (200, 200, 0)       # 电属性黄色

# -------------------------- 布局比例（自适应分辨率） --------------------------
GATE_WIDTH_RATIO = 0.8         # 大门宽度占屏幕宽度比例
GATE_Y_FROM_BOTTOM = 0.225     # 大门距离底部比例
CELL_TOTAL_SECTIONS = 7        # 建造格子总数量
MIDDLE_CELL_INDEX = 3          # 中间格子（玩家枪所在）
CELL_HEIGHT_RATIO = 0.0625     # 建造格子高度比例
CELL_PADDING_RATIO = 0.1       # 格子间距比例

# -------------------------- 自动计算布局（无需修改） --------------------------
GATE_W = int(SCREEN_W * GATE_WIDTH_RATIO)
GATE_Y = int(SCREEN_H - SCREEN_H * GATE_Y_FROM_BOTTOM)
CELL_TOTAL = CELL_TOTAL_SECTIONS
CELL_RAW_W = GATE_W / CELL_TOTAL_SECTIONS
CELL_FINAL_W = int(CELL_RAW_W * (1 - CELL_PADDING_RATIO))
CELL_H = int(SCREEN_H * CELL_HEIGHT_RATIO)
CELL_START_X = (SCREEN_W - GATE_W) // 2

# -------------------------- 炮塔UI配置（保卫萝卜风格） --------------------------
TOWER_UI_ICON_SIZE = 40        # 炮塔选择图标尺寸
TOWER_UI_BTN_SIZE = 40         # 升级/出售/取消按钮尺寸
TOWER_UI_SPACING = 5           # 按钮间距
MAX_TOWER_LEVEL = 6            # 炮塔最大等级（1级初始）
SELL_RETURN_RATIO = 0.8        # 出售返还金币比例（80%）

# -------------------------- 玩家枪升级系统配置 --------------------------
MAX_GUN_LEVEL = 16                     # 枪最大等级 15级
GUN_UPGRADE_COST_BASE = 80             # 枪基础升级费用
GUN_UPGRADE_COST_MULTI = 1.2           # 升级费用递增系数
GUN_CRITICAL_LEVELS = [3,6,9,12,15]    # 特殊等级：弹道+1 / 连发+1
GUN_INIT_BALLISTIC = 1                 # 初始弹道数量（扇形子弹数）
GUN_INIT_BURST = 1                     # 初始连发数量（串行发射次数）
GUN_BALLISTIC_ANGLE_STEP = 2.0         # 每多1条弹道，左右各偏移角度(度)
GUN_BURST_DELAY_MS = 80                # 连发子弹之间发射延迟(毫秒)，远小于主发射间隔

# -------------------------- 玩家初始属性 --------------------------
PLAYER_INIT_GOLD = 20000         # 初始金币
PLAYER_INIT_HP = 100           # 初始血量
PLAYER_SIZE = 40               # 玩家大小

# -------------------------- 炮塔建造价格 --------------------------
TOWER_COST_NORMAL = 40         # 普通炮塔价格
TOWER_COST_ICE = 80            # 冰炮塔价格
TOWER_COST_FIRE = 100          # 火炮塔价格
TOWER_COST_ELEC = 120          # 电炮塔价格

# -------------------------- 炮塔升级成长属性 --------------------------
TOWER_BASE_SIZE = 45           # 炮塔基础大小
TOWER_UPGRADE_DMG = 1.4        # 伤害成长系数
TOWER_UPGRADE_RANGE = 20       # 射程成长值
TOWER_UPGRADE_ATK_SPEED = 0.9  # 攻击速度成长系数

# -------------------------- 炮塔基础属性 --------------------------
TOWER_NORMAL_RANGE = 180
TOWER_NORMAL_DAMAGE = 12
TOWER_NORMAL_ATK_SPEED = 800
TOWER_ICE_RANGE = 200
TOWER_ICE_DAMAGE = 10
TOWER_ICE_ATK_SPEED = 800
TOWER_FIRE_RANGE = 160
TOWER_FIRE_DAMAGE = 18
TOWER_FIRE_ATK_SPEED = 800
TOWER_ELEC_RANGE = 220
TOWER_ELEC_DAMAGE = 15
TOWER_ELEC_ATK_SPEED = 700

# -------------------------- 子弹配置 --------------------------
BULLET_SIZE_W = 10
BULLET_SIZE_H = 10
BULLET_SPEED_PLAYER_NORMAL = 8
BULLET_SPEED_PLAYER_LASER = 12
BULLET_SPEED_TOWER = 7

# -------------------------- 怪物通用配置 --------------------------
MONSTER_BASE_SPEED = 1.5       # 基础移速
MONSTER_SIZE = 30              # 基础大小
MONSTER_DAMAGE_TO_GATE = 10    # 攻击大门伤害
MONSTER_KILL_REWARD = 10       # 击杀奖励金币
MONSTER_SPAWN_INTERVAL = 500  # 刷怪间隔

# -------------------------- 怪物属性 + 四系抗性（0~1） --------------------------
MONSTER_NORMAL_HP = 30
MONSTER_NORMAL_PHYS_RES = 0.0
MONSTER_NORMAL_FIRE_RES = 0.0
MONSTER_NORMAL_ICE_RES = 0.0
MONSTER_NORMAL_ELEC_RES = 0.0
MONSTER_ELITE_HP = 80
MONSTER_ELITE_PHYS_RES = 0.6
MONSTER_ELITE_FIRE_RES = 0.1
MONSTER_ELITE_ICE_RES = 0.1
MONSTER_ELITE_ELEC_RES = 0.1
MONSTER_BOSS_HP = 300
MONSTER_BOSS_PHYS_RES = 0.8
MONSTER_BOSS_FIRE_RES = 0.3
MONSTER_BOSS_ICE_RES = 0.3
MONSTER_BOSS_ELEC_RES = -0.2

# -------------------------- 玩家枪支基础配置 --------------------------
GUN_INIT_DAMAGE = 8
GUN_INIT_ATK_SPEED = 800
GUN_UPGRADE_COST = 60
GAN_UPGRADE_DMG = 1.3
GUN_UPGRADE_SPEED = 0.85

# -------------------------- 技能配置 --------------------------
SKILL_UPGRADE_COST = 100
SKILL_UPGRADE_DMG = 1.35
SKILL_UPGRADE_RANGE = 25
SKILL_UPGRADE_CD = 0.85
SKILL_FIRE_BASE_DMG = 25
SKILL_FIRE_BASE_RANGE = 200
SKILL_FIRE_BASE_CD = 3200
SKILL_THUNDER_BASE_DMG = 40
SKILL_THUNDER_BASE_RANGE = 160
SKILL_THUNDER_BASE_CD = 4000
SKILL_ICE_BASE_DMG = 20
SKILL_ICE_BASE_RANGE = 240
SKILL_ICE_BASE_CD = 3600



if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
