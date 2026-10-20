"""Check the delivered MP4's stimulus geometry in EVERY experiment frame.
This validates the file, not a human's ability to see the effect on a handset.
"""
from pathlib import Path
import json,subprocess
import numpy as np
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parents[1]
movie=ROOT/'deliverables/punto-ciego-test-15s.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(movie)]))
v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',450)
assert abs(float(info['format']['duration'])-15)<.001
# The entire horizontal stimulus strip, including both markers and their gap.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','crop=1080:100:0:980,format=gray','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(450,100,1080)
centers=[];areas=[]
for i,frame in enumerate(frames[58:],58):
 lab,n=label(frame>150);assert n==2,(i,n)
 objects=find_objects(lab);cc=[];aa=[]
 for y,x in objects:
  cc.append([(x.start+x.stop-1)/2,(y.start+y.stop-1)/2+980]);aa.append(int(np.count_nonzero(lab[y,x])))
 assert np.allclose(cc,[[189.5,1029.5],[869.5,1029.5]],atol=.6),(i,cc)
 centers.append(cc);areas.append(aa)
assert np.max(np.ptp(np.array(centers),axis=0))<=1
# Decode a full-frame pause to ensure captions, background, and camera also hold.
pause=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-vf','select=gte(n\\,324),scale=270:480','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'])
pause=np.frombuffer(pause,np.uint8).reshape(-1,480,270,3)
changes=[float(np.abs(x.astype(np.float32)-pause[0].astype(np.float32)).mean()) for x in pause]
assert len(pause)==126 and max(changes)<.5
# Independent audio check: same duration / rhythm and no other sound layered.
ref=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'public/audio/punto-ciego-test-15s.wav'),'-f','f32le','-']),np.float32)
out=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-map','0:a:0','-f','f32le','-']),np.float32)
n=round(10.8*44100);corr=float(np.corrcoef(ref[:n],out[:n])[0,1]);assert corr>.999
assert np.max(np.abs(out[round(10.9*44100):15*44100]))<.001
report={'durationSeconds':15,'dimensions':[1080,1920],'fps':30,'frames':450,'experimentFramesChecked':392,'markerCenters':centers[0],'markerPositionMaxVariationPx':float(np.max(np.ptp(np.array(centers),axis=0))),'markersPresentInEveryExperimentFrame':True,'pauseFramesChecked':126,'pauseFullImageMaxMeanPixelDifference':max(changes),'audioCorrelationToUnmodifiedPreviewPCM':corr,'audioTrackDuration':a['duration'],'physicalPhoneTest':'Pending user test; not performed in this cloud environment.'}
(ROOT/'out/blindspot/video-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
