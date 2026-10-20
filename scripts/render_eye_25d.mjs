import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import {existsSync,mkdirSync} from 'node:fs';

const v2=process.argv.includes('--v2');
const outDir=v2?'out/eye-2-5d-v2':'out/eye-2-5d';
const id=v2?'Eye25DTestV2':'Eye25DTest';
for(const name of ['source','lashes','cornea','iris','cornea-alpha',...(v2?['v2/pupil']:[])]){
  if(!existsSync(`public/eye-2-5d/${name}.png`))throw new Error(`Missing image layer: ${name}`);
}
mkdirSync(outDir,{recursive:true});
const serveUrl=await bundle({entryPoint:v2?'src/eye-2-5d/v2/index.tsx':'src/eye-2-5d/index.tsx'});
const browserExecutable='/usr/bin/chromium';
const composition=await selectComposition({serveUrl,id,browserExecutable});
if(process.argv.includes('--stills')){
  for(const frame of v2?[0,55,105,132,149]:[0,74,149]){
    await renderStill({serveUrl,composition,browserExecutable,frame,imageFormat:'png',output:`${outDir}/review-${frame}.png`});
    console.log('REVIEW_FRAME',frame);
  }
}else{
  let last=-1;
  await renderMedia({serveUrl,composition,browserExecutable,outputLocation:v2?'deliverables/eye-2-5d-test-v2.mp4':'deliverables/eye-2-5d-test.mp4',codec:'h264',crf:15,pixelFormat:'yuv420p',muted:true,concurrency:2,onProgress:p=>{
    const step=Math.floor(p.renderedFrames/30);if(step!==last){last=step;console.log('Eye 2.5D',p.renderedFrames,'/150');}
  }});
  console.log('EYE_25D_MP4_READY');
}
