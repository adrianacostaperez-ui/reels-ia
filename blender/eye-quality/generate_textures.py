"""Deterministic iris stroma / crypts and scleral capillaries; no stock assets."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
OUT=Path(__file__).resolve().parent/'assets';OUT.mkdir(exist_ok=True)
rng=np.random.default_rng(81278);N=2048
y,x=np.mgrid[-1:1:complex(N),-1:1:complex(N)].astype(np.float32);r=np.sqrt(x*x+y*y);a=np.arctan2(y,x)
def noise(n):
 im=Image.fromarray(rng.integers(0,256,(n,n),dtype=np.uint8)).resize((N,N),Image.Resampling.BICUBIC)
 return np.asarray(im,dtype=np.float32)/255-.5
warp=a+.014*np.sin(r*46+np.sin(a*17)*1.8)+.004*np.sin(r*88+a*23)
fibre=np.zeros_like(r)
for freq,amp in [(67,.45),(137,.27),(291,.17),(553,.11),(887,.06)]:
 fibre+=amp*np.sin(warp*freq+np.sin(r*(22+freq*.015)+a*13)*1.9)
fibre*=.35+.65*np.sin(np.clip((r-.29)/.7,0,1)*np.pi)
fb=noise(80)*.08+noise(340)*.055+noise(1024)*.025
warm=np.exp(-((r-.39)/.14)**2)
base=np.stack([.26+warm*.19,.37+warm*.015,.39-warm*.15],axis=-1)
base*=1+fibre[...,None]*.28+fb[...,None]
height=.50+fibre*.075+fb*.7
# Stromal crypts are irregular depressions with raised rims, not straight spokes.
for i in range(210):
 theta=float(rng.uniform(-np.pi,np.pi));rr=float(rng.choice([.46,.53,.78])+rng.normal(0,.035));cx=np.cos(theta)*rr;cy=np.sin(theta)*rr
 rad=float(rng.uniform(.012,.050));tan=float(rng.uniform(.004,.014));reach=rad*3
 ix=int((cx+1)*N/2);iy=int((cy+1)*N/2);span=int(reach*N/2)+3
 x0=max(0,ix-span);x1=min(N,ix+span);y0=max(0,iy-span);y1=min(N,iy+span)
 dx=x[y0:y1,x0:x1]-cx;dy=y[y0:y1,x0:x1]-cy
 dr=dx*np.cos(theta)+dy*np.sin(theta);dt=-dx*np.sin(theta)+dy*np.cos(theta)
 g=np.exp(-.5*((dr/rad)**2+(dt/tan)**2));rim=np.exp(-.5*((dr/(rad*1.4))**2+(dt/(tan*1.5))**2))-g
 base[y0:y1,x0:x1]*=(1-.44*g[...,None]);base[y0:y1,x0:x1]+=rim[...,None]*.045;height[y0:y1,x0:x1]-=g*.16;height[y0:y1,x0:x1]+=rim*.06
limbus=1-.78*np.clip((r-.87)/.12,0,1)**1.5
base*=limbus[...,None]
pupil=.318+.006*np.sin(a*47)+.004*np.sin(a*113)
base*=np.clip((r-pupil)/.024,0,1)[...,None]*.9+.1
Image.fromarray(np.uint8(np.clip(base,0,1)*255)).save(OUT/'iris-color.png')
Image.fromarray(np.uint16(np.clip(height,0,1)*65535)).save(OUT/'iris-height.png')
# Creamy sclera with fine, branching superficial capillaries.
W,H=2048,1024
im=Image.new('RGB',(W,H),(217,211,203));v=Image.new('RGBA',(W,H));d=ImageDraw.Draw(v)
rrng=np.random.default_rng(572)
for i in range(95):
 sx=float(rrng.uniform(0,W));sy=float(rrng.uniform(0,H));ang=float(rrng.uniform(0,2*np.pi));steps=int(rrng.integers(12,34));pts=[(sx,sy)]
 for k in range(steps):
  ang+=float(rrng.normal(0,.16));sx+=np.cos(ang)*float(rrng.uniform(4,10));sy+=np.sin(ang)*float(rrng.uniform(4,10));pts.append((sx,sy))
 d.line(pts,fill=(151,65,70,int(rrng.integers(15,45))),width=int(rrng.choice([1,1,2])),joint='curve')
 for q in [len(pts)//3,len(pts)*2//3]:
  xx,yy=pts[q];at=ang+float(rrng.choice([-1,1]))*.6;branch=[(xx,yy)]
  for j in range(8):at+=float(rrng.normal(0,.22));xx+=np.cos(at)*5;yy+=np.sin(at)*5;branch.append((xx,yy))
  d.line(branch,fill=(161,76,79,22),width=1,joint='curve')
v=v.filter(ImageFilter.GaussianBlur(.30));im=Image.alpha_composite(im.convert('RGBA'),v).convert('RGB');im.save(OUT/'sclera-color.png')
print('Generated',OUT)
