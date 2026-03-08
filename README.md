# Manim-Captcha

<div style="display: flex;">
  <img src="https://github.com/user-attachments/assets/62677f79-c7a3-49ad-b01a-0143e48cb7ae" alt="captcha_circle" width="270" />
  <img src="https://github.com/user-attachments/assets/223b7e2d-99c4-410e-ab6e-4966ad47d2e8" alt="captcha_matrix" width="270" />
  <img src="https://github.com/user-attachments/assets/3c606acd-24bf-45bf-8a45-6127f392ea73" alt="captcha_piramid" width="270" />
</div>
<div style="display: flex;">
<img src="https://github.com/user-attachments/assets/67b04e84-1278-4bbe-87e1-6b5c301396f5" alt="custom_captcha" width="270" />
</div>

## Overview

Animated visual captcha generation library using [Manim Framework](https://github.com/ManimCommunity/manim).

Traditional CAPTCHAs are static images. Manim-Captcha generates animated visual challenges (e.g., moving selectors, distributed numbers, dynamic noise).

This library offers:

- A "Captcha Generator" that allows to request generation of captcha files.
- A "Captcha Automatic Generator" for async operation that acts as a background process to automatically generate captcha files in the filesystem for a custom interval and keeping a maximum number of captchas files (file rotation).
- Some builtin captcha animations that you can select to use.
- Kind of "plugin" based system were you can provide any external custom Manim captcha animation script (scene) and make the library use it.
- Easy way to pass custom properties to the captcha scenes for customization (like scenes).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Library Development](#library-development)

## Requirements

The manim-captcha library requires python 3 (tested with v3.12), Manim Community framework, and the corresponding requirements for Manim (like Cairo and Pango libraries).

## Installation

**Note:** The next installation instructions are for Debian based Linux systems.

From a command line, install the different requirements:

```bash
sudo apt-get update
sudo apt-get install build-essential make python3 python3-dev python3-pip
sudo apt-get install libcairo2-dev libpango1.0-dev
```

The library has been published to pypi so can be easily installed via pip:

```bash
pip install manim-captcha
```

## Usage

Basic captcha generator:

```python
from manim_captcha.generator import CaptchaGenerator
from manim_captcha.scenes import CaptchaScene
from pathlib import Path

generator = CaptchaGenerator()

captcha = generator.generate(
    code="1234",
    scene=CaptchaScene.CIRCLE_NUMS,
    out_dir=Path("./captchas"),
    properties={
        "theme": "dark",
        "noise": True
    }
)

if captcha.error:
    print("Fail to create the captcha:")
    print(captcha.error_info)
else:
    print("Captcha successfully created")
    print(f"  Code: \"{captcha.code}\"")
    print(f"  File: {captcha.file}")
print("")
```

Async and non-blocking automatic captcha generator:

```python
import asyncio
import logging
from manim_captcha.auto_generator import CaptchaAutoGenerator
from pathlib import Path

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def main():
    # Setup the CaptchaAutoGenerator
    MAX_NUM_CAPTCHAS = 5
    TIME_GEN_INTERVAL_S = 10
    OUT_DIR = Path("./captchas")
    auto_generator = CaptchaAutoGenerator(
        OUT_DIR, TIME_GEN_INTERVAL_S, MAX_NUM_CAPTCHAS)
    # Start the generator process
    start_success = await auto_generator.start()
    if not start_success:
        logger.error("Fail to Start CaptchaAutoGenerator")
        return
    # Wait and get some captchas during 1 minute
    TIME_CHECK = 60
    time_pass_s = 0
    run = True
    while run:
        # Show number of captchas availables
        num_captchas = auto_generator.num_captchas()
        logger.info("Num Captchas Availables: %d", num_captchas)
        # Try to get a captcha
        captcha = auto_generator.get_captcha()
        if not captcha.error:
            logger.info("Captcha retrieved:")
            logger.info("  Code: \"%s\"", captcha.code)
            logger.info("  File: %s", str(captcha.file))
        await asyncio.sleep(TIME_GEN_INTERVAL_S)
        # Check if check end time has arrive to exit the loop
        time_pass_s = time_pass_s + TIME_GEN_INTERVAL_S
        if time_pass_s >= TIME_CHECK:
            run = False
    # Stop the generator process
    await auto_generator.stop()

if __name__ == '__main__':
    asyncio.run(main())
```

**Note:** You can find some extra usages in the *examples/* directory.

## Use my own external custom captcha

The library provides some builtin captchas, but the most useful feature is that it allows you to easily pass to the generator any external custom captcha scene that you have define.

Take a look into [this example](examples/custom_captcha) to know how it works.

## Library Development

For library development, to ease project setup and installation of all the requirements, a Makefile and some bash scripts are provided for Linux systems based on Debian.

Setup the project (this will install all system requirements and creates a python virtual environment):

```bash
make setup
```

Extra actions can be performed through make, just run make without argments to see the usage help:

```bash
make

Usage:
  setup: Setup Project and install requirements
  test: Run project tests
  check_code_style: Run Code Style Checks
  check_static_types: Run Static Types Checks
  install: Install local package in edit mode
  publish: Publish the library to pypi
```

Now open any code editor (i.e. vscode) withing the python environment and start coding!
