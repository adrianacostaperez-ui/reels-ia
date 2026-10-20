import {AbsoluteFill,Composition,Img,registerRoot,staticFile,useCurrentFrame} from 'remotion';

/** Blender renders every 3D source pose. Remotion handles only 2D finishing/export.
 * No Three.js / R3F / WebGL scene is imported by this entry point.
 */
export const BlenderEyeQualityTest=()=>{
  const frame=useCurrentFrame()+1;
  return <AbsoluteFill style={{background:'#000'}}>
    <Img src={staticFile(`blender-eye/frames/${String(frame).padStart(4,'0')}.png`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/>
    <AbsoluteFill style={{background:'radial-gradient(ellipse 82% 42% at 50% 51%, transparent 35%, rgba(0,0,0,.40) 68%, rgba(0,0,0,.90) 100%)',pointerEvents:'none'}}/>
  </AbsoluteFill>;
};
const Root=()=> <Composition id="BlenderEyeQualityTest" component={BlenderEyeQualityTest} width={1080} height={1920} fps={30} durationInFrames={150}/>;
registerRoot(Root);
