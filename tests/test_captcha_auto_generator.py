#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    test_captcha_auto_generator.py
Description:
    Manim Captcha Automatic Generator tests.
Author:
    Jose Miguel Rios Rubio
Date:
    16/02/2026
Version:
    1.0.0
"""

###############################################################################
# Libraries
###############################################################################

# Standard Libraries
import asyncio
import shutil
from pathlib import Path
from traceback import format_exc

# Manim Library
from manim_captcha.auto_generator import CaptchaAutoGenerator


###############################################################################
# Constants
###############################################################################

BASE_DIR = Path(__file__).resolve().parent
BUILD_DIR = BASE_DIR / "../build/captchas/auto_generation"


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
        print("Fail to get captcha:")
        print(captcha.error_info)
        return
    print("")
    print("Captcha successfully obtained")
    print(f"  Code: \"{captcha.code}\"")
    print(f"  File: {captcha.file}")
    print("")


###############################################################################
# Test Functions
###############################################################################

async def test_captcha_auto_generator():
    MAX_NUM_CAPTCHAS = 3
    TIME_GEN_INTERVAL_S = 10
    TIME_CAPTCHA_GEN_S = 10
    auto_generator = CaptchaAutoGenerator(
        BUILD_DIR, TIME_GEN_INTERVAL_S, MAX_NUM_CAPTCHAS)
    # Test get captcha returns error when no captchas are availables
    rmdir(BUILD_DIR)
    captcha = auto_generator.get_captcha()
    show_result(captcha)
    assert captcha.error
    # Test Start of captcha automatic generator doesn't fail
    result = await auto_generator.start()
    assert result
    # Test number of generated captchas is 0 right after start
    num_captchas = auto_generator.num_captchas()
    assert num_captchas == 0
    # Test getting a captcha after wait for first generation interval
    await asyncio.sleep(TIME_CAPTCHA_GEN_S)
    num_captchas = auto_generator.num_captchas()
    assert num_captchas == 1
    captcha = auto_generator.get_captcha()
    show_result(captcha)
    assert not captcha.error
    # Test getting a captcha after wait for second generation interval
    await asyncio.sleep(TIME_CAPTCHA_GEN_S)
    num_captchas = auto_generator.num_captchas()
    assert num_captchas == 2
    captcha = auto_generator.get_captcha()
    show_result(captcha)
    assert not captcha.error
    # Test getting a captcha after wait for third generation interval
    await asyncio.sleep(TIME_CAPTCHA_GEN_S)
    num_captchas = auto_generator.num_captchas()
    assert num_captchas == 3
    captcha = auto_generator.get_captcha()
    show_result(captcha)
    # Test number of captchas after some asyncio is the configured limit
    await asyncio.sleep(3 * TIME_CAPTCHA_GEN_S)
    num_captchas = auto_generator.num_captchas()
    assert num_captchas == MAX_NUM_CAPTCHAS
    captcha = auto_generator.get_captcha()
    show_result(captcha)
    # Test Generator stop
    running = auto_generator.is_running()
    assert running
    await auto_generator.stop()
    running = auto_generator.is_running()
    assert not running

###############################################################################
