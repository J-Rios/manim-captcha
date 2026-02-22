
# This example shows basic operation on how to generate one of the
# builtin captcha scenes (CIRCLE_NUMS).

from manim_captcha.generator import CaptchaGenerator
from manim_captcha.scenes import CaptchaScene
from pathlib import Path

generator = CaptchaGenerator()

captcha = generator.generate(
    code="1234",
    scene=CaptchaScene.CIRCLE_NUMS,
    out_dir=Path("./captchas"),
    format="mp4",
    properties={
        "theme": "dark",
        "noise": True
    }
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
