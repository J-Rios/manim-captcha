#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    manim_captcha_generator.py
Description:
    Manim captcha colors (wrapper to isolate and abstract Manim colors).
Author:
    Jose Miguel Rios Rubio
Date:
    27/02/2026
Version:
    1.1.0
"""

###############################################################################
# Libraries
###############################################################################

import manim


###############################################################################
# Captcha Colors
###############################################################################

class CaptchaColor:
    """Predefined Captcha colors."""
    WHITE = "#FFFFFF"
    GREY_A = "#DDDDDD"
    GREY_B = "#BBBBBB"
    GREY_C = "#888888"
    GREY_D = "#444444"
    GREY_E = "#222222"
    BLACK = "#000000"
    LIGHTER_GREY = "#DDDDDD"
    LIGHT_GREY = "#BBBBBB"
    GREY = "#888888"
    DARK_GREY = "#444444"
    DARKER_GREY = "#222222"
    BLUE_A = "#C7E9F1"
    BLUE_B = "#9CDCEB"
    BLUE_C = "#58C4DD"
    BLUE_D = "#29ABCA"
    BLUE_E = "#236B8E"
    PURE_BLUE = "#0000FF"
    BLUE = "#58C4DD"
    DARK_BLUE = "#236B8E"
    TEAL_A = "#ACEAD7"
    TEAL_B = "#76DDC0"
    TEAL_C = "#5CD0B3"
    TEAL_D = "#55C1A7"
    TEAL_E = "#49A88F"
    TEAL = "#5CD0B3"
    GREEN_A = "#C9E2AE"
    GREEN_B = "#A6CF8C"
    GREEN_C = "#83C167"
    GREEN_D = "#77B05D"
    GREEN_E = "#699C52"
    PURE_GREEN = "#00FF00"
    GREEN = "#83C167"
    YELLOW_A = "#FFF1B6"
    YELLOW_B = "#FFEA94"
    YELLOW_C = "#FFFF00"
    YELLOW_D = "#F4D345"
    YELLOW_E = "#E8C11C"
    YELLOW = "#FFFF00"
    GOLD_A = "#F7C797"
    GOLD_B = "#F9B775"
    GOLD_C = "#F0AC5F"
    GOLD_D = "#E1A158"
    GOLD_E = "#C78D46"
    GOLD = "#F0AC5F"
    RED_A = "#F7A1A3"
    RED_B = "#FF8080"
    RED_C = "#FC6255"
    RED_D = "#E65A4C"
    RED_E = "#CF5044"
    PURE_RED = "#FF0000"
    RED = "#FC6255"
    MAROON_A = "#ECABC1"
    MAROON_B = "#EC92AB"
    MAROON_C = "#C55F73"
    MAROON_D = "#A24D61"
    MAROON_E = "#94424F"
    MAROON = "#C55F73"
    PURPLE_A = "#CAA3E8"
    PURPLE_B = "#B189C6"
    PURPLE_C = "#9A72AC"
    PURPLE_D = "#715582"
    PURPLE_E = "#644172"
    PURPLE = "#9A72AC"
    PINK = "#D147BD"
    LIGHT_PINK = "#DC75CD"
    ORANGE = "#FF862F"
    LIGHT_BROWN = "#CD853F"
    DARK_BROWN = "#8B4513"
    GREY_BROWN = "#736357"

###############################################################################
