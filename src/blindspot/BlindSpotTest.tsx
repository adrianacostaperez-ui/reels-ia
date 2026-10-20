import {useEffect, useMemo} from 'react';
import {AbsoluteFill, Audio, interpolate, staticFile, useCurrentFrame} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as T from 'three';
import {experiment as p} from './config';
import {captions} from './captions';

/** Only the exterior eye is built for this test: no retina, nerve or brain. */
function EyeExterior() {
  const f=useCurrentFrame();
  const {camera, gl, scene}=useThree();
  const irisGeometry=useMemo(()=>{
    const g=new T.SphereGeometry(1.558,96,40,0,Math.PI*2,0,.47);g.rotateX(Math.PI/2);
    const pos=g.getAttribute("position"),uv=g.getAttribute("uv");
    for(let i=0;i<pos.count;i++)uv.setXY(i,.5+pos.getX(i)/1.42,.5+pos.getY(i)/1.42);
    return g;
  },[]);
  const textures=useMemo(()=>{
    const canvas=document.createElement('canvas');canvas.width=1024;canvas.height=1024;
    const c=canvas.getContext('2d')!;
    const g=c.createRadialGradient(512,512,100,512,512,512);
    g.addColorStop(0,'#153b49');g.addColorStop(.32,'#608d9a');g.addColorStop(.65,'#3c697f');g.addColorStop(.90,'#193446');g.addColorStop(1,'#06131d');
    c.fillStyle=g;c.fillRect(0,0,1024,1024);
    // Seeded iris fibres are deterministic between frames and render workers.
    let seed=813;const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
    for(let i=0;i<1900;i++){
      const a=random()*Math.PI*2,r0=140+random()*90,r1=370+random()*150;
      c.strokeStyle=i%3===0?`rgba(173,203,194,${.08+random()*.22})`:`rgba(4,23,32,${.12+random()*.38})`;
      c.lineWidth=.5+random()*2.5;c.beginPath();
      c.moveTo(512+Math.cos(a)*r0,512+Math.sin(a)*r0);
      c.quadraticCurveTo(512+Math.cos(a+.012)*((r0+r1)/2),512+Math.sin(a+.012)*((r0+r1)/2),512+Math.cos(a)*r1,512+Math.sin(a)*r1);c.stroke();
    }
    const tex=new T.CanvasTexture(canvas);tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=4;
    return tex;
  },[]);
  useEffect(()=>{
    const c=document.createElement('canvas');c.width=1024;c.height=512;const ctx=c.getContext('2d')!;
    ctx.fillStyle='#05070e';ctx.fillRect(0,0,1024,512);
    ctx.fillStyle='#dbeaff';ctx.fillRect(210,50,44,330);ctx.fillRect(385,90,130,210);
    ctx.fillStyle='#647eff';ctx.fillRect(720,50,30,370);
    const t=new T.CanvasTexture(c);t.mapping=T.EquirectangularReflectionMapping;t.colorSpace=T.SRGBColorSpace;
    const gen=new T.PMREMGenerator(gl),env=gen.fromEquirectangular(t);scene.environment=env.texture;
    return()=>{scene.environment=null;env.dispose();gen.dispose();t.dispose();};
  },[gl,scene]);
  useEffect(()=>()=>textures.dispose(),[textures]);
  const u=f/57;
  camera.position.set(.4-u*.22,.15,7.7-u*.7);camera.lookAt(0,.18,0);
  return <>
    <ambientLight intensity={.35}/>
    <directionalLight position={[-3,4,5]} color="#dcecff" intensity={3.2}/>
    <pointLight position={[-3,0,2]} color="#387bff" intensity={27}/>
    <pointLight position={[3,1,0]} color="#8b52ff" intensity={32}/>
    <group position={[0,-.35,0]} rotation={[.03,-.13+u*.11,-.07]}>
      <mesh rotation={[Math.PI/2,0,0]}><sphereGeometry args={[1.55,96,64,0,Math.PI*2,.47,Math.PI-.47]}/><meshPhysicalMaterial color="#b4bbc7" roughness={.32} clearcoat={1} clearcoatRoughness={.12} envMapIntensity={.35}/></mesh>
      <mesh geometry={irisGeometry}>
        <meshPhysicalMaterial map={textures} roughness={.38} clearcoat={.8} clearcoatRoughness={.08} envMapIntensity={.45}/>
      </mesh>
      <mesh position={[0,0,1.562]}><circleGeometry args={[.235,96]}/><meshBasicMaterial color="#010309"/></mesh>
      <mesh position={[0,0,1.3]} scale={[.735,.735,.34]}>
        <sphereGeometry args={[1,80,40]}/>
        <meshPhysicalMaterial color="#dbeaff" transparent opacity={.16} roughness={.035} metalness={.1} clearcoat={1} clearcoatRoughness={.025} envMapIntensity={1.8} depthWrite={false}/>
      </mesh>
    </group>
  </>;
}

function Caption() {
  const f=useCurrentFrame();
  const cue=captions.find(c=>f>=Math.round(c.start*30)&&f<Math.round(c.end*30));
  if(!cue)return null;
  const start=Math.round(cue.start*30);
  const entrance=interpolate(f,[start,start+3],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div style={{position:'absolute',top:180,left:72,right:72,textAlign:'center',fontFamily:'Arial,sans-serif',fontSize:58,fontWeight:700,lineHeight:1.4,letterSpacing:-1.2,color:'#f5f7ff',textShadow:'0 3px 20px #000,0 1px 5px #000',transform:`translateY(${(1-entrance)*7}px)`,opacity:.65+.35*entrance}}>
    {cue.text.split(' ').map((word,i)=><span key={i}>{i>0?' ':''}<span style={word===cue.highlight?{display:'inline-block',border:'2px solid #73a9ff',borderRadius:5,background:'#153e86c4',padding:'0 10px',boxShadow:'0 0 18px #2464ef22'}:{}}>{word}</span></span>)}
  </div>;
}

/** SVG is deliberately static: no frame, transform, filter or animated props. */
function TestPlate() {
  const dotX=p.fixationX+p.separationPx;
  return <svg width={p.width} height={p.height} viewBox={`0 0 ${p.width} ${p.height}`} style={{position:'absolute',inset:0}} aria-label="Mira la cruz izquierda con el ojo derecho; punto de prueba a su derecha">
    <path d={`M ${p.fixationX-p.crossSizePx/2} ${p.stimulusY} H ${p.fixationX+p.crossSizePx/2} M ${p.fixationX} ${p.stimulusY-p.crossSizePx/2} V ${p.stimulusY+p.crossSizePx/2}`} stroke={p.stimulusColor} strokeWidth={p.crossStrokePx} fill="none"/>
    <circle cx={dotX} cy={p.stimulusY} r={p.dotRadiusPx} fill={p.stimulusColor}/>
  </svg>;
}

export function BlindSpotTest() {
  const f=useCurrentFrame(),isTest=f>=p.experimentStartFrame;
  return <AbsoluteFill style={{background:p.background}}>
    <Audio src={staticFile('audio/punto-ciego-test-15s.wav')}/>
    {!isTest && <>
      <AbsoluteFill style={{background:'radial-gradient(ellipse at 15% 52%,#10244977,transparent 65%),radial-gradient(ellipse at 90% 60%,#35134766,transparent 60%)'}}/>
      <ThreeCanvas width={1080} height={1920} camera={{fov:35,near:.1,far:30}} gl={{alpha:true,antialias:true,toneMapping:T.ACESFilmicToneMapping,toneMappingExposure:1.05}}><EyeExterior/></ThreeCanvas>
      <AbsoluteFill style={{boxShadow:'inset 0 0 140px #0007'}}/>
    </>}
    {isTest && <TestPlate/>}
    <Caption/>
    {f>=p.pauseStartFrame && <div style={{position:'absolute',top:1370,left:96,right:96,textAlign:'center',fontFamily:'Arial,sans-serif',fontSize:30,fontWeight:400,letterSpacing:.1,color:'#a4adbc'}}>Puedes pausar para probar</div>}
  </AbsoluteFill>;
}
