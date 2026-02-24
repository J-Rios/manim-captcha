#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    auto_generator.py
Description:
    Automatic captcha generation manager.
    This component act as a producer that periodically creates and store
    random Manim Captchas into a directory of the filesystem, allowing
    external consumers (users of the library) to request any of these
    captchas. It keeps control of the number of generated captchas, and
    apply some kind of "files rotation" of the storage, removing and
    replacing older captchas with newer ones to control and limit the
    maximum number of captchas in the filesytem.
Author:
    Jose Miguel Rios Rubio
Creation date:
    15/02/2026
Last modified date:
    16/02/2026
Version:
    1.0.0
"""

###############################################################################
# Standard Libraries
###############################################################################

import asyncio
import logging
import secrets

from pathlib import Path
from traceback import format_exc


###############################################################################
# Third-Party Libraries
###############################################################################

from manim import Scene
from manim.constants import RendererType


###############################################################################
# Local Libraries
###############################################################################

from .data import CaptchaData
from .generator import CaptchaGenerator


###############################################################################
# Logger Setup
###############################################################################

logger = logging.getLogger(__name__)


###############################################################################
# Class ManimCaptchaGenerator
###############################################################################

class CaptchaAutoGenerator:
    """Automatic captcha generation manager."""

    ###########################################################################

    ### Constants ###

    # None

    ###########################################################################

    ### Data Types ###

    # None

    ###########################################################################

    ### Constructor ###

    def __init__(self,
                 out_dir: Path = Path("./captchas"),
                 interval_s: int = 60,
                 max_items: int = 100):
        '''
        Automatic captcha generation manager construction.
        Arguments:
        - out_dir: Output directory to place the generated captchas.
        - interval: Time for creation of each new Captcha (in seconds).
        - max_items: Maximum number of Captchas allowed in the
        filesystem (once this number of captchas are generated, the file
        rotate mechanism will be replacing older captchas with newer
        ones).
        '''
        self.list_captcha_files: list = list()
        self.list_scenes: list = list()
        self.out_dir = out_dir
        self.interval_s = interval_s
        self.max_items = max_items
        self.format: str = "mp4"
        self._task_create: asyncio.Task | None = None
        self._task_remove: asyncio.Task | None = None
        self._running: bool = False
        self._lock = asyncio.Lock()
        self._generator = CaptchaGenerator()
        self.available: bool = self._generator.is_available()

    ###########################################################################

    ### Public Methods ###

    def add_captcha_scene(self,
                          scene: type[Scene],
                          properties: dict | None = None,
                          width: int = 854,
                          height: int = 480,
                          fps: int = 30,
                          format: str = "mp4",
                          renderer: RendererType = RendererType.CAIRO):
        '''Add a scene to the list of captchas to be generated.'''
        captcha_cfg = {
            "scene": scene,
            "width": width,
            "height": height,
            "fps": fps,
            "format": format,
            "renderer": renderer,
            "properties": properties
        }
        if captcha_cfg not in self.list_scenes:
            self.list_scenes.append(captcha_cfg)

    async def start(self) -> bool:
        '''Launch the manager to start creating captchas.'''
        # Check if the generator can be started
        if not self.available:
            return False
        if self._running:
            return False
        # Get list of captcha files already in the output directory
        list_files = list(self.out_dir.glob(f"*.{self.format}"))
        self.list_captcha_files = sorted(
            list_files, key=lambda f: f.stat().st_mtime)
        # Start Producer and Remover tasks
        self._running = True
        self._task_create = asyncio.create_task(self._producer_loop())
        self._task_remove = asyncio.create_task(self._remove_loop())
        return True

    async def stop(self):
        '''Stop the manager and the captcha creation.'''
        if self._task_create:
            self._task_create.cancel()
            try:
                await self._task_create
            except asyncio.CancelledError:
                pass
            self._task_create = None
        if self._task_remove:
            self._task_remove.cancel()
            try:
                await self._task_remove
            except asyncio.CancelledError:
                pass
            self._task_remove = None
        self._running = False

    def is_running(self) -> bool:
        '''Get Captcha Generator manager running status.'''
        return self._running

    def num_captchas(self) -> int:
        '''
        Get the number of generated captcha files availables in the
        file system.
        '''
        return len(self.list_captcha_files)

    def get_captcha(self) -> CaptchaData:
        '''Return a random captcha file from storage.'''
        captcha_result = CaptchaData()
        if not self.available:
            captcha_result.error = True
            captcha_result.error_info = "Manim not found in the system"
            return captcha_result
        try:
            if not self.list_captcha_files:
                captcha_result.error = True
                captcha_result.error_info = "None captcha files generated"
                return captcha_result
            captcha_result.file = secrets.choice(self.list_captcha_files)
            captcha_result.code = captcha_result.file.stem
        except Exception:
            logger.error(format_exc())
            captcha_result.error = True
            captcha_result.error_info = "Fail to get captcha from filesystem"
        return captcha_result

    ###########################################################################

    ### Private Methods - Create Captchas ###

    async def _producer_loop(self):
        """Internal async captcha creation producer loop."""
        while self._running:
            try:
                async with self._lock:
                    await self._generate_captcha()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.error(format_exc())
            await asyncio.sleep(self.interval_s)

    async def _generate_captcha(self):
        """Generate a captcha."""
        loop = asyncio.get_running_loop()
        # Generate a random one from the list of configured captchas
        if len(self.list_scenes) > 0:
            captcha_cfg = secrets.choice(self.list_scenes)
            result = await loop.run_in_executor(
                None,
                self._generator.generate,
                None,  # code
                captcha_cfg["scene"],
                self.out_dir,
                None,  # tmp_dir
                captcha_cfg["width"],
                captcha_cfg["height"],
                captcha_cfg["fps"],
                captcha_cfg["format"],
                captcha_cfg["renderer"],
                captcha_cfg["properties"],
            )
        # If none captchas configured, generate one from builtin
        else:
            result = await loop.run_in_executor(
                None,
                self._generator.generate,
                None,  # code
                None,  # scene
                self.out_dir
            )
        if result.error:
            logger.error("Captcha generation fail: %s", result.error_info)
        else:
            logger.debug("Generated captcha: %s", result.file)
            self.list_captcha_files.append(result.file)

    ###########################################################################

    ### Private Methods - Remove Captchas ###

    async def _remove_loop(self):
        """Internal async captcha remove/rotate loop."""
        while self._running:
            try:
                async with self._lock:
                    self._process_remove()
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.error(format_exc())
            await asyncio.sleep(self.interval_s)

    def _process_remove(self):
        """Remove oldest file if limit exceeded."""
        # Dont remove if number of captchas is less than max_items limit
        if len(self.list_captcha_files) < self.max_items:
            return
        # Remove oldest captcha file
        while len(self.list_captcha_files) > self.max_items:
            oldest = self.list_captcha_files.pop(0)
            try:
                # Atomic rename (protect race condition from consumers)
                # and delete the file
                deleting = oldest.with_suffix(oldest.suffix + ".deleting")
                oldest.rename(deleting)
                deleting.unlink(missing_ok=True)
                logger.info("Removed old captcha: %s", oldest)
            except PermissionError:
                logger.warning("File in use, skipping removal: %s", oldest)
            except Exception:
                logger.error(format_exc())

###############################################################################
