# sheet.py <dir> <out.jpg> <cols> [thumb_w]  — tile t_*.jpg / at_*.jpg into a labeled contact sheet
import sys, glob, os
from PIL import Image, ImageDraw
d, out, cols = sys.argv[1], sys.argv[2], int(sys.argv[3]); tw = int(sys.argv[4]) if len(sys.argv) > 4 else 320
files = sorted(glob.glob(os.path.join(d, 't_*.jpg')) + glob.glob(os.path.join(d, 'at_*.jpg')))
if not files: sys.exit('no frames')
ims = []
for f in files:
    im = Image.open(f).convert('RGB'); th = round(tw * im.height / im.width); ims.append((os.path.basename(f), im.resize((tw, th))))
th = ims[0][1].height; rows = (len(ims) + cols - 1) // cols; LBL = 18
sheet = Image.new('RGB', (cols * tw, rows * (th + LBL)), (20, 20, 20)); dr = ImageDraw.Draw(sheet)
for i, (name, im) in enumerate(ims):
    x, y = (i % cols) * tw, (i // cols) * (th + LBL); sheet.paste(im, (x, y + LBL)); dr.text((x + 4, y + 2), name.replace('.jpg', ''), fill=(255, 220, 120))
sheet.save(out, quality=82); print(out, sheet.size, len(ims), 'frames')
