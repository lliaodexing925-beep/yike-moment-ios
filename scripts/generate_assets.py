from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import random
import plistlib

ROOT = Path(__file__).resolve().parents[1]
ICON = ROOT / "ios/App/App/Assets.xcassets/AppIcon.appiconset/AppIcon-512@2x.png"
SPLASH_DIR = ROOT / "ios/App/App/Assets.xcassets/Splash.imageset"

def font(size, latin=False):
    candidates = ["/System/Library/Fonts/Helvetica.ttc"] if latin else [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)

def background(size):
    image = Image.new("RGB", (size, size))
    draw = ImageDraw.Draw(image)
    for y in range(size):
        t = y / max(1, size - 1)
        color = (int(15 - 10*t), int(23 - 17*t), int(42 + 3*t))
        draw.line((0, y, size, y), fill=color)
    rng = random.Random(20261026)
    for _ in range(int(size * .12)):
        x, y = rng.randrange(size), rng.randrange(size)
        r = rng.choice([1, 1, 2, 2, 3]) * max(1, size // 1024)
        color = rng.choice([(235,245,255), (155,216,201), (182,192,208)])
        draw.ellipse((x-r,y-r,x+r,y+r), fill=color)
    return image

def centered(draw, xy, text, face, fill):
    draw.text(xy, text, font=face, fill=fill, anchor="mm")

ICON.parent.mkdir(parents=True, exist_ok=True)
icon = background(1024)
d = ImageDraw.Draw(icon)
d.ellipse((228,228,796,796), outline=(98,142,151), width=4)
d.ellipse((274,274,750,750), outline=(58,87,111), width=2)
centered(d, (512,495), "一", font(330), (248,250,252))
centered(d, (512,805), "MOMENT", font(35, latin=True), (155,216,201))
icon.save(ICON)

SPLASH_DIR.mkdir(parents=True, exist_ok=True)
splash = background(2732)
d = ImageDraw.Draw(splash)
d.ellipse((866,806,1866,1806), outline=(64,101,117), width=6)
centered(d, (1366,1240), "一刻", font(300), (248,250,252))
centered(d, (1366,1555), "MOMENT", font(58, latin=True), (155,216,201))
centered(d, (1366,1760), "每一刻，都清晰。", font(64), (182,192,208))
for name in ["splash-2732x2732-1.png", "splash-2732x2732-2.png", "splash-2732x2732.png"]:
    splash.save(SPLASH_DIR / name)

INFO = ROOT / "ios/App/App/Info.plist"
info = plistlib.loads(INFO.read_bytes())
info.update({
    "NSCameraUsageDescription": "拍摄照片或视频，保存到你的时刻。",
    "NSMicrophoneUsageDescription": "录制语音，保存到你的时刻。",
    "NSPhotoLibraryUsageDescription": "选择照片和视频，添加到你的时刻。",
    "NSPhotoLibraryAddUsageDescription": "保存你在时刻中查看的照片或视频。",
})
INFO.write_bytes(plistlib.dumps(info, fmt=plistlib.FMT_XML, sort_keys=False))
print("Generated visual assets and configured media permissions")
