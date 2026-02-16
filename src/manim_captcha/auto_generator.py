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

# None


###############################################################################
# Local Libraries
###############################################################################

from manim_captcha.generator import CaptchaGenerator


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

    class CaptchaData:
        """Captcha information."""

        def __init__(self):
            self.code: str = ""
            self.file: Path | None = None
            self.error: bool = False
            self.error_info: str = ""

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

    async def start(self) -> bool:
        '''Launch the manager to start creating captchas.'''
        if not self.available:
            return False
        if self._running:
            return False
        self._running = True
        self._task_create = asyncio.create_task(self._producer_loop())
        self._task_remove = asyncio.create_task(self._remove_loop())
        return True

    async def stop(self):
        '''Stop the manager and the captcha creation.'''
        self._running = False
        if self._task_create:
            await self._task_create
            self._task_create = None
        if self._task_remove:
            await self._task_remove
            self._task_remove = None

    def get_captcha(self) -> CaptchaData:
        '''Return a random captcha file from storage.'''
        captcha_result = self.CaptchaData()
        if not self.available:
            captcha_result.error = True
            captcha_result.error_info = "Manim not found in the system"
            return captcha_result
        try:
            files = list(self.out_dir.glob(f"*.{self.format}"))
            if not files:
                captcha_result.error = True
                captcha_result.error_info = "None captcha files generated"
                return captcha_result
            captcha_result.file = secrets.choice(files)
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
            except Exception:
                logger.error(format_exc())
            await asyncio.sleep(self.interval_s)

    async def _generate_captcha(self):
        """Generate one captcha."""
        # Dont generate if number of captchas is at max_items limit
        files = list(self.out_dir.glob(f"*.{self.format}"))
        if len(files) >= self.max_items:
            return
        # Generate a new captcha
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None,
            self._generator.generate,
            None,  # code
            None,  # scene
            self.out_dir
        )
        if result.error:
            logger.error("Captcha generation failed: %s", result.error_info)
        else:
            logger.info("Generated captcha: %s", result.file)

    ###########################################################################

    ### Private Methods - Remove Captchas ###

    async def _remove_loop(self):
        """Internal async captcha remove/rotate loop."""
        while self._running:
            try:
                async with self._lock:
                    await self._process_remove()
            except Exception:
                logger.error(format_exc())
            await asyncio.sleep(1)

    def _process_remove(self):
        """Remove oldest file if limit exceeded."""
        # Dont remove if number of captchas is less than max_items limit
        files = list(self.out_dir.glob(f"*.{self.format}"))
        if len(files) <= self.max_items:
            return
        # Remove oldest captcha file
        files.sort(key=lambda p: p.stat().st_mtime)
        while len(files) > self.max_items:
            oldest = files.pop(0)
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
