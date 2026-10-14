import os
from PIL import Image

IMG_DIR = r"c:\Users\Nor Anisa\Downloads\LOMBA SI\B-OUTDOOR\img"

# Load screenshots
map_im = Image.open(os.path.join(IMG_DIR, "screenshot_map.png")).convert("RGB")
dir_im = Image.open(os.path.join(IMG_DIR, "screenshot_dir.png")).convert("RGB")

w, h = map_im.size # 1440 x 900

# Crop map section (remove top announcement bar slightly, focus on header + map)
# y from 30 to 890
map_crop = map_im.crop((0, 32, w, 890))

# Crop dir section (remove top bar and focus on title + 3 cards)
dir_crop = dir_im.crop((0, 185, w, 790))

# Resize to standard width 1440
target_w = 1440
map_h = map_crop.size[1]
dir_h = dir_crop.size[1]

total_h = map_h + dir_h + 30 # with separator

composite = Image.new("RGB", (target_w, total_h), "#ffffff")
composite.paste(map_crop, (0, 0))
composite.paste(dir_crop, (0, map_h + 30))

out_path = os.path.join(IMG_DIR, "fig_4_4_real_screenshot.png")
composite.save(out_path, format="PNG", optimize=True)
print(f"Created real website composite: {out_path} ({composite.size})")
