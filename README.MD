zombie_tower/
├── main.py               # 游戏入口
├── settings.py           # 配置、颜色、屏幕
├── assets/           # UI图标
│   ├── player.png    # 玩家
│   ├── gate.png      # 大门
│   ├── monster.png   # 普通怪
│   ├── elite.png     # 精英怪
│   ├── boss.png      # BOSS
│   ├── bullet.png    # 子弹
│   └── gun.png       # 枪支
│
├── sounds/ 
│   ├── bgm.mp3          # 背景音乐
│   ├── shoot.wav        # 开枪音效
│   ├── bullet_hit.wav   # 子弹命中音效
│   ├── fire_hit.wav     # 火焰技能命中音效
│   ├── thunder_hit.wav  # 雷电技能命中音效
│   ├── ice_hit.wav      # 冰技能命中音效
│   └── gate_hit.wav     # 怪物命中大门音效
│
├── factory/              # 抽象工厂 + 具体工厂
│   ├── __init__.py
│   ├── game_factory.py   # 抽象工厂基类
│   └── zombie_factory.py # 僵尸游戏具体工厂
│
├── entities/             # 所有游戏实体（父类+子类）
│   ├── __init__.py
│   ├── monster.py        # 怪物父类 + 各种僵尸
│   ├── player.py         # 主角父类 + 主角
│   ├── gate.py           # 大门父类 + 基地
│   ├── gun.py            # 枪支父类 + 各种枪
│   └── skill.py          # 技能父类 + 火焰/雷电技能
└── tools.py              # 工具（字体、碰撞等）

