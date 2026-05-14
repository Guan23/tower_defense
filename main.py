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
from tools import load_image, get_font
from utils.sound_manager import bullet_hit_snd, gate_hit_snd, play_bgm

if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()

    # 启动背景音乐
    play_bgm()

    bullet_img = load_image("assets/bullet", (10, 10))

    factory = ZombieGameFactory()
    player = NormalPlayer()
    gate = HomeGate()
    gun = factory.create_gun("normal")
    fire = FireSkill()
    thunder = ThunderSkill()
    ice = IceSkill()  # 冰系技能实例

    monsters = []
    wave = 1
    spawn_timer = 0
    damage_texts = []

    running = True
    while running:
        screen.fill(GRAY)
        now = pygame.time.get_ticks()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                player.x = event.pos[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire.release(monsters, damage_texts)
                if event.key == pygame.K_t:
                    thunder.release(monsters, damage_texts)
                if event.key == pygame.K_c:  # C键释放冰系技能
                    ice.release(monsters, damage_texts)

        gun.shoot(player.x, player.y)

        if now - spawn_timer > 1500:
            spawn_timer = now
            monsters.append(factory.create_monster(wave))

        # 更新怪物
        for m in monsters[:]:
            m.update()
            if m.y + m.size > gate.y and m.y < gate.y + gate.h:
                gate.hp -= m.damage
                damage_texts.append(DamageText(gate.x, gate.y - 20, m.damage, "physical", False))
                if gate_hit_snd:
                    gate_hit_snd.play()
                monsters.remove(m)
            if m.hp <= 0:
                player.gold += 10
                monsters.remove(m)

        # 子弹碰撞
        bullets_to_remove = []
        for bullet in gun.bullets:
            bullet["rect"].y -= bullet["speed"]
            if bullet["rect"].bottom < 0:
                bullets_to_remove.append(bullet)
                continue
            for m in monsters:
                monster_rect = pygame.Rect(m.x, m.y, m.size, m.size)
                if bullet["rect"].colliderect(monster_rect):
                    dmg = bullet["dmg"]
                    is_crit = random.random() < 0.1
                    if is_crit:
                        dmg = int(dmg * 1.5)
                    m.hp -= dmg
                    damage_texts.append(DamageText(m.x + m.size // 2, m.y, dmg, "physical", is_crit))
                    if bullet_hit_snd:
                        bullet_hit_snd.play()
                    bullets_to_remove.append(bullet)
                    break
        for b in bullets_to_remove:
            if b in gun.bullets:
                gun.bullets.remove(b)

        # 飘字
        for dt in damage_texts[:]:
            dt.update()
            dt.draw(screen)
            if dt.life <= 0:
                damage_texts.remove(dt)

        # 绘制
        gate.draw(screen)
        player.draw(screen)
        if gun.img:
            screen.blit(gun.img, (player.x - 15, player.y - 40))

        for m in monsters:
            m.draw(screen)

        for b in gun.bullets:
            if bullet_img:
                screen.blit(bullet_img, b["rect"])
            else:
                color = YELLOW if b["laser"] else WHITE
                pygame.draw.circle(screen, color, b["rect"].center, 5)

        # 绘制三个技能范围
        fire.draw(screen, W // 2, H // 2)
        thunder.draw(screen, W // 2, H // 2)
        ice.draw(screen, W // 2, H // 2)

        # UI
        font = get_font(24)
        screen.blit(font.render(f"金币：{player.gold}", True, WHITE), (10, 10))
        screen.blit(font.render(f"大门HP：{gate.hp}", True, WHITE), (10, 35))
        screen.blit(font.render(f"波次：{wave}", True, WHITE), (10, 60))
        screen.blit(font.render("空格=火焰  T=雷电  C=冰系", True, ORANGE), (10, 740))

        if gate.hp <= 0:
            big_font = get_font(60)
            screen.blit(big_font.render("游戏结束", True, RED), (W // 2 - 80, H // 2))

        pygame.display.flip()

    pygame.quit()

    print("\n----------------- end -----------------\n")
