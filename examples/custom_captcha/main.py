
# This example shows how to use your own external custom captcha scene
# with the generator.

from pathlib import Path
from manim_captcha.generator import CaptchaGenerator
from my_captcha import MyCaptcha

generator = CaptchaGenerator()

captcha = generator.generate(
    code="1234",
    scene=MyCaptcha,
    out_dir=Path("./captchas"),
    format="mp4",
    properties=None
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
