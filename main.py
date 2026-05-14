# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:50
# @Author   : GuanXK
# @File     : main.py

"""
info:

"""

# system
import os
import random

# third_party
import pygame

# custom
import pygame
import random
from settings import *
from factory.zombie_factory import ZombieGameFactory
from entities.player import NormalPlayer
from entities.gate import HomeGate
from entities.damage_text import DamageText
from entities.skill import FireSkill, ThunderSkill, IceSkill
from entities.tower import NormalTower, IceTower, FireTower
from tools import load_image, get_font
from utils.sound_manager import bullet_hit_snd, gate_hit_snd, play_bgm

if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    import pygame
    import random
    from settings import *
    from factory.zombie_factory import ZombieGameFactory
    from entities.player import NormalPlayer
    from entities.gate import HomeGate
    from entities.damage_text import DamageText
    from entities.skill import FireSkill, ThunderSkill, IceSkill
    from entities.tower import NormalTower, IceTower, FireTower
    from tools import load_image, get_font
    from utils.sound_manager import bullet_hit_snd, gate_hit_snd, play_bgm

    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    # 播放背景音乐
    play_bgm()
    # 加载子弹图片
    bullet_img = load_image("assets/bullet", (10, 10))

    # 创建工厂、玩家、大门、枪支、三大技能
    factory = ZombieGameFactory()
    player = NormalPlayer()
    gate = HomeGate()
    gun = factory.create_gun("normal")
    fire = FireSkill()
    thunder = ThunderSkill()
    ice = IceSkill()

    # 游戏对象容器
    monsters = []  # 怪物列表
    towers = []  # 炮塔列表
    wave = 1  # 当前波次
    spawn_timer = 0  # 刷怪计时器
    damage_texts = []  # 伤害飘字列表

    # -------------------------- 建造格子配置 --------------------------
    cell_occupied = [False] * CELL_TOTAL  # 7个格子占用状态 0~6
    buildable_cell = [0, 1, 2, 4, 5, 6]  # 可建造格子：左3 右3，中间3号不可建造
    BUILD_COST = {"normal": 40, "ice": 80, "fire": 100}  # 炮塔建造金币

    # 升级花费
    UPGRADE_COST_GUN = 60
    UPGRADE_COST_SKILL = 100
    gun_level = 1
    fire_lv = 1
    thunder_lv = 1
    ice_lv = 1

    build_mode = None  # 建造模式: None / normal / ice / fire
    selected_tower = None  # 当前选中的炮塔，用于升级/摧毁

    # 游戏主循环
    running = True
    while running:
        screen.fill(GRAY)
        now = pygame.time.get_ticks()
        clock.tick(FPS)

        # -------------------------- 绘制7个建造格子 --------------------------
        for i in range(CELL_TOTAL):
            cx = CELL_START_X + i * CELL_W
            cy = GATE_Y + gate.h + 10
            rect = pygame.Rect(cx, cy, CELL_W - 2, 50)
            # 中间格子为人物位置，不可建造，深灰色
            if i == MIDDLE_CELL_IDX:
                pygame.draw.rect(screen, (40, 40, 40), rect, 2)
            else:
                # 已建造/未建造区分颜色
                color = (60, 60, 60) if cell_occupied[i] else (90, 90, 90)
                pygame.draw.rect(screen, color, rect, 2)

        # -------------------------- 事件处理：按键+鼠标 --------------------------
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                running = False

            # 键盘按下事件
            if event.type == pygame.KEYDOWN:
                # 释放技能
                if event.key == pygame.K_SPACE:
                    fire.release(monsters, damage_texts)
                if event.key == pygame.K_t:
                    thunder.release(monsters, damage_texts)
                if event.key == pygame.K_c:
                    ice.release(monsters, damage_texts)

                # 切换建造模式
                if event.key == pygame.K_1:
                    build_mode = "normal"
                if event.key == pygame.K_2:
                    build_mode = "ice"
                if event.key == pygame.K_3:
                    build_mode = "fire"
                if event.key == pygame.K_0:
                    build_mode = None
                    selected_tower = None

                # 升级玩家枪支
                if event.key == pygame.K_q and player.gold >= UPGRADE_COST_GUN:
                    player.gold -= UPGRADE_COST_GUN
                    gun_level += 1
                    gun.damage = int(gun.damage * 1.3)
                    gun.fire_rate = int(gun.fire_rate * 0.85)

                # 升级三大技能
                if event.key == pygame.K_f and player.gold >= UPGRADE_COST_SKILL:
                    player.gold -= UPGRADE_COST_SKILL
                    fire.upgrade()
                    fire_lv += 1
                if event.key == pygame.K_r and player.gold >= UPGRADE_COST_SKILL:
                    player.gold -= UPGRADE_COST_SKILL
                    thunder.upgrade()
                    thunder_lv += 1
                if event.key == pygame.K_v and player.gold >= UPGRADE_COST_SKILL:
                    player.gold -= UPGRADE_COST_SKILL
                    ice.upgrade()
                    ice_lv += 1

                # U：升级选中的炮塔
                if event.key == pygame.K_u and selected_tower:
                    cost = selected_tower.upgrade_cost()
                    if player.gold >= cost:
                        player.gold -= cost
                        selected_tower.upgrade()

                # D：摧毁选中的炮塔，返还80%总花费
                if event.key == pygame.K_d and selected_tower:
                    refund = int(selected_tower.total_cost * 0.8)
                    player.gold += refund
                    cell_occupied[selected_tower.cell_idx] = False
                    towers.remove(selected_tower)
                    selected_tower = None

            # 鼠标点击：建造炮塔 / 选中炮塔
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i in range(CELL_TOTAL):
                    cx = CELL_START_X + i * CELL_W
                    cy = GATE_Y + gate.h + 10
                    # 点击格子区域
                    if cx <= mx <= cx + CELL_W and cy <= my <= cy + 50:
                        # 只能在可建造格子建造
                        if i in buildable_cell and build_mode and not cell_occupied[i]:
                            cost = BUILD_COST[build_mode]
                            if player.gold >= cost:
                                player.gold -= cost
                                tx = cx + CELL_W // 2
                                ty = cy + 25
                                # 创建炮塔，传入格子索引
                                t = factory.create_tower(build_mode, tx, ty, i)
                                t.total_cost = cost
                                towers.append(t)
                                cell_occupied[i] = True
                                build_mode = None
                        # 点击已有炮塔 → 选中
                        for t in towers:
                            if abs(mx - t.x) < t.size and abs(my - t.y) < t.size:
                                selected_tower = t
                                break

        # -------------------------- 玩家枪支自动射击（智能寻敌） --------------------------
        gun.shoot(player.x, player.y, monsters, GATE_Y)

        # -------------------------- 定时刷怪 --------------------------
        if now - spawn_timer > 1500:
            spawn_timer = now
            monsters.append(factory.create_monster(wave))

        # -------------------------- 怪物更新：移动+撞击大门+死亡 --------------------------
        for m in monsters[:]:
            m.update()
            # 先标记是否需要删除
            need_remove = False

            # 怪物撞击大门
            if m.y + m.size > gate.y and m.y < gate.y + gate.h:
                gate.hp -= m.damage
                damage_texts.append(DamageText(gate.x, gate.y - 20, m.damage, "physical", False))
                if gate_hit_snd:
                    gate_hit_snd.play()
                need_remove = True

            # 怪物死亡，获得金币
            if m.hp <= 0 and not need_remove:
                player.gold += 10
                need_remove = True

            # 统一删除，避免重复移除报错
            if need_remove and m in monsters:
                monsters.remove(m)

        # -------------------------- 炮塔射击 + 子弹位移 --------------------------
        for t in towers:
            t.shoot(monsters, GATE_Y)
            for b in t.bullets:
                b["rect"].x += b["dir"][0] * b["speed"]
                b["rect"].y += b["dir"][1] * b["speed"]

        # 玩家子弹位移
        for b in gun.bullets:
            b["rect"].x += b["dir"][0] * b["speed"]
            b["rect"].y += b["dir"][1] * b["speed"]

        # -------------------------- 子弹碰撞检测（精准，无持续伤害） --------------------------
        all_bullets = gun.bullets + [b for t in towers for b in t.bullets]
        bullets_to_remove = []
        for bullet in all_bullets:
            # 子弹飞出屏幕，标记删除
            if bullet["rect"].top > H or bullet["rect"].bottom < 0 or bullet["rect"].left < 0 or bullet[
                "rect"].right > W:
                bullets_to_remove.append(bullet)
                continue

            hit = False
            for m in monsters:
                mr = pygame.Rect(m.x, m.y, m.size, m.size)
                if bullet["rect"].colliderect(mr):
                    # 计算伤害+暴击
                    dmg = bullet["dmg"]
                    crit = random.random() < 0.1
                    if crit:
                        dmg = int(dmg * 1.5)

                    m.hp -= dmg
                    # 生成伤害飘字
                    damage_texts.append(DamageText(m.x + m.size // 2, m.y, dmg, bullet["dmg_type"], crit))

                    # 玩家子弹播放命中音效，炮塔子弹不播放
                    if not bullet.get("from_tower") and bullet_hit_snd:
                        bullet_hit_snd.play()

                    bullets_to_remove.append(bullet)
                    hit = True
                    break
            if hit:
                continue

        # 统一删除子弹
        for b in bullets_to_remove:
            if b in gun.bullets:
                gun.bullets.remove(b)
            for t in towers:
                if b in t.bullets:
                    t.bullets.remove(b)

        # -------------------------- 更新并绘制伤害飘字 --------------------------
        for dt in damage_texts[:]:
            dt.update()
            dt.draw(screen)
            if dt.life <= 0:
                damage_texts.remove(dt)

        # -------------------------- 绘制所有游戏元素 --------------------------
        gate.draw(screen)
        player.draw(screen)
        # 绘制枪支
        if gun.img:
            screen.blit(gun.img, (player.x - 15, player.y - 40))

        # 绘制炮塔，选中的炮塔加黄色外框
        for t in towers:
            t.draw(screen)
            if selected_tower is t:
                pygame.draw.circle(screen, YELLOW, (t.x, t.y), t.size // 2 + 5, 2)

        # 绘制怪物
        for m in monsters:
            m.draw(screen)

        # 绘制子弹
        for b in gun.bullets + [b for t in towers for b in t.bullets]:
            if bullet_img:
                screen.blit(bullet_img, b["rect"])
            else:
                c = YELLOW if b["laser"] else WHITE
                pygame.draw.circle(screen, c, b["rect"].center, 5)

        # 绘制技能范围与CD
        fire.draw(screen, W // 2, H // 2)
        thunder.draw(screen, W // 2, H // 2)
        ice.draw(screen, W // 2, H // 2)

        # -------------------------- UI文字信息 --------------------------
        font = get_font(20)
        screen.blit(font.render(f"金币:{player.gold}", True, WHITE), (10, 10))
        screen.blit(font.render(f"大门HP:{gate.hp}", True, WHITE), (10, 30))
        screen.blit(font.render(f"波次:{wave}", True, WHITE), (10, 50))
        screen.blit(font.render("1普通塔40  2冰塔80  3火塔100  |  选中塔: U升级  D摧毁", True, YELLOW), (10, 740))
        screen.blit(font.render("空格=火焰  T=雷电  C=冰  0取消建造", True, ORANGE), (10, 765))

        # 游戏结束
        if gate.hp <= 0:
            bf = get_font(60)
            screen.blit(bf.render("游戏结束", True, RED), (W // 2 - 80, H // 2))

        pygame.display.flip()

    pygame.quit()

    print("\n----------------- end -----------------\n")
