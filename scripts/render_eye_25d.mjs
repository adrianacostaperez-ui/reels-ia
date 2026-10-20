import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import {existsSync,mkdirSync} from 'node:fs';

for(const name of ['source','lashes','cornea','iris','cornea-alpha']){
  if(!existsSync(`public/eye-2-5d/${name}.png`))throw new Error(`Missing image layer: ${name}`);
}
mkdirSync('out/eye-2-5d',{recursive:true});
const serveUrl=await bundle({entryPoint:'src/eye-2-5d/index.tsx'});
const browserExecutable='/usr/bin/chromium';
const composition=await selectComposition({serveUrl,id:'Eye25DTest',browserExecutable});
if(process.argv.includes('--stills')){
  for(const frame of [0,74,149]){
    await renderStill({serveUrl,composition,browserExecutable,frame,imageFormat:'png',output:`out/eye-2-5d/review-${frame}.png`});
    console.log('REVIEW_FRAME',frame);
  }
}else{
  let last=-1;
  await renderMedia({serveUrl,composition,browserExecutable,outputLocation:'deliverables/eye-2-5d-test.mp4',codec:'h264',crf:15,pixelFormat:'yuv420p',muted:true,concurrency:2,onProgress:p=>{
    const step=Math.floor(p.renderedFrames/30);if(step!==last){last=step;console.log('Eye 2.5D',p.renderedFrames,'/150');}
  }});
  console.log('EYE_25D_MP4_READY');
}
