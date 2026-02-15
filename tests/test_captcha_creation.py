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

from pathlib import Path
from manim.constants import RendererType
from manim_captcha.generator import CaptchaGenerator
from manim_captcha.scenes import CaptchaScene
from manim_captcha.colors import CaptchaColor, CaptchaColorCustom
# from custom_captcha.test import TheScene as TestScene


###############################################################################
# Constants
###############################################################################

BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "../build/captchas"

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

### Test Functions ###


def test_captcha_creation_invalid_code():
    OUT_DIR = BUILD_DIR / "invalid"
    generator = CaptchaGenerator()
    # Invalid Generation 1: Negative integer for circle nums captcha
    captcha = generator.generate(
        -123, scene=CaptchaScene.CIRCLE_NUMS,  # type: ignore[arg-type]
        out_dir=OUT_DIR)
    show_result(captcha)
    assert captcha.error
    # Invalid Generation 2: Negative number for circle nums captcha
    captcha = generator.generate("-123", scene=CaptchaScene.CIRCLE_NUMS,
                                 out_dir=OUT_DIR)
    show_result(captcha)
    assert captcha.error
    # Invalid Generation 3: Not number for circle nums captcha
    captcha = generator.generate("1AB2", scene=CaptchaScene.CIRCLE_NUMS,
                                 out_dir=OUT_DIR)
    show_result(captcha)
    assert captcha.error


def test_captcha_creation_default():
    OUT_DIR = BUILD_DIR / "default"
    NUM_CAPTCHAS_TO_GENERATE = 3
    generator = CaptchaGenerator()
    # Default Generation
    for _ in range(NUM_CAPTCHAS_TO_GENERATE):
        captcha = generator.generate(out_dir=OUT_DIR)
        show_result(captcha)
        assert not captcha.error


def test_captcha_creation_short_long():
    OUT_DIR = BUILD_DIR / "short_long"
    generator = CaptchaGenerator()
    # Cairo Renderer Generation
    captcha = generator.generate("5", out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # OpenGL Renderer Generation
    captcha = generator.generate("0123456789", out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error


def test_captcha_creation_render():
    OUT_DIR = BUILD_DIR / "render"
    generator = CaptchaGenerator()
    # Cairo Renderer Generation
    captcha = generator.generate("1234", scene=CaptchaScene.CIRCLE_NUMS,
                                 renderer=RendererType.CAIRO, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # OpenGL Renderer Generation
    captcha = generator.generate("5678", scene=CaptchaScene.CIRCLE_NUMS,
                                 renderer=RendererType.OPENGL, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error


def test_captcha_creation_builtin_scenes():
    OUT_DIR = BUILD_DIR / "builtin_scenes"
    generator = CaptchaGenerator()
    # Captcha Generation - Circle Nums
    captcha = generator.generate("0123", scene=CaptchaScene.CIRCLE_NUMS,
                                 out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Matrix Nums
    captcha = generator.generate("5678", scene=CaptchaScene.MATRIX_NUMS,
                                 out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Piramid Nums
    captcha = generator.generate("9012", scene=CaptchaScene.PIRAMID_NUMS,
                                 out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error


def test_captcha_creation_theme_dark():
    theme_dark = {
        "bg_color": CaptchaColorCustom("#0E1621"),
        "draw_color": CaptchaColor.WHITE,
        "selector_color": CaptchaColor.BLUE_D,
        "container_color": CaptchaColorCustom("#1F1F1F")
    }
    OUT_DIR = BUILD_DIR / "theme_dark"
    generator = CaptchaGenerator()
    properties = theme_dark
    # Captcha Generation - Circle Nums
    captcha = generator.generate("1234", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Matrix Nums
    captcha = generator.generate("5678", scene=CaptchaScene.MATRIX_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Piramid Nums
    captcha = generator.generate("9012", scene=CaptchaScene.PIRAMID_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error


def test_captcha_creation_theme_light():
    theme_light = {
        "bg_color": CaptchaColorCustom("#6FA788"),
        "draw_color": CaptchaColor.BLACK,
        "selector_color": CaptchaColor.RED_D,
        "container_color": CaptchaColor.WHITE,
    }
    OUT_DIR = BUILD_DIR / "theme_light"
    generator = CaptchaGenerator()
    properties = theme_light
    # Captcha Generation - Circle Nums
    captcha = generator.generate("1234", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Matrix Nums
    captcha = generator.generate("5678", scene=CaptchaScene.MATRIX_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Piramid Nums
    captcha = generator.generate("9012", scene=CaptchaScene.PIRAMID_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error

###############################################################################
