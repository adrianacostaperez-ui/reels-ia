"""Produce 150 output images from 31 fully rendered Cycles camera poses.
No still-image zoom: the optical-flow anchors contain physical parallax/DOF.
This is a CPU look-development optimization, explicitly recorded in metadata.
"""
from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];O=R/'out/blender-eye';A=O/'anchors';D=R/'public/blender-eye/frames';D.mkdir(parents=True,exist_ok=True)
frames=list(range(1,147,5))+[150]
for f in frames:assert (A/f'{f:04d}.png').exists(),f
# One leading anchor and two trailing anchors let the bidirectional estimator
# see both neighbors all the way through the requested 0..149 output range.
lines=['ffconcat version 1.0']
def add(f,d):lines.extend(["file '"+str(A/f'{f:04d}.png')+"'",'option framerate 30',f'duration {d:.9f}'])
add(1,1/6)
for i,f in enumerate(frames):
 duration=(frames[i+1]-f)/30 if i+1<len(frames) else 1/6
 add(f,duration)
add(150,1/6);lines.append("file '"+str(A/'0150.png')+"'")
manifest=O/'anchors.ffconcat';manifest.write_text('\n'.join(lines)+'\n')
subprocess.run(['ffmpeg','-v','error','-y','-safe','0','-i',str(manifest),'-vf','format=yuv444p,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1:search_param=32,trim=start=0.166666:end=5.166666,setpts=N/(30*TB)','-fps_mode','passthrough','-frames:v','150',str(D/'%04d.png')],check=True)
files=sorted(D.glob('*.png'));assert len(files)==150,len(files)
print('INTERPOLATION_COMPLETE',len(files),flush=True)
