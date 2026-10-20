import React from 'react';
import {AbsoluteFill, Composition, Img, registerRoot, staticFile, useCurrentFrame} from 'remotion';
import {eye25d as p, gentleMove} from './config';

/** Flat photographic planes projected with slightly different depths.
 * All transforms are uniform scales + translations: no iris/lash deformation.
 * This entry imports no Three.js, Blender render, shader or generated eye.
 */
export const Eye25D = () => {
  const frame = useCurrentFrame();
  const u = gentleMove(frame / (p.frames - 1));
  const focus = gentleMove(Math.min(1, frame / 115));
  const fit = Math.max(p.width / p.sourceWidth, p.height / p.sourceHeight);
  const anchorX = (p.width - p.sourceWidth * fit) / 2 + p.pupil.x * fit;
  const anchorY = (p.height - p.sourceHeight * fit) / 2 + p.pupil.y * fit;
  const project = (depth: number): React.CSSProperties => {
    const k = fit * p.initialOverscan * (p.cameraDistance - depth) / (p.cameraDistance - depth - p.dollyDistance * u);
    const x = -p.lateralTravel * u - depth * .045 * u;
    const y = p.verticalTravel * u + depth * .012 * u;
    return {
      position:'absolute', width:p.sourceWidth, height:p.sourceHeight,
      left:anchorX - p.pupil.x, top:anchorY - p.pupil.y,
      transformOrigin:`${p.pupil.x}px ${p.pupil.y}px`,
      transform:`translate(${x * fit}px, ${y * fit}px) scale(${k})`,
    };
  };
  const imageStyle: React.CSSProperties = {position:'absolute',inset:0,width:p.sourceWidth,height:p.sourceHeight};
  return <AbsoluteFill style={{background:'#020309',overflow:'hidden'}}>
    {(['skin','lashes','cornea','iris'] as const).map(name=>{
      const plane = p.planes[name];
      const blur = plane.blurStart + (plane.blurEnd - plane.blurStart) * focus;
      return <div key={name} style={project(plane.depth)}>
        <Img src={staticFile(`eye-2-5d/${name==='skin'?'source':name}.png`)} style={{...imageStyle,filter:`blur(${blur}px)`}}/>
      </div>;
    })}
    <div style={{...project(p.planes.cornea.depth),mixBlendMode:'screen',pointerEvents:'none'}}>
      <svg width={p.sourceWidth} height={p.sourceHeight} style={{position:'absolute',inset:0}}>
        <defs>
          <mask id="ocular-surface" maskUnits="userSpaceOnUse" x={0} y={0} width={p.sourceWidth} height={p.sourceHeight}>
            <image href={staticFile('eye-2-5d/cornea-alpha.png')} width={p.sourceWidth} height={p.sourceHeight}/>
          </mask>
          <radialGradient id="softbox-light">
            <stop offset="0" stopColor="#edf5ff" stopOpacity=".065"/>
            <stop offset=".38" stopColor="#dceaff" stopOpacity=".032"/>
            <stop offset="1" stopColor="#c4daff" stopOpacity="0"/>
          </radialGradient>
        </defs>
        <g mask="url(#ocular-surface)">
          <ellipse cx={624-16*u} cy={728+7*u} rx={27} ry={52} fill="url(#softbox-light)" transform={`rotate(${-18+3*u} ${624-16*u} ${728+7*u})`}/>
        </g>
      </svg>
    </div>
  </AbsoluteFill>;
};
const Root = () => <Composition id="Eye25DTest" component={Eye25D} width={p.width} height={p.height} fps={p.fps} durationInFrames={p.frames}/>;
registerRoot(Root);
