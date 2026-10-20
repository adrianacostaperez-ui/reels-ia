import {bundle} from '@remotion/bundler';
import {selectComposition,renderMedia} from '@remotion/renderer';
import {existsSync} from 'node:fs';
for(let i=1;i<=150;i++){if(!existsSync(`public/blender-eye/frames/${String(i).padStart(4,'0')}.png`))throw new Error(`Missing Blender/interpolated frame ${i}`);}
const serveUrl=await bundle({entryPoint:'src/blender-eye/index.tsx'});
const browserExecutable='/usr/bin/chromium';
const composition=await selectComposition({serveUrl,id:'BlenderEyeQualityTest',browserExecutable});
await renderMedia({serveUrl,composition,browserExecutable,outputLocation:'deliverables/blender-eye-quality-test.mp4',codec:'h264',crf:16,pixelFormat:'yuv420p',muted:true,concurrency:2,onProgress:p=>{if(p.renderedFrames%30===0)console.log('2D export',p.renderedFrames,'/150');}});
console.log('BLENDER_EYE_MP4_READY');
