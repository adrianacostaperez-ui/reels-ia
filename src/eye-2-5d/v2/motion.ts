import {eye25d as base, gentleMove} from '../config';

export const eyeV2 = {
  ...base,
  dollyDistance: 200,
  entryDolly: 55,
  lateralTravel: 7,
  verticalTravel: 2,
  target: {x:552,y:952},
  parallax: .075,
  depths: {skin:18,lashes:10,cornea:0,iris:-10,reflection:5},
} as const;

/** A steady dolly with a slight acceleration continues through the last frame.
 * No random jitter, per-pixel warp, anisotropic scale or invented anatomy.
 */
export function cameraV2(frame:number) {
  const p=eyeV2,t=Math.max(0,Math.min(1,frame/(p.frames-1))),seconds=frame/p.fps;
  const advance=.62*t+.38*t*t;
  const align=gentleMove((t-.46)/.54);
  const entry=gentleMove((t-.71)/.29);
  const irisFocus=gentleMove((t-.035)/.365);
  const pupilFocus=gentleMove((t-.49)/.43);
  const microEnvelope=Math.sin(Math.PI*t)*(1-.65*gentleMove((t-.8)/.2));
  const microX=(.52*Math.sin(seconds*1.05+.2)+.20*Math.sin(seconds*2.35+1.1))*microEnvelope;
  const microY=(.36*Math.sin(seconds*1.18+.7)+.13*Math.sin(seconds*2.1+.1))*microEnvelope;
  const breathing=1+.00115*Math.sin(2*Math.PI*(t+.14))*Math.sin(Math.PI*t);
  const focusBreath=.012*(1+Math.sin(seconds*1.45+.6))*Math.sin(Math.PI*t);
  const fit=Math.max(p.width/p.sourceWidth,p.height/p.sourceHeight);
  const anchorX=(p.width-p.sourceWidth*fit)/2+p.pupil.x*fit;
  const anchorY=(p.height-p.sourceHeight*fit)/2+p.pupil.y*fit;
  const lateral=-p.lateralTravel*advance*fit+2.0*Math.sin(Math.PI*t)*fit;
  const vertical=p.verticalTravel*advance*fit;
  const x=lateral+(p.target.x-anchorX+p.lateralTravel*fit)*align+microX;
  const y=vertical+(p.target.y-anchorY-p.verticalTravel*fit)*align+microY;
  const dolly=p.dollyDistance*advance+p.entryDolly*entry;
  const roll=.014*Math.sin(seconds*1.38)*Math.sin(Math.PI*t);
  const scale=(depth:number)=>fit*p.initialOverscan*(p.cameraDistance-depth)/(p.cameraDistance-depth-dolly)*breathing;
  return {t,seconds,advance,align,entry,irisFocus,pupilFocus,focusBreath,fit,anchorX,anchorY,x,y,dolly,roll,scale};
}
