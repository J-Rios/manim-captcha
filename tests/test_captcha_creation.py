#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    test_captcha_creation.py
Description:
    Manim Captcha creation tests.
Author:
    Jose Miguel Rios Rubio
Creation date:
    14/02/2026
Last modified date:
    14/02/2026
Version:
    1.0.0
"""

###############################################################################
# Libraries
###############################################################################

import pytest

from pathlib import Path
from manim_captcha.generator import CaptchaGenerator
from manim_captcha.colors import CaptchaColor, CaptchaColorCustom
# from custom_captcha.test import TheScene as TestScene


###############################################################################
# Constants
###############################################################################

BASE_DIR = Path(__file__).resolve().parent
OUT_DIR = BASE_DIR / "../build/captchas"

theme_dark = {
    "bg_color": CaptchaColorCustom("#0E1621"),
    "draw_color": CaptchaColor.WHITE,
    "selector_color": CaptchaColor.BLUE_D,
    "container_color": CaptchaColorCustom("#17212B")
}

theme_light = {
    "bg_color": CaptchaColorCustom("#6FA788"),
    "draw_color": CaptchaColor.BLACK,
    "selector_color": CaptchaColor.RED_D,
    "container_color": CaptchaColor.WHITE,
}

###############################################################################

### Auxiliary FUnctions ###

def show_result(captcha):
    if captcha.error:
        print(captcha.error_info)
        print("Fail to create the captcha")
        return
    print("")
    print("Captcha successfully created")
    print(f"  Code: \"{captcha.code}\"")
    print(f"  File: {captcha.file}")
    print("")

###############################################################################

### Test Function ###

def test_captcha_creation():
    generator = CaptchaGenerator()
    # Default Generation
    captcha = generator.generate(1234, out_dir=OUT_DIR)
    show_result(captcha)
    # OpenGL Renderer Generation
    captcha = generator.generate(1235, renderer="opengl", out_dir=OUT_DIR)
    show_result(captcha)
    # Custom Properties
    captcha = generator.generate(1236, properties=theme_dark, out_dir=OUT_DIR)
    show_result(captcha)
    assert True

###############################################################################
