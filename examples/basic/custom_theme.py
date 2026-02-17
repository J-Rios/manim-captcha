
# This example shows how to provide external properties to a captcha
# scene in order to customize some colors.

from manim_captcha.generator import CaptchaGenerator
from manim_captcha.scenes import CaptchaScene
from manim_captcha.colors import CaptchaColorCustom
from pathlib import Path

THEME = {
    "bg_color": CaptchaColorCustom("#84D5E9"),
    "draw_color": CaptchaColorCustom("#FDA552"),
    "selector_color": CaptchaColorCustom("#FDC189"),
    "container_color": CaptchaColorCustom("#FBFCC0")
}

generator = CaptchaGenerator()

captcha = generator.generate(
    code="1234",
    scene=CaptchaScene.PIRAMID_NUMS,
    out_dir=Path("./captchas"),
    properties=THEME
)

print("")
if captcha.error:
    print("Fail to create the captcha:")
    print(captcha.error_info)
else:
    print("Captcha successfully created")
    print(f"  Code: \"{captcha.code}\"")
    print(f"  File: {captcha.file}")
print("")
