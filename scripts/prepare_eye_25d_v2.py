"""Add an alpha-only focus region from the same original pixels.
The first version's source, planes and MP4 remain unchanged.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import numpy as np,hashlib

R=Path(__file__).resolve().parents[1];D=R/'public/eye-2-5d';O=D/'v2';O.mkdir(exist_ok=True)
assert hashlib.sha256((D/'source.png').read_bytes()).hexdigest()=='1767b8c9ed6cf6d40f4350c87813266ffcf5123fc7bb4a4a4385a04471a8c690'
im=Image.open(D/'source.png').convert('RGBA')
mask=Image.new('L',im.size);ImageDraw.Draw(mask).ellipse((505,696,635,826),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(10))
outer=np.asarray(Image.open(D/'iris.png').getchannel('A'),dtype=np.float32)
mask=Image.fromarray(np.uint8(np.asarray(mask,dtype=np.float32)*outer/255))
im.putalpha(mask);im.save(O/'pupil.png')
print('V2_FOCUS_MASK_READY: original RGB retained, iris/pupil share one rigid transform')
