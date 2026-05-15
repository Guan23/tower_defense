# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:50
# @Author   : GuanXK
# @File     : main.py

"""
info:

"""

# system


# third_party


# custom


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
    from entities.tower import NormalTower, IceTower, FireTower, ElectricTower
    from tools import load_image, get_font
    from utils.sound_manager import bullet_hit_snd, gate_hit_snd, play_bgm

    # 初始化
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    play_bgm()

    # 加载图片
    bullet_img = load_image("assets/bullet", (BULLET_SIZE_W, BULLET_SIZE_H))
    btn_upgrade = load_image("assets/btn_upgrade", (TOWER_UI_BTN_SIZE, TOWER_UI_BTN_SIZE))
    btn_sell = load_image("assets/btn_sell", (TOWER_UI_BTN_SIZE, TOWER_UI_BTN_SIZE))
    btn_cancel = load_image("assets/btn_cancel", (TOWER_UI_BTN_SIZE, TOWER_UI_BTN_SIZE))

    # 炮塔建造列表（含电塔）
    TOWER_SELECT_DATA = [
        {"type": "normal", "cost": TOWER_COST_NORMAL, "color": (100, 100, 100), "name": "普通"},
        {"type": "ice", "cost": TOWER_COST_ICE, "color": COLOR_ICE_BLUE, "name": "冰塔"},
        {"type": "fire", "cost": TOWER_COST_FIRE, "color": (255, 80, 0), "name": "火塔"},
        {"type": "electric", "cost": TOWER_COST_ELEC, "color": COLOR_ELEC, "name": "电塔"},
    ]

    # 游戏核心
    factory = ZombieGameFactory()
    player = NormalPlayer()
    gate = HomeGate()
    gun = factory.create_gun("normal")
    fire_skill = FireSkill()
    thunder_skill = ThunderSkill()
    ice_skill = IceSkill()

    monsters = []
    towers = []
    wave = 1
    spawn_timer = 0
    damage_texts = []

    cell_occupied = [False] * CELL_TOTAL
    buildable_cells = [0, 1, 2, 4, 5, 6]

    # UI状态
    show_tower_buy = False
    selected_cell = -1
    show_tower_menu = False
    selected_tower = None
    show_gun_menu = False
    tip_text = ""
    tip_time = 0

    # 主循环
    running = True
    while running:
        screen.fill(COLOR_GRAY)
        now = pygame.time.get_ticks()
        clock.tick(FPS)

        # 绘制建造格子
        cell_rects = []
        for i in range(CELL_TOTAL):
            x = CELL_START_X + i * int(CELL_RAW_W)
            y = GATE_Y + gate.h + 10
            r = pygame.Rect(x, y, CELL_FINAL_W, CELL_H)
            cell_rects.append(r)
            if i == MIDDLE_CELL_INDEX:
                pygame.draw.rect(screen, (60, 80, 100), r, 2)
                font = get_font(22)
                screen.blit(font.render(f"Lv{gun.level}", True, COLOR_WHITE), (x + 8, y + 6))
                if gun.level < MAX_GUN_LEVEL and player.gold >= gun.upgrade_cost():
                    screen.blit(get_font(20).render("↑", True, COLOR_GREEN), (x + CELL_FINAL_W - 20, y - 15))
            else:
                c = (60, 60, 60) if cell_occupied[i] else (90, 90, 90)
                pygame.draw.rect(screen, c, r, 2)
                if not cell_occupied[i]:
                    screen.blit(get_font(24).render("+", True, COLOR_WHITE),
                                (x + CELL_FINAL_W // 2 - 8, y + 8))

        # 事件
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                hit = False

                # 建造面板
                if show_tower_buy:
                    for idx, opt in enumerate(TOWER_SELECT_DATA):
                        row = idx // 2
                        col = idx % 2
                        ix = SCREEN_W // 2 - 50 + col * (TOWER_UI_ICON_SIZE + 10)
                        iy = GATE_Y - 80 + row * (TOWER_UI_ICON_SIZE + 10)
                        br = pygame.Rect(ix, iy, TOWER_UI_ICON_SIZE, TOWER_UI_ICON_SIZE)
                        if br.collidepoint(mx, my):
                            if player.gold >= opt["cost"]:
                                player.gold -= opt["cost"]
                                cx = CELL_START_X + selected_cell * int(CELL_RAW_W)
                                tx = cx + CELL_FINAL_W // 2
                                ty = GATE_Y + gate.h + CELL_H // 2
                                t = factory.create_tower(opt["type"], tx, ty, selected_cell)
                                t.total_cost = opt["cost"]
                                t.level = 1
                                towers.append(t)
                                cell_occupied[selected_cell] = True
                            else:
                                tip_text = "金币不足！"
                                tip_time = now + 1500
                            show_tower_buy = False
                            selected_cell = -1
                            hit = True
                            break
                    if not hit:
                        show_tower_buy = False
                        selected_cell = -1

                # 炮塔菜单
                elif show_tower_menu and selected_tower:
                    btn_w = TOWER_UI_BTN_SIZE
                    space = TOWER_UI_SPACING
                    total_w = btn_w * 3 + space * 2
                    sx = selected_tower.x - total_w // 2
                    sy = selected_tower.y - 80

                    r1 = pygame.Rect(sx, sy, btn_w, btn_w)
                    r2 = pygame.Rect(sx + btn_w + space, sy, btn_w, btn_w)
                    r3 = pygame.Rect(sx + (btn_w + space) * 2, sy, btn_w, btn_w)

                    if r1.collidepoint(mx, my):
                        cost = selected_tower.upgrade_cost()
                        if selected_tower.level < MAX_TOWER_LEVEL and player.gold >= cost:
                            player.gold -= cost
                            selected_tower.level += 1
                            selected_tower.upgrade_stat()
                        hit = True
                    elif r2.collidepoint(mx, my):
                        player.gold += int(selected_tower.total_cost * SELL_RETURN_RATIO)
                        cell_occupied[selected_tower.cell_idx] = False
                        towers.remove(selected_tower)
                        hit = True
                    elif r3.collidepoint(mx, my):
                        hit = True

                    show_tower_menu = False
                    selected_tower = None

                # 枪升级面板
                elif show_gun_menu:
                    cx = CELL_START_X + MIDDLE_CELL_INDEX * int(CELL_RAW_W)
                    cy = GATE_Y + gate.h + 10
                    btn_w = 80
                    spacing = 10
                    cost = gun.upgrade_cost()
                    can_up = gun.level < MAX_GUN_LEVEL and player.gold >= cost
                    is_critical = gun.level in GUN_CRITICAL_LEVELS

                    if is_critical:
                        r1 = pygame.Rect(cx - 90, cy - 120, btn_w, 40)
                        r2 = pygame.Rect(cx, cy - 120, btn_w, 40)
                        r3 = pygame.Rect(cx + 90, cy - 120, btn_w, 40)
                        if r1.collidepoint(mx, my) and can_up:
                            player.gold -= cost
                            gun.add_ballistic()
                            hit = True
                        elif r2.collidepoint(mx, my) and can_up:
                            player.gold -= cost
                            gun.add_burst()
                            hit = True
                        elif r3.collidepoint(mx, my):
                            hit = True
                    else:
                        r1 = pygame.Rect(cx - 45, cy - 120, btn_w, 40)
                        r2 = pygame.Rect(cx + 45, cy - 120, btn_w, 40)
                        if r1.collidepoint(mx, my) and can_up:
                            player.gold -= cost
                            gun.normal_upgrade()
                            hit = True
                        elif r2.collidepoint(mx, my):
                            hit = True
                    show_gun_menu = False

                # 普通点击
                else:
                    for i in range(CELL_TOTAL):
                        if cell_rects[i].collidepoint(mx, my):
                            if i == MIDDLE_CELL_INDEX:
                                show_gun_menu = True
                                hit = True
                            elif i in buildable_cells and not cell_occupied[i]:
                                show_tower_buy = True
                                selected_cell = i
                                hit = True
                            break
                    if not hit:
                        for t in towers:
                            if abs(mx - t.x) < 40 and abs(my - t.y) < 40:
                                selected_tower = t
                                show_tower_menu = True
                                hit = True
                                break

        # 绘制建造面板
        if show_tower_buy:
            pw = 110
            ph = 100
            px = SCREEN_W // 2 - pw // 2
            py = GATE_Y - 100
            pygame.draw.rect(screen, (50, 50, 50), (px, py, pw, ph))
            pygame.draw.rect(screen, COLOR_WHITE, (px, py, pw, ph), 2)
            for idx, opt in enumerate(TOWER_SELECT_DATA):
                row = idx // 2
                col = idx % 2
                ix = px + 10 + col * (TOWER_UI_ICON_SIZE + 10)
                iy = py + 10 + row * (TOWER_UI_ICON_SIZE + 10)
                pygame.draw.rect(screen, opt["color"], (ix, iy, TOWER_UI_ICON_SIZE, TOWER_UI_ICON_SIZE))
                screen.blit(get_font(12).render(str(opt["cost"]), True, COLOR_WHITE),
                            (ix + 5, iy + TOWER_UI_ICON_SIZE - 16))

        # 绘制炮塔3按钮菜单
        if show_tower_menu and selected_tower:
            btn_w = TOWER_UI_BTN_SIZE
            space = TOWER_UI_SPACING
            cost = selected_tower.upgrade_cost()
            can_up = selected_tower.level < MAX_TOWER_LEVEL and player.gold >= cost
            total_w = btn_w * 3 + space * 2
            sx = selected_tower.x - total_w // 2
            sy = selected_tower.y - 80

            r1 = (sx, sy, btn_w, btn_w)
            pygame.draw.rect(screen, (70, 70, 70), r1)
            if can_up:
                if btn_upgrade:
                    screen.blit(btn_upgrade, r1)
                else:
                    pygame.draw.rect(screen, COLOR_GREEN, (sx + 15, sy + 10, 10, 20))
            txt = f"{cost}" if selected_tower.level < MAX_TOWER_LEVEL else "MAX"
            screen.blit(get_font(12).render(txt, True, COLOR_WHITE if can_up else (160, 160, 160)),
                        (sx + 8, sy + btn_w - 16))

            r2 = (sx + btn_w + space, sy, btn_w, btn_w)
            pygame.draw.rect(screen, (70, 70, 70), r2)
            if btn_sell: screen.blit(btn_sell, r2)

            r3 = (sx + (btn_w + space) * 2, sy, btn_w, btn_w)
            pygame.draw.rect(screen, (70, 70, 70), r3)
            if btn_cancel: screen.blit(btn_cancel, r3)

        # 绘制枪升级面板
        if show_gun_menu:
            cx = CELL_START_X + MIDDLE_CELL_INDEX * int(CELL_RAW_W)
            cy = GATE_Y + gate.h + 10
            cost = gun.upgrade_cost()
            can_up = gun.level < MAX_GUN_LEVEL and player.gold >= cost
            is_critical = gun.level in GUN_CRITICAL_LEVELS
            font = get_font(14)

            if is_critical:
                r1 = pygame.Rect(cx - 90, cy - 120, 80, 40)
                r2 = pygame.Rect(cx, cy - 120, 80, 40)
                r3 = pygame.Rect(cx + 90, cy - 120, 80, 40)
                pygame.draw.rect(screen, (60, 60, 60), r1)
                pygame.draw.rect(screen, (60, 60, 60), r2)
                pygame.draw.rect(screen, (60, 60, 60), r3)
                screen.blit(font.render("弹道+1", True, COLOR_WHITE if can_up else (120, 120, 120)),
                            (r1.x + 15, r1.y + 10))
                screen.blit(font.render("连发+1", True, COLOR_WHITE if can_up else (120, 120, 120)),
                            (r2.x + 15, r2.y + 10))
                screen.blit(font.render("退出", True, COLOR_WHITE), (r3.x + 25, r3.y + 10))
            else:
                r1 = pygame.Rect(cx - 45, cy - 120, 80, 40)
                r2 = pygame.Rect(cx + 45, cy - 120, 80, 40)
                pygame.draw.rect(screen, (60, 60, 60), r1)
                pygame.draw.rect(screen, (60, 60, 60), r2)
                screen.blit(font.render(f"升级{cost}", True, COLOR_WHITE if can_up else (120, 120, 120)),
                            (r1.x + 10, r1.y + 10))
                screen.blit(font.render("退出", True, COLOR_WHITE), (r2.x + 25, r2.y + 10))

        # 玩家射击
        gun.shoot(player.x, player.y, monsters, GATE_Y)

        # 刷怪
        if now - spawn_timer > MONSTER_SPAWN_INTERVAL:
            spawn_timer = now
            monsters.append(factory.create_monster(wave))

        # 怪物逻辑
        for m in monsters[:]:
            m.update()
            rm = False
            if m.y + m.size > gate.y and m.y < gate.y + gate.h:
                gate.hp -= MONSTER_DAMAGE_TO_GATE
                damage_texts.append(DamageText(gate.x, gate.y - 20, MONSTER_DAMAGE_TO_GATE, "physical"))
                rm = True
            if m.hp <= 0 and not rm:
                player.gold += MONSTER_KILL_REWARD
                rm = True
            if rm and m in monsters:
                monsters.remove(m)

        # 炮塔射击
        for t in towers:
            t.shoot(monsters, GATE_Y)
            for b in t.bullets:
                b["rect"].x += b["dir"][0] * BULLET_SPEED_TOWER
                b["rect"].y += b["dir"][1] * BULLET_SPEED_TOWER

        # 玩家子弹移动
        for b in gun.bullets:
            b["rect"].x += b["dir"][0] * b["speed"]
            b["rect"].y += b["dir"][1] * b["speed"]

        # 子弹碰撞 + 抗性伤害计算
        all_bullets = gun.bullets + [b for t in towers for b in t.bullets]
        rem = []
        for b in all_bullets:
            if b["rect"].left < 0 or b["rect"].right > SCREEN_W or b["rect"].top < 0 or b["rect"].bottom > SCREEN_H:
                rem.append(b)
                continue
            for m in monsters:
                mr = pygame.Rect(m.x - m.size // 2, m.y - m.size // 2, m.size, m.size)
                if b["rect"].colliderect(mr):
                    dt = b["dmg_type"]
                    val = b["dmg"]
                    p = f = e = i = 0
                    if dt == "physical": p = val
                    if dt == "fire": f = val
                    if dt == "ice": i = val
                    if dt == "electric": e = val
                    real = (1 - m.phys_resist) * p + (1 - m.fire_resist) * f + (1 - m.ice_resist) * i + (
                                1 - m.elec_resist) * e
                    m.hp -= real
                    damage_texts.append(DamageText(m.x, m.y - 20, int(real), dt))
                    rem.append(b)
                    break

        # 清除子弹
        for b in rem:
            if b in gun.bullets: gun.bullets.remove(b)
            for t in towers:
                if b in t.bullets: t.bullets.remove(b)

        # 伤害数字
        for dt in damage_texts[:]:
            dt.update()
            dt.draw(screen)
            if dt.life <= 0: damage_texts.remove(dt)

        # 绘制场景
        gate.draw(screen)
        player.draw(screen)
        if gun.img: screen.blit(gun.img, (player.x - 15, player.y - 40))

        # 绘制炮塔
        for t in towers:
            t.draw(screen)
            screen.blit(get_font(18).render(str(t.level), True, COLOR_YELLOW), (t.x - 25, t.y - 25))
            cost = t.upgrade_cost()
            if t.level < MAX_TOWER_LEVEL and player.gold >= cost:
                screen.blit(get_font(20).render("↑", True, COLOR_GREEN), (t.x + 15, t.y - 25))

        # 怪物 & 子弹 + 怪物血条
        for m in monsters:
            m.draw(screen)
            bar_w = m.size
            bar_h = 4
            ratio = m.hp / m.max_hp
            pygame.draw.rect(screen, COLOR_RED, (m.x - bar_w // 2, m.y - m.size // 2 - 8, bar_w, bar_h))
            pygame.draw.rect(screen, COLOR_GREEN, (m.x - bar_w // 2, m.y - m.size // 2 - 8, bar_w * ratio, bar_h))

        for b in all_bullets:
            if bullet_img:
                screen.blit(bullet_img, b["rect"])
            else:
                pygame.draw.circle(screen, COLOR_YELLOW if b.get("laser") else COLOR_WHITE, b["rect"].center, 5)

        # 技能范围
        fire_skill.draw(screen, SCREEN_W // 2, SCREEN_H // 2)
        thunder_skill.draw(screen, SCREEN_W // 2, SCREEN_H // 2)
        ice_skill.draw(screen, SCREEN_W // 2, SCREEN_H // 2)

        # UI文字
        f = get_font(20)
        screen.blit(f.render(f"金币:{player.gold}", True, COLOR_WHITE), (10, 10))
        screen.blit(f.render(f"大门HP:{gate.hp}", True, COLOR_WHITE), (10, 30))
        screen.blit(f.render(f"波次:{wave}", True, COLOR_WHITE), (10, 50))
        screen.blit(f.render("左键：建造/升级/出售 空白关闭", True, COLOR_YELLOW), (10, 740))

        # 提示文本
        if now < tip_time:
            screen.blit(get_font(26).render(tip_text, True, COLOR_RED), (SCREEN_W // 2 - 70, SCREEN_H // 2))

        # 游戏结束
        if gate.hp <= 0:
            screen.blit(get_font(60).render("游戏结束", True, COLOR_RED), (SCREEN_W // 2 - 100, SCREEN_H // 2))

        pygame.display.flip()

    pygame.quit()

    print("\n----------------- end -----------------\n")
