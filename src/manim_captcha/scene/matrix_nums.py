#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    circle_nums.py
Description:
    Manim captcha scene of numbers in a matrix distribution animation.
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

import random

from manim import *


###############################################################################
# Scene
###############################################################################

class MatrixNums(Scene):
    '''
    Manim captcha scene of numbers in a matrix distribution animation.
    '''

    def __init__(self,
                 captcha_code: int | None = None,
                 properties: dict | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.captcha_code = captcha_code
        self.bg_color = BLACK
        self.draw_color = WHITE
        self.selector_color = BLUE_D
        self.container_color = self.bg_color
        if properties:
            if "bg_color" in properties:
                self.bg_color = properties["bg_color"]
            if "draw_color" in properties:
                self.draw_color = properties["draw_color"]
            if "selector_color" in properties:
                self.selector_color = properties["selector_color"]
            if "container_color" in properties:
                self.container_color = properties["container_color"]

    def construct(self):
        SELECTOR_OPACITY = 0.5
        SELECTOR_SIZE = 1.2
        NUMBERS_SIZE = 84
        if self.captcha_code is None:
            return
        # Random 0-9 Numbers
        num_map = {}
        orden = random.sample(range(10), 10)
        nums = VGroup()
        for n in orden:
            t = Text(str(n), font_size=NUMBERS_SIZE, color=self.draw_color)
            nums.add(t)
            num_map[n] = t
        # Numbers distribution
        ROWS = 2
        COLS = 5
        SPACING_X = 2.5
        SPACING_Y = 2.5
        for i, num in enumerate(nums):
            row = i // COLS
            col = i % COLS
            x = (col - (COLS-1)/2) * SPACING_X
            y = ((ROWS-1)/2 - row) * SPACING_Y
            num.move_to(np.array([x, y, 0]))
        # Draw Container
        container = Rectangle(width=12,
                              height=5,
                              stroke_width=10,
                              color=self.draw_color,
                              fill_color=self.container_color,
                              fill_opacity=1.0)
        self.add(container)
        # Draw Selector
        selector = Square(side_length=SELECTOR_SIZE,
                          color=self.draw_color,
                          fill_color=self.selector_color,
                          fill_opacity=SELECTOR_OPACITY)
        self.add(selector)
        # Display numbers with fade-in
        for num in nums:
            self.play(FadeIn(num, scale=0.1), run_time=0.1)
        # Display Selector transition over numbers
        l_target_numbers = [int(d) for d in str(abs(self.captcha_code))]
        for target_num in l_target_numbers:
            # Go to target number
            target = num_map[target_num]
            self.play(
                selector.animate.move_to(target.get_center()),
                run_time=0.6,
                rate_func=smooth
            )
            self.wait(0.6)
        # Move Selector to original position
        self.play(
            selector.animate.move_to(ORIGIN),
            run_time=0.6,
            rate_func=smooth
        )
        self.wait(1)

###############################################################################
