#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    manim_captcha_generator.py
Description:
    Manim video Captcha generator.
    This component allows you to generate a captcha video file using
    Manim library according to the specified parameters.
    The captcha scene to be used in the captcha can be provided as
    custom scene or define from some builtint predefined scenes.
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
# Standard Libraries
###############################################################################

import logging
import random
import shutil

from pathlib import Path
from traceback import format_exc


###############################################################################
# Third-Party Libraries
###############################################################################

import manim


###############################################################################
# Local Libraries
###############################################################################

from .colors import CaptchaColor
from .scenes import CaptchaScene

###############################################################################
# Logger Setup
###############################################################################

logger = logging.getLogger(__name__)


###############################################################################
# Class ManimCaptchaGenerator
###############################################################################

class CaptchaGenerator:
    """Manim captcha Generator."""

    ###########################################################################

    ### Constants ###

    # None

    ###########################################################################

    ### Data Types ###

    class CaptchaData:
        """Captcha information."""

        def __init__(self):
            self.code: str = ""
            self.file: Path = None
            self.error: bool = False
            self.error_info: str = ""

    ###########################################################################

    ### Constructor ###

    def __init__(self):
        self.scene: manim.Scene | None = None
        self.code: str = None
        self.width: int = 854
        self.height: int = 480
        self.fps: int = 30
        self.bg_color = CaptchaColor.BLACK
        self.properties: dict | None = None
        self.format: str = "mp4"
        self.renderer: str = "cairo"
        self.out_dir: Path = Path(".")
        self.tmp_dir: Path = self.out_dir / "tmp"
        self.available: bool = self._is_manim_available()

    ###########################################################################

    ### Public Methods ###

    def generate(self,
                 code: str | None = None,
                 scene: manim.Scene | None = None,
                 out_dir: Path | None = None,
                 tmp_dir: Path | None = None,
                 width: int = 854,
                 height: int = 480,
                 fps: int = 30,
                 properties: dict | None = None,
                 format: str = "mp4",
                 renderer: str = "cairo") -> CaptchaData:
        """
        Generate a captcha for the provided code.
        Arguments:
        - scene: Manim captcha scene to use.
        - code: Captcha code to generate.
        - out_dir: Output directory to put the generated captcha file.
        - tmp_dir: Temporary directory for captcha build.
        - width: Output captcha resolution width.
        - height: Output captcha resolution height.
        - fps: Output captcha video framerate.
        - properties: Captcha properties (i.e. colors).
        - format: Captcha output format (mp4/gif).
        - rendered: Video renderer to use (cairo/opengl).
        """
        captcha_result = self.CaptchaData()
        # Set properties to use from provided arguments
        self.scene = scene
        self.code = code
        self.out_dir = out_dir
        self.tmp_dir = tmp_dir
        self.width = width
        self.height = height
        self.fps = fps
        self.properties = properties
        self.format = format
        self.renderer = renderer
        if self.properties:
            self.bg_color = self.properties.get("bg_color", manim.BLACK)
        # Do nothing if Manim is not available
        if not self.available:
            captcha_result.error = True
            captcha_result.error_info = "Manim not found in the system"
            return captcha_result
        # Use a random captcha scene if was not provided
        if self.scene is None:
            self.scene = CaptchaScene.get_random_scene()
        # Use a random captcha code number if was not provided
        if self.code is None:
            self.code = self._generate_random_code()
        # Set output captcha file (use current path if was not provided)
        if self.out_dir is None:
            self.out_dir = Path(".")
        out_file = self.out_dir / f"{self.code}.{self.format}"
        # Use current path for temporary directory if was not provided
        if tmp_dir is None:
            tmp_dir = self.out_dir / "tmp"
        self.tmp_dir = tmp_dir
        # Create output directory if it doesn't exists
        self.out_dir.mkdir(parents=True, exist_ok=True)
        # Run Manim to generate the captcha
        self._run_manim()
        generated_file = self._find_generated_file()
        if generated_file:
            self._move_file(generated_file, out_file)
            captcha_result.code = self.code
            captcha_result.file = out_file
            logger.info("Captcha generated at: %s", out_file)
        else:
            captcha_result.error = True
            captcha_result.error_info = "Captcha creation fail"
        self._cleanup()
        return captcha_result

    ###########################################################################

    ### Private Methods ###

    def _run_manim(self):
        config = {
            "renderer": self.renderer,
            "format": self.format,
            "pixel_width": self.width,
            "pixel_height": self.height,
            "frame_rate": self.fps,
            "background_color": self.bg_color,
            "media_dir": str(self.tmp_dir),
            "preview": False
        }
        with manim._config.tempconfig(config):
            self.scene(self.code, self.properties).render()

    def _generate_random_code(self, digits: int = 4) -> str:
        return "".join(random.choices("0123456789", k=digits))

    def _find_generated_file(self) -> Path:
        gen_files = list(self.tmp_dir.rglob(f"*.{self.format}"))
        if not gen_files:
            return None
        # Last generated
        return max(gen_files, key=lambda p: p.stat().st_mtime)

    def _cleanup(self):
        try:
            shutil.rmtree(self.tmp_dir, ignore_errors=True)
        except Exception:
            logger.error(format_exc())
            logger.error("Fail to remove directory: %s", self.tmp_dir)

    def _move_file(self, file, target_dir):
        try:
            shutil.move(file, target_dir)
        except Exception:
            logger.error(format_exc())
            logger.error("Fail to move file to directory: %s -> %s",
                         file, target_dir)

    def _is_manim_available(self) -> bool:
        manim_bin = shutil.which("manim")
        if not manim_bin:
            return False
        return True

###############################################################################
