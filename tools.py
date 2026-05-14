# _*_ coding: utf-8 _*_
# @Time     : 2026/5/14 13:55
# @Author   : GuanXK
# @File     : utils.py

"""
info:

"""

# system

# third_party

# custom

import pygame
import os


# 加载UI图片
def load_image(path_no_ext, size=None):
    """
    尝试加载 .png .bmp .jpg .jpeg
    path_no_ext: 不带后缀的路径，如 "assets/player"
    size: (w,h) 缩放
    """
    exts = [".png", ".bmp", ".jpg", ".jpeg"]
    img = None
    for ext in exts:
        full_path = path_no_ext + ext
        if os.path.exists(full_path):
            img = pygame.image.load(full_path).convert_alpha()
            break
    if img and size:
        img = pygame.transform.scale(img, size)
    return img


# 支持中文
def get_font(size):
    # 优先使用自定义中文字体
    if os.path.exists("fonts/msyh.ttf"):
        return pygame.font.Font("fonts/msyh.ttf", size)
    # 没有字体就用系统默认（不保证中文）
    return pygame.font.SysFont(None, size)


if __name__ == "__main__":
    print("\n---------------- start ----------------\n")

    print("\n----------------- end -----------------\n")
