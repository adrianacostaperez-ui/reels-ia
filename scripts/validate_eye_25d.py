"""Validate actual encoded output, source preservation and stable pupil motion."""
from pathlib import Path
import json,hashlib,subprocess,argparse
import numpy as np
from PIL import Image
from scipy.ndimage import label

R=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--v2',action='store_true');args=parser.parse_args();v2=args.v2
SOURCE=R/'public/eye-2-5d/source.png'
EXPECTED='1767b8c9ed6cf6d40f4350c87813266ffcf5123fc7bb4a4a4385a04471a8c690'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
original=np.asarray(Image.open(SOURCE).convert('RGB'))
for name in ['lashes','cornea','iris']+(['v2/pupil'] if v2 else []):
    pixels=np.asarray(Image.open(R/f'public/eye-2-5d/{name}.png').convert('RGBA'))
    assert np.array_equal(pixels[:,:,:3],original),name

video=R/('deliverables/eye-2-5d-test-v2.mp4' if v2 else 'deliverables/eye-2-5d-test.mp4')
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video)]))
streams=info['streams'];assert len(streams)==1 and streams[0]['codec_type']=='video'
v=streams[0];assert (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==('h264',1080,1920,'30/1',150)
assert abs(float(info['format']['duration'])-5)<.001
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(video),'-vf','scale=540:960,format=gray','-f','rawvideo','-'])
frames=np.frombuffer(raw,np.uint8).reshape(150,960,540)
assert min(float(im.std()) for im in frames)>20
measure=[];center=np.array([327.5,438.0])
for im in frames:
    if v2:
        x0,y0=np.rint(center-57).astype(int);region=im[y0:y0+114,x0:x0+114]
    else:x0,y0=290,400;region=im[400:490,290:380]
    components,count=label(region<18)
    sizes=np.bincount(components.ravel());sizes[0]=0
    idx=int(sizes.argmax());mass=int(sizes[idx]);assert 700<mass<(4200 if v2 else 3500),mass
    yy,xx=np.nonzero(components==idx);cx=float(xx.mean());cy=float(yy.mean())
    eig=np.linalg.eigvalsh(np.cov(np.stack([xx,yy])))
    center=np.array([cx+x0,cy+y0]);measure.append([*center,mass,float(np.sqrt(eig[-1]/eig[0]))])
m=np.asarray(measure)
motion={'pupilAreaGrowth':float(m[-1,2]/m[0,2]),'maximumCenterStepPxAt540':float(np.linalg.norm(np.diff(m[:,:2],axis=0),axis=1).max()),'pupilAxisRatioVariation':float(np.ptp(m[:,3]))}
assert (1.35 if v2 else 1.15)<motion['pupilAreaGrowth']<(1.75 if v2 else 1.5),motion
assert motion['maximumCenterStepPxAt540']<(1.9 if v2 else .8),motion
assert motion['pupilAxisRatioVariation']<.1,motion
subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
report={'file':str(video.relative_to(R)),'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),'duration':5,'dimensions':[1080,1920],'fps':30,'frames':150,'audioStreams':0,'sourceSha256':EXPECTED,'originalSourceUnchanged':True,'layerRGBMatchesSource':True,'technique':'Remotion photographic 2.5D planes, rigid uniform transforms, focus and optical light pass','generatedReplacementEye':False,'blender':False,'threeJS':False,'opticalFlow':False,'fullDecodePassed':True,'motionChecks':motion}
if v2:
    previous=R/'deliverables/eye-2-5d-test.mp4'
    assert hashlib.sha256(previous.read_bytes()).hexdigest()=='be942b0d630d584a3b1c367002d3e976c66b9df37f735f65ef83527ac89109b4'
    report.update({'version':2,'previousMP4Unchanged':True,'focus':'iris then pupil, same rigid iris transform','endingPupilCenter1080':(m[-1,:2]*2).tolist(),'intendedEntryCenter1080':[552,952]})
    assert np.linalg.norm(m[-1,:2]-np.array([276,476]))<6,report
(R/('src/eye-2-5d/v2/validation.json' if v2 else 'src/eye-2-5d/validation.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
