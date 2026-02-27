#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script:
    manim_launcher.py
Description:
    Manim process launcher.
    This script runs Manim process to render a Scene for the provided
    JSON configuration. It main purpose is to be used by the generator
    via subprocess for memory isolation (running Manim as subprocess
    ensures all RAM memory resources are completely free once process
    ends) to avoid RAM memory fragmentation or any possible leak at
    Manim or ffmpg affects the generator process that uses it.
Author:
    Jose Miguel Rios Rubio
Date:
    27/02/2026
Version:
    1.0.0
"""

###############################################################################
# Standard Libraries
###############################################################################

import json
import logging
import sys


###############################################################################
# Third-Party Libraries
###############################################################################

import manim


###############################################################################
# Main Function
###############################################################################

def main(argc, argv):
    # Set Manim logging level to error to hide messages
    logging.getLogger("manim").setLevel(logging.ERROR)
    # Get Manim config data from argments
    if argc < 1:
        return 1
    json_data = json.loads(argv[0])
    # Sanitize json data to expected types
    if len(json_data["properties"]) == 0:
        json_data["properties"] = None
    bg_color = manim.ManimColor(json_data["background_color"])
    json_data["background_color"] = bg_color
    json_data["renderer"] = manim.constants.RendererType[json_data["renderer"]]
    print(json_data)
    # Load Manim Scene
    scene_module = json_data["scene_module"]
    scene_class = json_data["scene_class"]
    module = __import__(scene_module, fromlist=[scene_class])
    SceneClass = getattr(module, scene_class)
    # Setup config renderer type
    manim_config = {
        "renderer": json_data["renderer"],
        "format": json_data["format"],
        "pixel_width": json_data["pixel_width"],
        "pixel_height": json_data["pixel_height"],
        "frame_rate": json_data["frame_rate"],
        "background_color": json_data["background_color"],
        "media_dir": json_data["media_dir"],
        "output_file": json_data["output_file"],
        # "disable_caching": True,
        "write_to_movie": True,
        "progress_bar": "none",
        "preview": False,
    }
    with manim._config.tempconfig(manim_config):
        SceneClass(json_data["code"], json_data["properties"]).render()
    return 0


###############################################################################
# Main Call
###############################################################################

if __name__ == "__main__":
    rc = main(len(sys.argv) - 1, sys.argv[1:])
    sys.exit(rc)
