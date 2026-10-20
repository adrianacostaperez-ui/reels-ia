"""Validate the actual silent MP4 and check for gross interpolation distortions."""
from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2];O=R/'out/blender-eye'
def pupil_motion(frames):
 yy,xx=np.mgrid[400:600,180:360];measure=[]
 for im in frames:
  mask=im[400:600,180:360]<10;mass=int(mask.sum());assert 3000<mass<22000,mass
  cx=float((mask*xx).sum()/mass);cy=float((mask*yy).sum()/mass)
  dx=xx-cx;dy=yy-cy;c=np.array([[(mask*dx*dx).sum(),(mask*dx*dy).sum()],[(mask*dx*dy).sum(),(mask*dy*dy).sum()]])/mass
  ev=np.linalg.eigvalsh(c);measure.append([cx,cy,mass,float(np.sqrt(ev[-1]/ev[0]))])
 m=np.array(measure);steps=np.linalg.norm(np.diff(m[:,:2],axis=0),axis=1)
 return {'pupilAreaStart':float(m[0,2]),'pupilAreaEnd':float(m[-1,2]),'pupilAreaGrowth':float(m[-1,2]/m[0,2]),'maxPupilCenterStepPxAt540':float(steps.max()),'maxPupilAxisRatio':float(m[:,3].max())}
def main():
 p=R/'deliverables/blender-eye-quality-test.mp4'
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]));v=[s for s in info['streams'] if s['codec_type']=='video'];audio=[s for s in info['streams'] if s['codec_type']=='audio']
 assert len(v)==1 and not audio
 v=v[0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',150)
 assert abs(float(info['format']['duration'])-5)<.001
 anchors=sorted((O/'anchors').glob('*.png'));assert len(anchors)==31
 for image in anchors:assert Image.open(image).size==(1080,1920)
 outframes=sorted((R/'public/blender-eye/frames').glob('*.png'));assert len(outframes)==150
 for image in outframes:assert Image.open(image).size==(1080,1920)
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf','scale=540:960,format=gray','-f','rawvideo','-'])
 images=np.frombuffer(raw,np.uint8).reshape(150,960,540);assert all(im.std()>20 for im in images)
 motion=pupil_motion(images);assert motion['pupilAreaGrowth']>1.25,motion;assert motion['maxPupilCenterStepPxAt540']<2.5,motion;assert motion['maxPupilAxisRatio']<1.25,motion
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True)
 report={'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'duration':5,'dimensions':[1080,1920],'fps':30,'outputFrames':150,'audioStreams':0,'sourceEngine':'Blender 5.2.2 LTS / Cycles CPU','pathTracedSourcePoses':31,'motionCompensatedInbetweens':True,'native150FrameRender':False,'remotionRole':'2D image assembly, restrained vignette, H.264 export; no 3D scene','fullDecodePassed':True,'motionChecks':motion}
 (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
