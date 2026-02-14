#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    scene.py
Description:
    Manim builtin captcha scenes.
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

# Standard Libraries
import random

# Third-Party Libraries
import manim

# Captcha Builtin Scenes
from .scene.circle_nums import CircleNums
# ...


###############################################################################
# Captcha Builtin Scenes
###############################################################################

class CaptchaScene:
    '''Captcha builtin scenes.'''

    CIRCLE_NUMS = CircleNums
    # ...

    def get_random_scene(self):
        scenes = [
            v for v in vars(CaptchaScene).values()
            if isinstance(v, type) and issubclass(v, manim.Scene)
        ]
        return random.choice(scenes)

###############################################################################
