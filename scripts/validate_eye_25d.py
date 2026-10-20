"""Validate actual encoded output, source preservation and stable pupil motion."""
from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image
from scipy.ndimage import label

R=Path(__file__).resolve().parents[1]
SOURCE=R/'public/eye-2-5d/source.png'
EXPECTED='1767b8c9ed6cf6d40f4350c87813266ffcf5123fc7bb4a4a4385a04471a8c690'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
original=np.asarray(Image.open(SOURCE).convert('RGB'))
for name in ['lashes','cornea','iris']:
    pixels=np.asarray(Image.open(R/f'public/eye-2-5d/{name}.png').convert('RGBA'))
    assert np.array_equal(pixels[:,:,:3],original),name

video=R/'deliverables/eye-2-5d-test.mp4'
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
streams=info['streams'];assert len(streams)==1 and streams[0]['codec_type']=='video'
v=streams[0];assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',150)
assert abs(float(info['format']['duration'])-5)<.001
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','scale=540:960,format=gray','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(150,960,540)
assert min(float(im.std()) for im in frames)>20
measure=[]
for im in frames:
    region=im[400:490,290:380]
    components,count=label(region<18)
    sizes=np.bincount(components.ravel());sizes[0]=0
    idx=int(sizes.argmax());mass=int(sizes[idx]);assert 700<mass<3500,mass
    yy,xx=np.nonzero(components==idx);cx=float(xx.mean());cy=float(yy.mean())
    eig=np.linalg.eigvalsh(np.cov(np.stack([xx,yy])))
    measure.append([cx+290,cy+400,mass,float(np.sqrt(eig[-1]/eig[0]))])
m=np.asarray(measure)
motion={'pupilAreaGrowth':float(m[-1,2]/m[0,2]),'maximumCenterStepPxAt540':float(np.linalg.norm(np.diff(m[:,:2],axis=0),axis=1).max()),'pupilAxisRatioVariation':float(np.ptp(m[:,3]))}
assert 1.15<motion['pupilAreaGrowth']<1.5,motion
assert motion['maximumCenterStepPxAt540']<.8,motion
assert motion['pupilAxisRatioVariation']<.1,motion
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
report={'file':str(video.relative_to(R)),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration':5,'dimensions':[1080,1920],'fps':30,'frames':150,'audioStreams':0,'sourceSha256':EXPECTED,'originalSourceUnchanged':True,'layerRGBMatchesSource':True,'technique':'Remotion photographic 2.5D planes, rigid uniform transforms, focus and optical light pass','generatedReplacementEye':False,'blender':False,'threeJS':False,'opticalFlow':False,'fullDecodePassed':True,'motionChecks':motion}
(R/'src/eye-2-5d/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
