import {bundle} from '@remotion/bundler';
import {selectComposition,openBrowser,renderStill} from '@remotion/renderer';
import {mkdirSync,writeFileSync} from 'node:fs';
const dir='out/blindspot-full/review';mkdirSync(dir,{recursive:true});
const serveUrl=await bundle({entryPoint:'src/blindspot/full-index.tsx'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});
const composition=await selectComposition({serveUrl,id:'BlindSpotFull',puppeteerInstance:browser,browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});
const times=process.argv.slice(2).length?process.argv.slice(2).map(Number):[.8,2.4,5.5,12.5,15.5,18.5,21.9,22.4,23.5,24.9,26.8,28.9,31.4,33.9,36.5,39.5,42.3,44.5,47.4,49.5,51.5,53.7,56.7,60.7];
for(let i=0;i<times.length;i+=2){await Promise.all(times.slice(i,i+2).map(async t=>{const output=`${dir}/${t.toFixed(2)}.png`;await renderStill({serveUrl,composition,frame:Math.round(t*30),output,imageFormat:'png',scale:Number(process.env.REVIEW_SCALE||.5),puppeteerInstance:browser,browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});console.log('Reviewed frame ready',t,output);}));}
await browser.close({silent:true});writeFileSync(`${dir}/shots.json`,JSON.stringify(times));
