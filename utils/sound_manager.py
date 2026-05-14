# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 16:37
# @Author   : GuanXK
# @File     : sound_manager.py

"""
info:

"""

# system

# third_party

# custom
import pygame
import os

pygame.mixer.init()
pygame.mixer.set_num_channels(16)

SUPPORT_EXTS = [".wav", ".mp3"]


def load_sound(path_no_ext):
    for ext in SUPPORT_EXTS:
        full = path_no_ext + ext
        if os.path.exists(full):
            try:
                return pygame.mixer.Sound(full)
            except:
                pass
    return None


# 音效
bullet_hit_snd = load_sound("sounds/bullet_hit")
fire_hit_snd = load_sound("sounds/fire_hit")
thunder_hit_snd = load_sound("sounds/thunder_hit")
ice_hit_snd = load_sound("sounds/ice_hit")  # 冰系
gate_hit_snd = load_sound("sounds/gate_hit")
shoot_snd = load_sound("sounds/shoot")  # 开枪音效


# 背景音乐
def play_bgm():
    bgm_path = None
    for ext in SUPPORT_EXTS:
        p = "sounds/bgm" + ext
        if os.path.exists(p):
            bgm_path = p
            break
    if bgm_path:
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # 无限循环


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
