"""Verify final video geometry against the physically approved 15-second test."""
from pathlib import Path
import json,subprocess,hashlib
import numpy as np
from scipy.ndimage import label,find_objects
R=Path(__file__).resolve().parents[1]
movie=R/'deliverables/punto-ciego-v1.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)]))
v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',1898)
assert abs(float(info['format']['duration'])-1898/30)<.002
assert abs(float(a['duration'])-63.245714)<.002
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','select=between(n\\,58\\,484),crop=1080:100:0:980,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(-1,100,1080);assert len(frames)==427
centers=[];bounds=[]
for i,im in enumerate(frames,58):
 lab,n=label(im>150);assert n==2,(i,n)
 objects=find_objects(lab);cc=[];bb=[]
 for y,x in objects:
  cc.append([(x.start+x.stop-1)/2,(y.start+y.stop-1)/2+980]);bb.append([x.stop-x.start,y.stop-y.start])
 assert np.allclose(cc,[[189.5,1029.5],[869.5,1029.5]],atol=.6),(i,cc)
 centers.append(cc);bounds.append(bb)
assert np.max(np.ptp(np.array(centers),axis=0))==0
assert np.max(np.ptp(np.array(bounds),axis=0))<=1
# Compare the exact same stimulus strip in the original approved video.
oldraw=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'deliverables/punto-ciego-test-15s.mp4'),'-vf','select=eq(n\\,390),crop=1080:100:0:980,format=gray','-fps_mode','passthrough','-f','rawvideo','-'])
old=np.frombuffer(oldraw,np.uint8).reshape(100,1080)
assert np.abs(old.astype(float)-frames[390-58].astype(float)).mean()<.6
pause=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','select=between(n\\,324\\,443),scale=270:480','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'])
pause=np.frombuffer(pause,np.uint8).reshape(-1,480,270,3);assert len(pause)==120
change=max(float(np.abs(x.astype(float)-pause[0].astype(float)).mean()) for x in pause);assert change<.5
ref=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'public/audio/punto-ciego-full.wav'),'-f','f32le','-']),np.float32)
out=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-map','0:a:0','-f','f32le','-']),np.float32)
n=min(len(ref),len(out));corr=float(np.corrcoef(ref[:n],out[:n])[0,1]);assert corr>.999
assert np.max(np.abs(out[round(10.9*44100):round(14.7*44100)]))<.001
src=R/'public/audio/punto-ciego-narracion-original.mp3';assert hashlib.sha256(src.read_bytes()).hexdigest()=='05e542237413c0c80517bca585b8b844563d38141935eb19dd34d4d620f23053'
# A regression check for coverage in actual sequential rendering, not only stills.
rawfield=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','select=eq(n\\,1707),scale=540:960','-fps_mode','passthrough','-frames:v','1','-pix_fmt','rgb24','-f','rawvideo','-'])
field=np.frombuffer(rawfield,np.uint8).reshape(960,540,3)
coverage=float(field[625:643,350:390].mean()/field[625:643,250:290].mean());assert coverage>.9,coverage
# Decode entire file independently, fail on any codec error.
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(movie),'-f','null','-'],check=True)
report={'width':1080,'height':1920,'fps':30,'frames':1898,'videoDuration':v['duration'],'audioDuration':a['duration'],'originalNarrationUnchanged':True,'audioCorrelation':corr,'experimentalFramesChecked':427,'markerCenters':centers[0],'markerBoundsPx':bounds[0],'markerPositionVariationPx':float(np.max(np.ptp(np.array(centers),axis=0))),'pauseFramesChecked':120,'pauseMaxMeanPixelDifference':change,'sourceMP3Unchanged':True,'binocularCoverageLuminanceRatio':coverage,'fullDecodePassed':True,'physicalExperiment':'User tested and approved the original test geometry; same geometry used without modification.'}
(R/'out/blindspot-full/final-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
