#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    test_captcha_creation.py
Description:
    Manim Captcha creation tests.
Author:
    Jose Miguel Rios Rubio
Date:
    27/02/2026
Version:
    1.0.1
"""

###############################################################################
# Libraries
###############################################################################

# Standard Libraries
import shutil
from pathlib import Path
from traceback import format_exc

# Manim Library
from manim.constants import RendererType
from manim_captcha.generator import CaptchaGenerator
from manim_captcha.scenes import CaptchaScene
# from custom_captcha.test import TheScene as TestScene


###############################################################################
# Constants
###############################################################################

BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "../build/captchas"


###############################################################################
# Auxiliary Functions
###############################################################################

def rmdir(dir):
    try:
        shutil.rmtree(dir, ignore_errors=True)
    except Exception:
        print(format_exc())
        print("Fail to remove directory: %s", dir)


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
# Test Functions
###############################################################################

def test_captcha_creation_invalid_code():
    OUT_DIR = BUILD_DIR / "invalid"
    rmdir(OUT_DIR)
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
    rmdir(OUT_DIR)
    generator = CaptchaGenerator()
    # Default Generation
    for _ in range(NUM_CAPTCHAS_TO_GENERATE):
        captcha = generator.generate(out_dir=OUT_DIR)
        show_result(captcha)
        assert not captcha.error


def test_captcha_creation_short_long():
    OUT_DIR = BUILD_DIR / "short_long"
    rmdir(OUT_DIR)
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
    rmdir(OUT_DIR)
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
    rmdir(OUT_DIR)
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


def test_captcha_creation_builtin_themes():
    OUT_DIR = BUILD_DIR / "themes"
    rmdir(OUT_DIR)
    generator = CaptchaGenerator()
    # Captcha Generation - Default Theme
    properties = {"theme": "default"}
    captcha = generator.generate("1234", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Dark Theme
    properties = {"theme": "dark"}
    captcha = generator.generate("5678", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Light Theme
    properties = {"theme": "light"}
    captcha = generator.generate("9012", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error


def test_captcha_creation_custom_theme():
    THEME = {
        "bg_color": "#84D5E9",
        "draw_color": "#FDA552",
        "selector_color": "#FDC189",
        "container_color": "#FBFCC0"
    }
    OUT_DIR = BUILD_DIR / "theme_custom"
    rmdir(OUT_DIR)
    generator = CaptchaGenerator()
    properties = THEME
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


def test_captcha_creation_with_noise():
    OUT_DIR = BUILD_DIR / "noise"
    rmdir(OUT_DIR)
    generator = CaptchaGenerator()
    properties = {
        "theme": "random",
        "noise": True
    }
    # Captcha Generation - Circle Nums
    captcha = generator.generate("1234", scene=CaptchaScene.CIRCLE_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Matrix Nums
    captcha = generator.generate("2345", scene=CaptchaScene.MATRIX_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error
    # Captcha Generation - Piramid Nums
    captcha = generator.generate("3456", scene=CaptchaScene.PIRAMID_NUMS,
                                 properties=properties, out_dir=OUT_DIR)
    show_result(captcha)
    assert not captcha.error

###############################################################################
