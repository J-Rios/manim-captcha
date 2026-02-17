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
import secrets
import shutil

from pathlib import Path
from traceback import format_exc


###############################################################################
# Third-Party Libraries
###############################################################################

import manim

from manim.constants import RendererType

###############################################################################
# Local Libraries
###############################################################################

from .colors import CaptchaColor
from .data import CaptchaData
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

    # None

    ###########################################################################

    ### Constructor ###

    def __init__(self):
        self.available: bool = self._is_manim_available()
        if self.available:
            logging.getLogger("manim").setLevel(logging.ERROR)

    ###########################################################################

    ### Public Methods ###

    def is_available(self):
        '''Get Generator availability.'''
        return self.available

    def generate(self,
                 code: str | None = None,
                 scene: type[manim.Scene] | None = None,
                 out_dir: Path | None = None,
                 tmp_dir: Path | None = None,
                 width: int = 854,
                 height: int = 480,
                 fps: int = 30,
                 format: str = "mp4",
                 renderer: RendererType = RendererType.CAIRO,
                 properties: dict | None = None) -> CaptchaData:
        """
        Generate a captcha for the provided code.
        Arguments:
        - scene: Manim captcha scene to use.
        - code: Captcha code to generate (string).
        - out_dir: Output directory to put the generated captcha file.
        - tmp_dir: Temporary directory for captcha build.
        - width: Output captcha resolution width.
        - height: Output captcha resolution height.
        - fps: Output captcha video framerate.
        - properties: Captcha properties (i.e. colors).
        - format: Captcha output format (mp4/gif).
        - rendered: Video renderer to use (cairo/opengl).
        """
        captcha_result = CaptchaData()
        # Do nothing if Manim is not available
        if not self.available:
            captcha_result.error = True
            captcha_result.error_info = "Manim not found in the system"
            return captcha_result
        # Use a random captcha code number if was not provided
        if code is None:
            code = self._generate_random_code()
        # Use a random captcha scene if was not provided
        if scene is None:
            scene = CaptchaScene.get_random_scene()
        # Set output captcha file (use current path if was not provided)
        if out_dir is None:
            out_dir = Path(".")
        out_file = out_dir / f"{code}.{format}"
        # Use current path for temporary directory if was not provided
        if tmp_dir is None:
            tmp_dir = out_dir / "tmp"
        # Set background color
        bg_color = CaptchaColor.BLACK
        if properties:
            bg_color = properties.get("bg_color", manim.BLACK)
        # Create output directory if it doesn't exists
        out_dir.mkdir(parents=True, exist_ok=True)
        # Run Manim to generate the captcha
        self._run_manim(code, scene, tmp_dir, width, height, fps, format,
                        renderer, bg_color, properties)
        generated_file = self._find_file(tmp_dir, format)
        if generated_file:
            self._move_file(generated_file, out_file)
            captcha_result.code = code
            captcha_result.file = out_file
            logger.info("Generated captcha: %s", out_file)
        else:
            captcha_result.error = True
            captcha_result.error_info = "Captcha creation fail"
        self._rmdir(tmp_dir)
        return captcha_result

    ###########################################################################

    ### Private Methods ###

    def _run_manim(self, code: str, scene, media_dir: Path,
                   width: int, height: int, fps: int, format: str,
                   renderer: RendererType, bg_color: manim.ManimColor,
                   properties: dict | None):
        config = {
            "renderer": renderer,
            "format": format,
            "pixel_width": width,
            "pixel_height": height,
            "frame_rate": fps,
            "background_color": bg_color,
            "media_dir": str(media_dir),
            "progress_bar": "none",
            "preview": False
        }
        with manim._config.tempconfig(config):
            scene(code, properties).render()

    def _generate_random_code(self, digits: int = 4) -> str:
        return "".join(secrets.choice("0123456789") for _ in range(digits))

    def _find_file(self, directory, file_extension) -> Path | None:
        gen_files = list(directory.rglob(f"*.{file_extension}"))
        if not gen_files:
            return None
        # Last generated
        return max(gen_files, key=lambda p: p.stat().st_mtime)

    def _rmdir(self, dir):
        try:
            shutil.rmtree(dir, ignore_errors=True)
        except Exception:
            logger.error(format_exc())
            logger.error("Fail to remove directory: %s", dir)

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
