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

# Standard Libraries
import secrets

# Third-Party Libraries
import manim


###############################################################################
# Scene
###############################################################################

class MatrixNums(manim.Scene):
    '''
    Manim captcha scene of numbers in a matrix distribution animation.
    '''

    def __init__(self,
                 captcha_code: str | int | None = None,
                 properties: dict | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.captcha_code = captcha_code
        self.bg_color = manim.BLACK
        self.draw_color = manim.WHITE
        self.selector_color = manim.BLUE_D
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
        # Ensure the code is an unsigned number (int or str)
        if not self._is_valid_captcha_code(self.captcha_code):
            return
        self.captcha_code = str(self.captcha_code)
        # Random 0-9 Numbers
        num_map = {}
        orden = secrets.SystemRandom().sample(range(10), 10)
        nums = manim.VGroup()
        for n in orden:
            t = manim.Text(str(n), font_size=NUMBERS_SIZE,
                           color=self.draw_color)
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
            num.move_to(manim.np.array([x, y, 0]))
        # Draw Container
        container = manim.Rectangle(width=12,
                                    height=5,
                                    stroke_width=10,
                                    color=self.draw_color,
                                    fill_color=self.container_color,
                                    fill_opacity=1.0)
        self.add(container)
        # Draw Selector
        selector = manim.Square(side_length=SELECTOR_SIZE,
                                color=self.draw_color,
                                fill_color=self.selector_color,
                                fill_opacity=SELECTOR_OPACITY)
        self.add(selector)
        # Display numbers with fade-in
        for num in nums:
            self.play(manim.FadeIn(num, scale=0.1), run_time=0.1)
        # Display Selector transition over numbers
        l_target_numbers = [int(d) for d in self.captcha_code]
        for target_num in l_target_numbers:
            # Go to target number
            target = num_map[target_num]
            self.play(
                selector.animate.move_to(target.get_center()),
                run_time=0.6,
                rate_func=manim.smooth
            )
            self.wait(0.6)
        # Move Selector to original position
        self.play(
            selector.animate.move_to(manim.ORIGIN),
            run_time=0.6,
            rate_func=manim.smooth
        )
        self.wait(1)

    def _is_valid_captcha_code(self, captcha_code: str | int | None):
        valid = False
        if captcha_code:
            try:
                int_captcha_code = int(captcha_code)
                if int_captcha_code >= 0:
                    valid = True
            except ValueError:
                valid = False
        return valid

###############################################################################
