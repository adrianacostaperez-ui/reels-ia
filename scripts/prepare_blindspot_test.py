"""Build only the approved 15 s preview audio, never synthesize or time-stretch.
The explanation starts at source 10.92 s (video 14.92 s), so exclude that
complete phrase from this preview instead of cutting its first word at 15 s.
"""
from pathlib import Path
import hashlib,json,subprocess
import numpy as np
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'public/audio/punto-ciego-narracion-original.mp3'
EXPECTED='05e542237413c0c80517bca585b8b844563d38141935eb19dd34d4d620f23053'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
work=ROOT/'out/blindspot';work.mkdir(exist_ok=True,parents=True)
decoded=work/'source-decoded.wav'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(SOURCE),'-c:a','pcm_s24le',str(decoded)],check=True)
a,sr=sf.read(decoded,dtype='int32',always_2d=True)
assert sr==44100 and a.shape[1]==1
cut=round(10.8*sr);result=np.zeros((15*sr,1),np.int32);result[:cut]=a[:cut]
out=ROOT/'public/audio/punto-ciego-test-15s.wav';sf.write(out,result,sr,subtype='PCM_24')
check,sr2=sf.read(out,dtype='int32',always_2d=True)
assert sr2==sr and np.array_equal(check[:cut],a[:cut]) and np.all(check[cut:]==0)
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
report={'sourceSha256':EXPECTED,'sampleRate':sr,'sourceDurationSeconds':len(a)/sr,'previewDurationSeconds':len(check)/sr,'retainedOriginalSamples':cut,'retainedSpeechPCMIdentical':True,'additionalPauseSeconds':4,'pauseVideoStart':10.8,'pauseVideoEnd':14.8,'previewTail':'Hold static plate to 15 s; do not include El punto sigue ahi, which would be cut mid-word. Full film timeline remains unchanged.','voiceRegenerated':False,'voiceStretched':False}
(work/'audio-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
