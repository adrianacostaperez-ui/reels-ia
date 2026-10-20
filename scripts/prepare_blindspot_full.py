"""Insert only the approved four-second silence; preserve all decoded speech samples."""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
import soundfile as sf
R=Path(__file__).resolve().parents[1]
src=R/'public/audio/punto-ciego-narracion-original.mp3'
expected='05e542237413c0c80517bca585b8b844563d38141935eb19dd34d4d620f23053'
assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
out=R/'out/blindspot-full';out.mkdir(exist_ok=True,parents=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-c:a','pcm_s24le',str(out/'source.wav')],check=True)
a,sr=sf.read(out/'source.wav',dtype='int32',always_2d=True)
cut=round(10.8*sr);pause=np.zeros((4*sr,a.shape[1]),np.int32)
b=np.concatenate([a[:cut],pause,a[cut:]])
dest=R/'public/audio/punto-ciego-full.wav';sf.write(dest,b,sr,subtype='PCM_24')
c,sr2=sf.read(dest,dtype='int32',always_2d=True)
assert sr2==sr and np.array_equal(a[:cut],c[:cut]) and np.array_equal(a[cut:],c[cut+len(pause):])
assert hashlib.sha256(src.read_bytes()).hexdigest()==expected
report={'originalMp3Sha256':expected,'originalDecodedSamples':len(a),'outputSamples':len(b),'sampleRate':sr,'durationSeconds':len(b)/sr,'pauseStart':10.8,'pauseSeconds':4,'allOriginalSamplesPreserved':True,'timeStretch':False,'voiceSynthesis':False,'frames30fps':int(np.ceil(len(b)/sr*30))}
(out/'audio-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
