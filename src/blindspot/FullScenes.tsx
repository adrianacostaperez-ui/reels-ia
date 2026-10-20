import {useMemo} from 'react';
import {useThree} from '@react-three/fiber';
import * as T from 'three';
import {useCurrentFrame} from 'remotion';
import {PremiumEye,Retina,OpticNerve,Ray,Brain,LightTent,Tube,Dot,smooth,lerp,disc,type V} from './visuals';

function travel(t:number,keys:number[],values:number[]){
  if(t<=keys[0])return values[0];if(t>=keys.at(-1)!)return values.at(-1)!;
  const i=keys.findIndex(k=>k>t)-1,u=smooth(keys[i],keys[i+1],t);return T.MathUtils.lerp(values[i],values[i+1],u);
}
function setCamera(camera:T.Camera,t:number,keys:number[],positions:V[],targets:V[]){
  const axis=(a:V[],n:number)=>travel(t,keys,a.map(p=>p[n]));
  camera.position.set(axis(positions,0),axis(positions,1),axis(positions,2));camera.lookAt(axis(targets,0),axis(targets,1),axis(targets,2));
}
function Hero({t,closing=false}:{t:number;closing?:boolean}){
  const {camera}=useThree();const u=closing?smooth(58.18,62.84,t):smooth(0,1.933,t);
  camera.position.set(.65-u*.45,.32,closing?11.0-u*1.2:9.8-u*2.0);camera.lookAt(0,.30,.1);
  return <group position={[0,-.45,0]} rotation={[.03,-.13+u*.10,-.04]}><PremiumEye/></group>;
}
function Anatomy({t}:{t:number}){
  const {camera}=useThree();
  const entryKeys=[16.16,18.5,21.81,22.76,24.1,25.9,27.2,28.43,30.40];
  const eyeTargets:V[]=[[0,0,.15],[0,0,.1],[0,0,-.5],[-.05,0,-1.9],[.12,.06,-1.95],[.12,.06,-1.95],disc,disc,disc];
  if(t<30.41)setCamera(camera,t,entryKeys,[[6.2,1.1,11],[3.4,.6,9],[.06,.04,5.5],[0,.01,1.20],[.12,.06,-.55],[.12,.08,-.85],[-.40,.12,-.20],[-.45,.12,-.15],[-.46,.12,-.20]],eyeTargets);
  else if(t<32.61)setCamera(camera,t,[30.41,32.60],[[4.0,.9,-6.0],[3.5,.65,-5.5]],[[-.6,0,-1.8],[-.75,0,-1.85]]);
  else if(t<35.22)setCamera(camera,t,[32.61,35.21],[[-.40,.16,-.10],[-.45,.12,-.20]],[disc,disc]);
  else if(t<38.38)setCamera(camera,t,[35.22,38.37],[[4.8,.5,5.6],[4.1,.5,4.7]],[[-.1,0,.25],[-.2,0,-.10]]);
  else setCamera(camera,t,[38.38,41.41],[[3.4,.7,4.2],[3.0,.6,3.5]],[[-.3,0,-.25],[-.4,0,-.5]]);
  const cutaway=t<21.81||t>=30.41&&t<32.61||t>=35.22;
  return <>
    <PremiumEye shellOpacity={cutaway?.14:1}/>
    <Retina t={t} transparent={cutaway}/>
    <OpticNerve t={t}/>
    {cutaway&&<mesh><torusGeometry args={[1.99,.009,8,128]}/><meshBasicMaterial color="#516480" transparent opacity={.45}/></mesh>}
    {(t<21.81||t>=35.22)&&<Ray t={t}/>}
    <pointLight position={[.4,.3,-.6]} color="#abc7ff" intensity={1.1} distance={4}/>
    <pointLight position={[-.7,.1,-1.1]} color="#b78ddd" intensity={.22} distance={2}/>
    {/* Local photoreceptor response stops at the receptor-free disc. */}
    {t>=35.22&&t<41.41&&<Dot at={[disc[0],disc[1],disc[2]+.055]} r={.045}/>}
  </>;
}
function VisualField({missing=false,point=true}:{missing?:boolean|number;point?:boolean}){
  const uniforms=useMemo(()=>({missing:{value:typeof missing==='number'?missing:missing?1:0}}),[missing]);
  return <group>
    <mesh><planeGeometry args={[3.5,2.0,32,16]}/><shaderMaterial uniforms={uniforms} side={T.DoubleSide} vertexShader={`varying vec2 v;void main(){v=uv;vec3 p=position;p.z+=.05*sin(p.x*1.3);gl_Position=projectionMatrix*modelViewMatrix*vec4(p,1.);}`} fragmentShader={`uniform float missing;varying vec2 v;void main(){float d=length((v-vec2(.72,.5))*vec2(1.75,1.));vec3 c=vec3(.025,.042,.07);float feather=smoothstep(.13,.145,d);float hatch=step(.5,fract((v.x+v.y)*55.));vec3 h=mix(vec3(.045,.06,.09),vec3(.12,.15,.2),hatch*.4);c=mix(c,h,missing*(1.-smoothstep(.13,.145,d)));gl_FragColor=vec4(c,1.);}`}/></mesh>
    <mesh position={[-1.05,0,.06]}><boxGeometry args={[.21,.025,.014]}/><meshBasicMaterial color="#eaf3ff"/></mesh>
    <mesh position={[-1.05,0,.06]}><boxGeometry args={[.025,.21,.014]}/><meshBasicMaterial color="#eaf3ff"/></mesh>
    {point&&<Dot at={[.77,0,.06]} r={.055} color="#eaf3ff"/>}
    {missing&&<mesh position={[.77,0,.07]}><ringGeometry args={[.276,.284,96]}/><meshBasicMaterial color="#83afe1" transparent opacity={(typeof missing==='number'?missing:1)*.7}/></mesh>}
  </group>;
}
function Perception({t}:{t:number}){
  const {camera}=useThree();
  if(t<43.14){
    camera.position.set(1.1-smooth(41.41,43.14,t)*.6,.45,7);camera.lookAt(0,0,0);
    return <group rotation={[-.12,-.15,0]}><VisualField missing point={false}/></group>;
  }
  if(t<46.34){
    camera.position.set(1.3-smooth(43.14,46.34,t)*.9,.45,7.6);camera.lookAt(0,.2,0);
    return <>
      <group position={[0,-.2,0]}><Brain t={t}/></group>
      {[-1,0,1].map((n,i)=><Tube key={n} points={[[-2,n*.25,.3],[-1.5,n*.32,.8],[-.8,n*.20,1.0],[-.3,n*.10,1.1]]} r={.013} color={i%2?'#9873dd':'#7aa7dd'} emissive opacity={.55}/>)}
      {[-1,0,1].map((n,i)=><Tube key={n} points={[[.3,n*.10,1.1],[.8,n*.20,1.0],[1.5,n*.32,.8],[2,n*.25,.3]]} r={.013} color="#a8c5e9" emissive opacity={.7}/>)}
    </>;
  }
  if(t<50.34){
    const u=smooth(46.34,50.34,t);camera.position.set(.5-u*.3,.4,9.0-u*.3);camera.lookAt(0,.15,0);
    return <>
      <group position={[0,1.03,-.12]} rotation={[-.12,.04,0]}><VisualField/></group>
      <group position={[0,-1.25,.3]} rotation={[-.12,-.04,0]}><VisualField point={false} missing={1-smooth(46.7,48.0,t)}/></group>
    </>;
  }
  camera.position.set(.8,.25,10.0-smooth(50.34,52.74,t)*.4);camera.lookAt(0,.20,0);
  return <group position={[0,-.45,0]} scale={.72}><PremiumEye/></group>;
}
function FieldCoverage({left=false,opacity=1,complete=0}:{left?:boolean;opacity?:number;complete?:number}){
  const uniforms=useMemo(()=>({blindX:{value:left?.32:.68},tint:{value:new T.Color(left?'#8359d1':'#377cbc')},alpha:{value:opacity},complete:{value:complete}}),[left,opacity,complete]);
  return <mesh position={[0,-.7,left?.4:.36]}><planeGeometry args={[3.3,1.9]}/><shaderMaterial transparent depthWrite={false} uniforms={uniforms} vertexShader={`varying vec2 v;void main(){v=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`} fragmentShader={`varying vec2 v;uniform float blindX;uniform vec3 tint;uniform float alpha;uniform float complete;void main(){float d=length((v-vec2(blindX,.5))*vec2(1.65,.95));float aperture=mix(smoothstep(.16,.18,d),1.,complete);float edge=smoothstep(0.,.025,min(min(v.x,1.-v.x),min(v.y,1.-v.y)));float line=exp(-pow((v.y-.5)/.012,2.));gl_FragColor=vec4(tint+line*.35,alpha*edge*aperture*(.30+line*.45));}`}/></mesh>;
}
function Binocular({t}:{t:number}){
  const {camera}=useThree(),u=smooth(52.74,58.18,t),leftOpacity=smooth(54.93,56.2,t);
  camera.position.set(.45-u*.4,.4,9.8-u*.65);camera.lookAt(0,.2,0);
  return <>
    <group position={[-.88,1.0,0]} rotation={[0,.06,0]}><PremiumEye scale={.39}/></group>
    <group position={[.88,1.0,0]} rotation={[0,-.06,0]}><PremiumEye scale={.39}/></group>
    <FieldCoverage complete={smooth(55.6,56.8,t)}/><FieldCoverage left opacity={leftOpacity} complete={smooth(55.6,56.8,t)}/>
    <Tube points={[[-.88,.35,.6],[-.80,-.05,.6],[-.45,-.7,.6]]} r={.008} color="#5c9ed9" opacity={.45} emissive/>
    <Tube points={[[.88,.35,.6],[.8,-.05,.6],[.45,-.7,.6]]} r={.008} color="#a583dc" opacity={leftOpacity*.5} emissive/>
    {t<54.93&&<mesh position={[.594,-.7,.39]}><ringGeometry args={[.17,.18,64]}/><meshBasicMaterial color="#8bb4df" transparent opacity={.6}/></mesh>}
  </>;
}
export function FullScene(){
  const t=Math.min(useCurrentFrame()/30,62.84);
  return <><LightTent/>{t<1.934?<Hero t={t}/>:t<41.41?<Anatomy t={t}/>:t<52.74?<Perception t={t}/>:t<58.18?<Binocular t={t}/>:<Hero t={t} closing/>}</>;
}
