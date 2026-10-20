import {bundle} from '@remotion/bundler';
import {selectComposition,openBrowser,renderMedia} from '@remotion/renderer';
import {mkdirSync,writeFileSync} from 'node:fs';
mkdirSync('out/blindspot-full',{recursive:true});
const serveUrl=await bundle({entryPoint:'src/blindspot/full-index.tsx'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});
try {
 const composition=await selectComposition({serveUrl,id:'BlindSpotFull',puppeteerInstance:browser,browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});
 const patch=process.argv.includes('--binocular-patch');
 let last=0;const start=Date.now();
 await renderMedia({serveUrl,composition,puppeteerInstance:browser,browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'},outputLocation:patch?'out/blindspot-full/binocular-patch.mp4':'out/blindspot-full/video-only.mp4',frameRange:patch?[1583,1745]:undefined,codec:'h264',crf:16,pixelFormat:'yuv420p',muted:true,concurrency:3,imageFormat:'jpeg',jpegQuality:95,timeoutInMilliseconds:120000,onProgress:p=>{if(Date.now()-last>15000||p.renderedFrames===composition.durationInFrames){last=Date.now();const data={rendered:p.renderedFrames,encoded:p.encodedFrames,total:composition.durationInFrames,elapsedSeconds:Math.round((Date.now()-start)/1000)};console.log(JSON.stringify(data));writeFileSync('out/blindspot-full/render-progress.json',JSON.stringify(data));}}});
 console.log('RENDER COMPLETE');
} finally {await browser.close({silent:true});}
