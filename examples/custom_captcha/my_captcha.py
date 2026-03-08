#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    my_captcha_scene.py
Description:
    Manim custom captcha scene.
Author:
    Jose Miguel Rios Rubio
Date:
    01/03/2026
Version:
    1.0.0
"""

###############################################################################
# Libraries
###############################################################################

# Standard Libraries
import math
import pathlib
import secrets

# Third-Party Libraries
import manim


###############################################################################
# Scene
###############################################################################

class MyCaptcha(manim.Scene):
    '''
    Manim captcha scene.
    '''

    DIR_RESOURCES = pathlib.Path(__file__).parent / "resources"
    IMG_BACKGROUND = DIR_RESOURCES / "background.png"
    IMG_SELECTOR = DIR_RESOURCES / "clock_hand.svg"

    def __init__(self,
                 captcha_code: str | int | None = None,
                 properties: dict | None = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.captcha_code = captcha_code
        self.camera.background_color = manim.BLACK
        self.draw_color = manim.BLACK
        self.valid_captcha = self._is_valid_captcha_code(self.captcha_code)
        if self.valid_captcha:
            self.captcha_code = str(self.captcha_code)

    def construct(self):
        NUMBERS_SIZE = 0.8
        NUMBERS_RADIUS = 2.2
        if not self.valid_captcha:
            return
        # Random 0-9 Numbers
        num_map = {}
        orden = secrets.SystemRandom().sample(range(10), 10)
        nums = manim.Group()
        for n in orden:
            img_path = self.DIR_RESOURCES / f"{n}.png"
            t = manim.ImageMobject(str(img_path))
            t.center()
            t.scale_to_fit_height(NUMBERS_SIZE)
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
        # Draw background image (only supported with cairo renderer)
        bg = manim.ImageMobject(str(self.IMG_BACKGROUND))
        bg.scale_to_fit_height(self.camera.frame_height)
        bg.scale_to_fit_width(self.camera.frame_width)
        bg.move_to(manim.ORIGIN)
        self.add(bg)
        # Draw selector image
        # Note: SVG used to avoid flickering during rotation
        SELECTOR_ORIGIN = manim.ORIGIN + [0.00, -0.30, 0.00]
        SELECTOR_COLOR = manim.ManimColor("#2E2E2E")
        selector = manim.SVGMobject(str(self.IMG_SELECTOR))
        selector.scale_to_fit_width(self.camera.frame_height / 8)
        selector.set_fill(SELECTOR_COLOR, opacity=1)
        selector.set_stroke(SELECTOR_COLOR, width=0)
        selector.set_z_index(10)
        selector.move_to(SELECTOR_ORIGIN, aligned_edge=manim.DOWN)
        self.add(selector)
        pivot = selector.get_center() + \
            (manim.DOWN * (selector.height / 2)) + (manim.UP * 0.22)
        # Debug: Display Pivot Position
        # pivot_dot = manim.Dot(pivot, radius=0.08, color=manim.RED)
        # pivot_dot.set_z_index(100)
        # self.add(pivot_dot)
        # Display numbers with fade-in
        for num in nums:
            self.play(manim.FadeIn(num, scale=0.1), run_time=0.1)
        # Display Selector transition over numbers
        INITIAL_ANGLE = manim.PI / 2
        current_angle = INITIAL_ANGLE
        l_target_numbers = [int(d) for d in self.captcha_code]
        for target_num in l_target_numbers:
            target = num_map[target_num]
            vector = target.get_center() - pivot
            angle = math.atan2(vector[1], vector[0])
            delta = angle - current_angle
            self.play(
                manim.Rotate(selector, delta, about_point=pivot),
                run_time=1.0
            )
            current_angle = angle
            self.wait(0.5)
        delta = INITIAL_ANGLE - current_angle
        self.play(
                manim.Rotate(selector, delta, about_point=pivot),
                run_time=1.0
            )
        selector.move_to(SELECTOR_ORIGIN, aligned_edge=manim.DOWN)
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
