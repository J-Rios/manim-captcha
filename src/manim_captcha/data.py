#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    data.py
Description:
    Manim Captcha Data (constants and data types).
Author:
    Jose Miguel Rios Rubio
Date:
    16/02/2026
Version:
    1.0.0
"""

###############################################################################
# Standard Libraries
###############################################################################

from pathlib import Path


###############################################################################
# Constants
###############################################################################

# None


###############################################################################
# Data Types
###############################################################################

class CaptchaData:
    """Captcha information."""

    def __init__(self):
        self.code: str = ""
        self.file: Path | None = None
        self.error: bool = False
        self.error_info: str = ""

###############################################################################
