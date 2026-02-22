
#
# This example shows how to use the CaptchaAutoGenerator for generating
# random builtin captchas without blocking (requires usage of asyncio).
#
# Note: The CaptchaAutoGenerator acts as a "producer" of captchas and
# you can have multiple "consumers" of the generated captchas in your
# application. Due CaptchaAutoGenerator focus in simplicity usage, no
# external locking-communication mechanism is needed by your
# application code to avoid race conditions, also CaptchaAutoGenerator
# doesn't open and provide a file-descriptor, instead it just provide a
# path to the captcha file. So under some conditions, it could happen
# that when you get a captcha, if your application takes a long time
# before opening this file, that file could habe been removed by the
# CaptchaAutoGenerator due the file rotation. All of this means, that
# is your application responsibility to check and handle the "file not
# found" exception when you are going to open the captcha file and it
# doesn't exists anymore, and retry to get a new captcha if that
# happens.
#

###############################################################################
# Libraries
###############################################################################

import asyncio
import logging
import shutil
from manim_captcha.auto_generator import CaptchaAutoGenerator
from pathlib import Path


###############################################################################
# Logger Setup
###############################################################################

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


###############################################################################
# Auxiliary Functions
###############################################################################

def rmdir(dir):
    try:
        shutil.rmtree(dir, ignore_errors=True)
    except Exception:
        logger.error("Fail to remove directory: %s", dir)


###############################################################################
# main Function
###############################################################################

async def main():
    # Setup the CaptchaAutoGenerator to trigger a captcha generation
    # each 10s and only allowing to have a maximum of 5 captchas in the
    # output directory (older captchas will be automatically removed
    # and renewed with new ones)
    MAX_NUM_CAPTCHAS = 5
    TIME_GEN_INTERVAL_S = 10
    OUT_DIR = Path("./captchas")
    rmdir(OUT_DIR)
    auto_generator = CaptchaAutoGenerator(
        OUT_DIR, TIME_GEN_INTERVAL_S, MAX_NUM_CAPTCHAS)
    # Start the generator process
    start_success = await auto_generator.start()
    if not start_success:
        logger.error("Fail to Start CaptchaAutoGenerator")
        return
    # Wait and get some captchas during 1 minute
    TIME_CHECK_S = 120
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
        if time_pass_s >= TIME_CHECK_S:
            run = False
    # Stop the generator process
    await auto_generator.stop()


###############################################################################
# Main Call
###############################################################################

if __name__ == '__main__':
    asyncio.run(main())
