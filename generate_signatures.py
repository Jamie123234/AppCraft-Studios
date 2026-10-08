import base64
import os
import subprocess
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, 'email-signatures')
SCRATCH_DIR = os.path.join(BASE_DIR, 'scratch')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

# 1. Tight-cropped version of the logo with 0px transparent border
raw_logo = Image.open(os.path.join(BASE_DIR, 'appcraft_studios.png'))
tight_logo = raw_logo.crop(raw_logo.getbbox())
tight_logo_path = os.path.join(SCRATCH_DIR, 'logo_tight.png')
tight_logo.save(tight_logo_path, 'PNG')

with open(tight_logo_path, 'rb') as f:
    logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode('utf-8')

# Crop function for transparent signatures that removes all transparent/invisible pixels
def crop_visible(img, alpha_threshold=20):
    arr = np.array(img)
    if arr.shape[2] < 4:
        return img
    alpha = arr[:, :, 3]
    rows = np.where(np.max(alpha, axis=1) > alpha_threshold)[0]
    cols = np.where(np.max(alpha, axis=0) > alpha_threshold)[0]
    if len(rows) > 0 and len(cols) > 0:
        return img.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return img

# Template configurations
# format: (html_string, is_solid, width, height)
templates = {
    # 1. EXECUTIVE CARD - SOLID FILL, NO CORNER RADIUS, ZERO TRANSPARENT MARGIN (100% OPAQUE)
    "appcraft-signature-executive": (
        f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin:0; padding:0; }}
html, body {{
    margin: 0;
    padding: 0;
    background: #FFFFFF;
    width: 500px;
    height: 100px;
    overflow: hidden;
}}
.card {{
    width: 500px;
    height: 100px;
    background: #FFFFFF;
    border-radius: 0;
    margin: 0;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    border-left: 5px solid #1D63ED;
    border-top: 1px solid #E2E8F0;
    border-right: 1px solid #E2E8F0;
    border-bottom: 1px solid #E2E8F0;
}}
.logo-img {{
    width: 46px;
    height: 46px;
    object-fit: contain;
    display: block;
    margin-right: 16px;
}}
.divider {{
    width: 1.5px;
    height: 44px;
    background: #E2E8F0;
    margin-right: 16px;
}}
.name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.2;
    margin-bottom: 2px;
}}
.title {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #1D63ED;
    margin-bottom: 2px;
}}
.site {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    color: #64748B;
}}
</style>
</head>
<body>
<div class="card">
    <img src="{logo_b64}" class="logo-img" alt="AppCraft Studios">
    <div class="divider"></div>
    <div>
        <div class="name">Jamie Abrahams</div>
        <div class="title">CEO, AppCraft Studios (Pty) Ltd</div>
        <div class="site">www.appcraftstudios.com</div>
    </div>
</div>
</body>
</html>''',
        True,  # is_solid (fills whole container, no transparent pixels)
        500,
        100
    ),

    # 2. EXECUTIVE DARK CARD - SOLID FILL, NO CORNER RADIUS
    "appcraft-signature-executive-dark": (
        f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin:0; padding:0; }}
html, body {{
    margin: 0;
    padding: 0;
    background: #0B192C;
    width: 500px;
    height: 100px;
    overflow: hidden;
}}
.card {{
    width: 500px;
    height: 100px;
    background: #0B192C;
    border-radius: 0;
    margin: 0;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    border-left: 5px solid #38BDF8;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}}
.logo-img {{
    width: 46px;
    height: 46px;
    object-fit: contain;
    display: block;
    margin-right: 16px;
}}
.divider {{
    width: 1.5px;
    height: 44px;
    background: rgba(255, 255, 255, 0.15);
    margin-right: 16px;
}}
.name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 2px;
}}
.title {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #38BDF8;
    margin-bottom: 2px;
}}
.site {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    color: #94A3B8;
}}
</style>
</head>
<body>
<div class="card">
    <img src="{logo_b64}" class="logo-img" alt="AppCraft Studios">
    <div class="divider"></div>
    <div>
        <div class="name">Jamie Abrahams</div>
        <div class="title">CEO, AppCraft Studios (Pty) Ltd</div>
        <div class="site">www.appcraftstudios.com</div>
    </div>
</div>
</body>
</html>''',
        True,
        500,
        100
    ),

    # 3. TEXT-FIRST FLUSH (Transparent background, zero margin)
    "appcraft-signature-text-first": (
        f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin:0; padding:0; }}
body {{ background: transparent; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; display: inline-block; margin:0; padding:0; }}
.sig {{
    display: inline-flex;
    align-items: center;
    background: transparent;
    margin: 0;
    padding: 0;
}}
.content {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.name {{
    font-size: 16px;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.15;
    margin-bottom: 3px;
    letter-spacing: -0.2px;
}}
.title {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #1D63ED;
    line-height: 1.2;
    margin-bottom: 3px;
}}
.site {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    color: #64748B;
    line-height: 1.2;
}}
.divider {{
    width: 2px;
    height: 42px;
    background: #1D63ED;
    border-radius: 2px;
    margin: 0 14px 0 16px;
}}
.logo-img {{
    width: 44px;
    height: 44px;
    object-fit: contain;
    display: block;
}}
</style>
</head>
<body>
<div class="sig">
    <div class="content">
        <div class="name">Jamie Abrahams</div>
        <div class="title">CEO, AppCraft Studios (Pty) Ltd</div>
        <div class="site">www.appcraftstudios.com</div>
    </div>
    <div class="divider"></div>
    <img src="{logo_b64}" class="logo-img" alt="AppCraft Studios">
</div>
</body>
</html>''',
        False,
        900,
        300
    ),

    # 4. LOGO-FIRST MINIMAL (Transparent, tight crop to edge)
    "appcraft-signature-minimal": (
        f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin:0; padding:0; }}
body {{ background: transparent; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; display: inline-block; margin:0; padding:0; }}
.sig {{
    display: inline-flex;
    align-items: center;
    background: transparent;
    margin: 0;
    padding: 0;
}}
.logo-img {{
    width: 44px;
    height: 44px;
    object-fit: contain;
    display: block;
    margin: 0;
}}
.divider {{
    width: 2px;
    height: 42px;
    background: #1D63ED;
    border-radius: 2px;
    margin: 0 12px;
}}
.content {{
    display: flex;
    flex-direction: column;
    justify-content: center;
}}
.name {{
    font-size: 16px;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.15;
    margin-bottom: 3px;
    letter-spacing: -0.2px;
}}
.title {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #1D63ED;
    line-height: 1.2;
    margin-bottom: 3px;
}}
.site {{
    font-family: 'Inter', sans-serif;
    font-size: 11px;
    font-weight: 500;
    color: #64748B;
    line-height: 1.2;
}}
</style>
</head>
<body>
<div class="sig">
    <img src="{logo_b64}" class="logo-img" alt="AppCraft Studios">
    <div class="divider"></div>
    <div class="content">
        <div class="name">Jamie Abrahams</div>
        <div class="title">CEO, AppCraft Studios (Pty) Ltd</div>
        <div class="site">www.appcraftstudios.com</div>
    </div>
</div>
</body>
</html>''',
        False,
        900,
        300
    ),

    # 5. PURE (Name + Title Only, zero margin)
    "appcraft-signature-pure": (
        f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Inter:wght@500;600&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin:0; padding:0; }}
body {{ background: transparent; font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; display: inline-block; margin:0; padding:0; }}
.sig {{
    display: inline-flex;
    align-items: center;
    background: transparent;
    margin: 0;
    padding: 0;
}}
.content {{
    display: flex;
    flex-direction: column;
}}
.name {{
    font-size: 15px;
    font-weight: 800;
    color: #0B192C;
    line-height: 1.2;
    margin-bottom: 2px;
}}
.title {{
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #1D63ED;
    line-height: 1.2;
}}
.divider {{
    width: 2px;
    height: 32px;
    background: #1D63ED;
    border-radius: 2px;
    margin: 0 12px 0 14px;
}}
.logo-img {{
    width: 34px;
    height: 34px;
    object-fit: contain;
    display: block;
}}
</style>
</head>
<body>
<div class="sig">
    <div class="content">
        <div class="name">Jamie Abrahams</div>
        <div class="title">CEO, AppCraft Studios (Pty) Ltd</div>
    </div>
    <div class="divider"></div>
    <img src="{logo_b64}" class="logo-img" alt="AppCraft Studios">
</div>
</body>
</html>''',
        False,
        900,
        300
    )
}

temp_html_path = os.path.join(SCRATCH_DIR, 'temp_sig_render.html')

for name, (html_content, is_solid, width, height) in templates.items():
    print(f"Generating {name}...")
    with open(temp_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_png_path = os.path.join(OUT_DIR, f"{name}.png")
    
    if is_solid:
        # For solid containers: screenshot the exact container dimensions with NO transparency
        cmd = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless=new',
            '--hide-scrollbars',
            f'--window-size={width},{height}',
            '--virtual-time-budget=2000',
            '--force-device-scale-factor=2',
            f'--screenshot={final_png_path}',
            temp_html_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Verify it has NO transparent pixels
        img = Image.open(final_png_path)
        # Convert to RGB (completely opaque, 0 transparency) or ensure 255 alpha
        img_rgb = img.convert('RGB')
        img_rgb.save(final_png_path, "PNG")
        print(f"  -> Saved solid {final_png_path} ({img_rgb.size[0]}x{img_rgb.size[1]}px, 100% opaque, 0 corner radius)")
    else:
        raw_png_path = os.path.join(OUT_DIR, f"{name}-raw.png")
        cmd = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless=new',
            '--default-background-color=00000000',
            '--hide-scrollbars',
            f'--window-size={width},{height}',
            '--virtual-time-budget=2000',
            '--force-device-scale-factor=2',
            f'--screenshot={raw_png_path}',
            temp_html_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(raw_png_path):
            img = Image.open(raw_png_path)
            cropped = crop_visible(img, alpha_threshold=20)
            cropped.save(final_png_path, "PNG")
            print(f"  -> Saved {final_png_path} ({cropped.size[0]}x{cropped.size[1]}px, tightly cropped)")
            os.remove(raw_png_path)

if os.path.exists(temp_html_path):
    os.remove(temp_html_path)

print("All executive signatures successfully generated!")
