"""Extract alpha-only photographic layers. Never regenerate or retouch the eye.
The original RGB source remains byte-for-byte unchanged. No inpainting, anatomy
synthesis, optical-flow deformation, sharpening or generative model is used.
"""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public/eye-2-5d'
SOURCE=OUT/'source.png'
EXPECTED='1767b8c9ed6cf6d40f4350c87813266ffcf5123fc7bb4a4a4385a04471a8c690'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
im=Image.open(SOURCE).convert('RGB');assert im.size==(941,1672)

def save_layer(name,mask):
    layer=im.copy().convert('RGBA');layer.putalpha(mask)
    layer.save(OUT/f'{name}.png')

def cubic(p0,p1,p2,p3):
    t=np.linspace(0,1,100)[:,None]
    return ((1-t)**3*np.array(p0)+3*(1-t)**2*t*np.array(p1)+3*(1-t)*t*t*np.array(p2)+t**3*np.array(p3)).tolist()

# Includes original upper/lower lashes, their roots and adjacent eyelid tissue.
# Broad feather boundaries lie in skin, away from high-contrast lash contours.
mask=Image.new('L',im.size);d=ImageDraw.Draw(mask)
d.polygon([(70,740),(106,650),(275,540),(505,525),(710,560),(866,650),(925,790),(919,947),(804,1045),(565,1100),(281,1105),(110,1012)],fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(24));save_layer('lashes',mask)

# Inner ocular surface. This contains photographic sclera/cornea, not a sphere.
path=[]
for ps in [((289,800),(350,703),(453,649),(560,654)),((560,654),(687,649),(797,744),(867,875)),((867,875),(768,899),(613,923),(468,900)),((468,900),(378,888),(303,845),(289,800))]:
    path.extend(cubic(*ps))
ap=Image.new('L',im.size);ImageDraw.Draw(ap).polygon([tuple(p) for p in path],fill=255)
ap=ap.filter(ImageFilter.GaussianBlur(5));save_layer('cornea',ap)

# Rigid iris + pupil together. Alpha is clipped to the photographic aperture.
iris=Image.new('L',im.size);ImageDraw.Draw(iris).ellipse((415,635,728,911),fill=255)
iris=iris.filter(ImageFilter.GaussianBlur(7))
iris=Image.fromarray(np.uint8(np.asarray(iris,dtype=np.float32)*np.asarray(ap,dtype=np.float32)/255))
save_layer('iris',iris)

# White alpha matte for a restrained optical light pass in Remotion.
lightmask=Image.new('RGBA',im.size,(255,255,255,0));lightmask.putalpha(ap);lightmask.save(OUT/'cornea-alpha.png')
report={'source':'source.png','sourceSha256':EXPECTED,'sourceDimensions':list(im.size),'layers':['source.png','lashes.png','cornea.png','iris.png'],'processing':'original RGB pixels plus feathered alpha masks only','newEyeGenerated':False,'inpainting':False,'irisOrLashGeometryWarped':False}
(OUT/'source-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
