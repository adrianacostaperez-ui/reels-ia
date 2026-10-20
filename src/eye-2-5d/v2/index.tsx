import React from 'react';
import {AbsoluteFill,Composition,Img,registerRoot,staticFile,useCurrentFrame} from 'remotion';
import {eyeV2 as p,cameraV2} from './motion';

export const Eye25DV2=()=>{
  const m=cameraV2(useCurrentFrame());
  const project=(depth:number):React.CSSProperties=>({
    position:'absolute',width:p.sourceWidth,height:p.sourceHeight,
    left:m.anchorX-p.pupil.x,top:m.anchorY-p.pupil.y,
    transformOrigin:`${p.pupil.x}px ${p.pupil.y}px`,
    transform:`translate(${m.x-depth*p.parallax*m.advance*m.fit}px, ${m.y+depth*.018*m.advance*m.fit}px) rotate(${m.roll}deg) scale(${m.scale(depth)})`,
  });
  const blur={
    skin:.18+.76*m.irisFocus+.76*m.pupilFocus+m.focusBreath,
    lashes:.12+.28*m.irisFocus+.45*m.pupilFocus+m.focusBreath,
    cornea:.12+.10*m.irisFocus+.18*m.pupilFocus,
    iris:.68-.615*m.irisFocus+.36*m.pupilFocus+m.focusBreath,
    pupil:(.68-.56*m.irisFocus)*(1-m.pupilFocus)+.02*m.pupilFocus+m.focusBreath*.3,
  };
  const reflectionX=624-25*m.advance+3.5*Math.sin(Math.PI*m.t);
  const reflectionY=728+10*m.advance+1.5*Math.sin(Math.PI*m.t);
  return <AbsoluteFill style={{background:'#020309',overflow:'hidden'}}>
    {(['skin','lashes','cornea','iris','pupil'] as const).map(name=>{
      // Inner pupil focus mask uses exactly the iris transform, including roll.
      const depth=p.depths[name==='pupil'?'iris':name];
      const image=name==='skin'?'source':name==='pupil'?'v2/pupil':name;
      return <div key={name} style={project(depth)}>
        <Img src={staticFile(`eye-2-5d/${image}.png`)} style={{position:'absolute',inset:0,width:p.sourceWidth,height:p.sourceHeight,filter:`blur(${blur[name]}px)`}}/>
      </div>;
    })}
    <div style={{...project(p.depths.reflection),mixBlendMode:'screen',pointerEvents:'none'}}>
      <svg width={p.sourceWidth} height={p.sourceHeight} style={{position:'absolute',inset:0}}>
        <defs>
          <mask id="v2-cornea" maskUnits="userSpaceOnUse" x={0} y={0} width={p.sourceWidth} height={p.sourceHeight}>
            <image href={staticFile('eye-2-5d/cornea-alpha.png')} width={p.sourceWidth} height={p.sourceHeight}/>
          </mask>
          <radialGradient id="v2-softbox">
            <stop offset="0" stopColor="#edf5ff" stopOpacity=".048"/>
            <stop offset=".38" stopColor="#dceaff" stopOpacity=".023"/>
            <stop offset="1" stopColor="#c4daff" stopOpacity="0"/>
          </radialGradient>
        </defs>
        <g mask="url(#v2-cornea)">
          <ellipse cx={reflectionX} cy={reflectionY} rx={27-2*m.advance} ry={52} fill="url(#v2-softbox)" transform={`rotate(${-18+5*m.advance} ${reflectionX} ${reflectionY})`}/>
        </g>
      </svg>
    </div>
  </AbsoluteFill>;
};
const Root=()=> <Composition id="Eye25DTestV2" component={Eye25DV2} width={p.width} height={p.height} fps={p.fps} durationInFrames={p.frames}/>;
registerRoot(Root);
