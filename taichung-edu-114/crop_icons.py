import os
from PIL import Image

def crop_and_remove_bg():
    img_path = "images/icon_sheet.png"
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found.")
        return

    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    n = 8
    icons = [f"icon_{i+1}" for i in range(n)]

    # Make background (#0d1117) transparent
    # We can do this by converting very dark pixels (close to #0d1117) to transparent.
    # #0d1117 is rgb(13, 17, 23). We'll set a threshold.
    datas = img.getdata()
    new_data = []
    for item in datas:
        # Check if pixel is very dark (r < 25, g < 25, b < 30)
        if item[0] < 25 and item[1] < 25 and item[2] < 30:
            new_data.append((0, 0, 0, 0)) # transparent
        else:
            new_data.append(item)
    img.putdata(new_data)

    print("Background removed. Splitting and cropping icons...")

    for i, name in enumerate(icons):
        x0 = i * (w // n)
        x1 = (i + 1) * (w // n) if i < n-1 else w
        col_w = x1 - x0
        sq = min(col_w, h)
        cx, cy = x0 + col_w // 2, h // 2
        crop = img.crop((cx-sq//2, cy-sq//2, cx+sq//2, cy+sq//2))
        # Try robust resample filters
        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            try:
                resample_filter = Image.LANCZOS
            except AttributeError:
                resample_filter = Image.ANTIALIAS
        crop = crop.resize((256, 256), resample_filter)
        crop.save(f"images/{name}.png")
        print(f"Saved: images/{name}.png")

if __name__ == "__main__":
    crop_and_remove_bg()
