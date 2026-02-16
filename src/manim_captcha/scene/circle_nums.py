#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    circle_nums.py
Description:
    Manim captcha scene of numbers in a circular distribution animation.
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
import math
import random
import secrets

# Third-Party Libraries
import manim


###############################################################################
# Scene
###############################################################################

class CircleNums(manim.Scene):
    '''
    Manim captcha scene of numbers in a circular distribution animation.
    '''

    theme_default = {
        "bg_color": manim.BLACK,
        "draw_color": manim.WHITE,
        "selector_color": manim.BLUE_D,
        "container_color": manim.BLACK,
    }

    theme_dark = {
        "bg_color": manim.ManimColor("#0E1621"),
        "draw_color": manim.WHITE,
        "selector_color": manim.BLUE_D,
        "container_color": manim.ManimColor("#1F1F1F")
    }

    theme_light = {
        "bg_color": manim.ManimColor("#6FA788"),
        "draw_color": manim.BLACK,
        "selector_color": manim.RED_D,
        "container_color": manim.WHITE,
    }

    def __init__(self,
                 captcha_code: str | int | None = None,
                 properties: dict | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.captcha_code = captcha_code
        self.noise = False
        self._apply_theme(self.theme_default)
        # Configure properties
        if properties:
            if "noise" in properties:
                self.noise = properties["noise"]
            if "theme" in properties:
                if properties["theme"] == "dark":
                    self._apply_theme(self.theme_dark)
                elif properties["theme"] == "light":
                    self._apply_theme(self.theme_light)
            if "bg_color" in properties:
                self.bg_color = properties["bg_color"]
            if "draw_color" in properties:
                self.draw_color = properties["draw_color"]
            if "selector_color" in properties:
                self.selector_color = properties["selector_color"]
            if "container_color" in properties:
                self.container_color = properties["container_color"]
        # Apply background color
        self.camera.background_color = self.bg_color

    def construct(self):
        SELECTOR_OPACITY = 0.5
        CONTAINER_RADIUS = 3.6
        SELECTOR_RADIUS = 0.6
        NUMBERS_SIZE = 84
        NUMBERS_RADIUS = 2.6
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
        for i, num in enumerate(nums):
            angle = 2 * math.pi * i / len(nums)
            pos = NUMBERS_RADIUS * manim.np.array([
                math.cos(angle),
                math.sin(angle),
                0
            ])
            num.move_to(pos)
        # Draw Container
        container = manim.Circle(radius=CONTAINER_RADIUS,
                                 stroke_width=10,
                                 color=self.draw_color,
                                 fill_color=self.container_color,
                                 fill_opacity=1.0)
        self.add(container)
        # Display noise
        if self.noise:
            self._add_noise(num_lines=25, num_dots=35, width=8, height=6)
        # Draw Selector
        selector = manim.Circle(radius=SELECTOR_RADIUS,
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
            self.wait(0.2)
            # Move Selector to original position
            self.play(
                selector.animate.move_to(manim.ORIGIN),
                run_time=0.6,
                rate_func=manim.smooth
            )
        self.wait(1)

    def _add_noise(self, num_lines=20, num_dots=30, width=8, height=6):
        '''Add noise particles free moving around the image.'''
        DOTS_RADIUS_MIN_MAX = (0.04, 0.08)
        LINES_STROKE_WIDTH_MIN_MAX = (3, 8)
        noise_group = manim.VGroup()
        # Slim Lines
        for _ in range(num_lines):
            start = manim.np.array([
                random.uniform(-width/2, width/2),
                random.uniform(-height/2, height/2),
                0
            ])
            end = start + manim.np.array([
                random.uniform(-0.5, 0.5),
                random.uniform(-0.5, 0.5),
                0
            ])
            stroke_width = random.uniform(
                LINES_STROKE_WIDTH_MIN_MAX[0], LINES_STROKE_WIDTH_MIN_MAX[1])
            line = manim.Line(
                start, end, stroke_width=stroke_width, color=self.draw_color)
            line._velocity = manim.np.array([
                random.uniform(-0.02, 0.02),
                random.uniform(-0.02, 0.02),
                0
            ])
            noise_group.add(line)
        # Small Dots
        for _ in range(num_dots):
            pos = manim.np.array([
                random.uniform(-width/2, width/2),
                random.uniform(-height/2, height/2),
                0
            ])
            radius = random.uniform(
                DOTS_RADIUS_MIN_MAX[0], DOTS_RADIUS_MIN_MAX[1])
            dot = manim.Dot(point=pos, radius=radius, color=self.draw_color)
            dot._velocity = manim.np.array([
                random.uniform(-0.03, 0.03),
                random.uniform(-0.03, 0.03),
                0
            ])
            noise_group.add(dot)
        self.add(noise_group)
        # Noise movement animation updater
        def move_noise_smooth(mob, dt):
            for obj in mob:
                # Move and reflect at borders
                obj.shift(obj._velocity)
                x, y, _ = obj.get_center()
                if x < -width/2 or x > width/2:
                    obj._velocity[0] *= -1
                if y < -height/2 or y > height/2:
                    obj._velocity[1] *= -1
        noise_group.add_updater(move_noise_smooth)

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

    def _apply_theme(self, theme):
        self.bg_color = theme["bg_color"]
        self.draw_color = theme["draw_color"]
        self.selector_color = theme["selector_color"]
        self.container_color = theme["container_color"]

###############################################################################
