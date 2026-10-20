"""Cycles look-development anchors. All source poses are real 1080×1920 renders.
The CPU-only preview uses optical-flow inbetweens; this is recorded, not hidden.
"""
import bpy,time,json,sys,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'out/blender-eye';DEST=OUT/'anchors';DEST.mkdir(exist_ok=True,parents=True)
bpy.ops.wm.open_mainfile(filepath=str(OUT/'eye-quality.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.adaptive_min_samples=8;s.cycles.adaptive_threshold=.035;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=5;s.render.use_persistent_data=True
s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='16';s.render.image_settings.color_mode='RGB'
frames=list(range(1,147,5))+[150];report={'engine':'Blender 5.2.2 LTS / Cycles CPU','resolution':[1080,1920],'maxSamples':24,'adaptiveMinimum':8,'noiseThreshold':.035,'denoiser':'OpenImageDenoise integrated','sourceFrames':frames,'sourceFrameCount':len(frames),'targetFrames':150,'targetFps':30,'duration':5,'interpolation':'FFmpeg motion-compensated optical flow between 31 Cycles poses; not 150 independent path-traced frames','finished':[]}
start=time.time()
for i,f in enumerate(frames):
 p=DEST/f'{f:04d}.png'
 if p.exists():report['finished'].append({'frame':f,'reused':True});continue
 s.frame_set(f);s.render.filepath=str(p);t=time.time();bpy.ops.render.render(write_still=True)
 item={'frame':f,'seconds':round(time.time()-t,2)};report['finished'].append(item);report['elapsedSeconds']=round(time.time()-start,2)
 (OUT/'render-progress.json').write_text(json.dumps(report,indent=2)+'\n');print('ANCHOR',i+1,'/',len(frames),json.dumps(item),flush=True)
(OUT/'render-progress.json').write_text(json.dumps(report,indent=2)+'\n');print('ALL_CYCLES_ANCHORS_READY',flush=True)
