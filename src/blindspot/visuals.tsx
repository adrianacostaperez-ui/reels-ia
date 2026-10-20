import {useEffect, useMemo} from 'react';
import {useThree} from '@react-three/fiber';
import * as T from 'three';
import {interpolate} from 'remotion';
export type V=[number,number,number];
export const smooth=(a:number,b:number,x:number)=>{const t=T.MathUtils.clamp((x-a)/(b-a),0,1);return t*t*(3-2*t);};
export const lerp=(t:number,keys:number[],v:number[])=>interpolate(t,keys,v,{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
export function curve(points:V[]){return new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)));}
export function Tube({points,r=.012,color='#93a8d2',opacity=1,emissive=false,linear=false}:{points:V[];r?:number;color?:string;opacity?:number;emissive?:boolean;linear?:boolean}) {
  const path=useMemo(()=>{if(!linear)return curve(points);const p=new T.CurvePath<T.Vector3>();for(let i=1;i<points.length;i++)p.add(new T.LineCurve3(new T.Vector3(...points[i-1]),new T.Vector3(...points[i])));return p;},[points,linear]);
  return <mesh><tubeGeometry args={[path,40,r,6,false]}/>{emissive?<meshBasicMaterial color={color} transparent={opacity<1} opacity={opacity}/>:<meshStandardMaterial color={color} roughness={.38} transparent={opacity<1} opacity={opacity}/>}</mesh>;
}
export function Dot({at,r=.035,color='#d5f2ff',opacity=1}:{at:V;r?:number;color?:string;opacity?:number}){return <mesh position={at}><sphereGeometry args={[r,16,12]}/><meshBasicMaterial color={color} transparent={opacity<1} opacity={opacity}/></mesh>;}

export function LightTent(){
  const {gl,scene}=useThree();
  useEffect(()=>{
    const c=document.createElement('canvas');c.width=1024;c.height=512;const x=c.getContext('2d')!;
    x.fillStyle='#03050a';x.fillRect(0,0,1024,512);
    const box=(px:number,py:number,w:number,h:number,col:string)=>{x.fillStyle=col;x.fillRect(px,py,w,h);};
    box(180,70,38,320,'#c7e4ff');box(390,90,120,240,'#e8efff');box(720,80,25,330,'#8876ff');box(890,150,12,230,'#448aff');
    // Actual portrait-screen reflection in the environment, not a HUD overlay.
    box(280,140,68,135,'#2d4766');box(284,145,60,125,'#0b1529');box(291,160,43,3,'#a4c4ed');box(291,168,31,2,'#6d95ce');
    box(295,205,2,12,'#f6faff');box(290,210,12,2,'#f6faff');x.beginPath();x.arc(331,211,3,0,Math.PI*2);x.fillStyle='#fff';x.fill();
    const tex=new T.CanvasTexture(c);tex.mapping=T.EquirectangularReflectionMapping;tex.colorSpace=T.SRGBColorSpace;
    const gen=new T.PMREMGenerator(gl),env=gen.fromEquirectangular(tex);scene.environment=env.texture;
    return()=>{scene.environment=null;env.dispose();gen.dispose();tex.dispose();};
  },[gl,scene]);
  return <><ambientLight intensity={.26}/><directionalLight position={[-3,5,6]} color="#dceaff" intensity={2.5}/><pointLight position={[-3,.6,2]} color="#407fff" intensity={16}/><pointLight position={[3,1,-1]} color="#9255ff" intensity={22}/></>;
}

function irisMaps(){
  const c=document.createElement('canvas');c.width=c.height=1024;const x=c.getContext('2d')!;
  const g=x.createRadialGradient(512,512,130,512,512,512);g.addColorStop(0,'#1c2429');g.addColorStop(.28,'#9a8f68');g.addColorStop(.46,'#4e787c');g.addColorStop(.78,'#2f5365');g.addColorStop(.94,'#152b39');g.addColorStop(1,'#050b11');x.fillStyle=g;x.fillRect(0,0,1024,1024);
  let seed=1937;const rnd=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  for(let i=0;i<3000;i++){
    const a=rnd()*Math.PI*2,r0=155+rnd()*95,r1=320+rnd()*180;
    x.strokeStyle=i%3?`rgba(3,17,22,${.1+rnd()*.4})`:`rgba(159,192,190,${.06+rnd()*.28})`;x.lineWidth=.4+rnd()*2;
    x.beginPath();x.moveTo(512+Math.cos(a)*r0,512+Math.sin(a)*r0);x.bezierCurveTo(512+Math.cos(a+.025)*260,512+Math.sin(a+.025)*260,512+Math.cos(a-.012)*350,512+Math.sin(a-.012)*350,512+Math.cos(a)*r1,512+Math.sin(a)*r1);x.stroke();
  }
  const map=new T.CanvasTexture(c);map.colorSpace=T.SRGBColorSpace;map.anisotropy=4;
  return map;
}
function scleraMap(){
  const c=document.createElement('canvas');c.width=1024;c.height=512;const x=c.getContext('2d')!;x.fillStyle='#abb1bb';x.fillRect(0,0,1024,512);
  for(let i=0;i<65;i++){
    const xx=(i*167.3)%1024,yy=(i*89.2)%512;x.strokeStyle='rgba(99,52,69,.055)';x.lineWidth=.6+(i%3)*.45;
    x.beginPath();x.moveTo(xx,yy);x.bezierCurveTo(xx+18,yy-8,xx+35,yy+25,xx+65,yy+14);x.stroke();
  }
  const map=new T.CanvasTexture(c);map.colorSpace=T.SRGBColorSpace;return map;
}
function irisGeometry(){
  const n=144,m=14,vertices:number[]=[],uvs:number[]=[],ids:number[]=[];
  for(let j=0;j<=m;j++)for(let i=0;i<=n;i++){
    const a=i/n*Math.PI*2,r=.245+j/m*.475;
    const z=1.895- .19*Math.pow((r-.245)/.475,1.4)+.009*Math.sin(a*43)*Math.sin(j/m*Math.PI);
    vertices.push(Math.cos(a)*r,Math.sin(a)*r,z);uvs.push(.5+Math.cos(a)*r/1.48,.5+Math.sin(a)*r/1.48);
  }
  for(let j=0;j<m;j++)for(let i=0;i<n;i++){const a=j*(n+1)+i,b=a+n+1;ids.push(a,b,a+1,a+1,b,b+1);}
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(vertices,3));g.setAttribute('uv',new T.Float32BufferAttribute(uvs,2));g.setIndex(ids);g.computeVertexNormals();return g;
}
/** Exterior includes a recessed iris, pupil aperture and separate wet cornea.
 * The pupil is an actual hole: the entry camera can travel through it.
 */
export function PremiumEye({shellOpacity=1,scale=1}:{shellOpacity?:number;scale?:number}){
  const [iris,sclera,geo]=useMemo(()=>[irisMaps(),scleraMap(),irisGeometry()] as const,[]);
  return <group scale={scale}>
    <mesh rotation={[Math.PI/2,0,0]}><sphereGeometry args={[2,80,48,0,Math.PI*2,.43,Math.PI-.43]}/><meshPhysicalMaterial map={sclera} roughness={.29} clearcoat={1} clearcoatRoughness={.08} envMapIntensity={.5} transparent={shellOpacity<1} opacity={shellOpacity} side={T.FrontSide}/></mesh>
    <group scale={[1.16,1.16,1]}>
    <mesh geometry={geo}><meshPhysicalMaterial map={iris} bumpMap={iris} bumpScale={.025} roughness={.4} clearcoat={.15} envMapIntensity={.35} side={T.DoubleSide}/></mesh>
    <mesh position={[0,0,1.90]}><ringGeometry args={[.24,.255,96]}/><meshStandardMaterial color="#171b20" roughness={.23}/></mesh>
    <mesh position={[0,0,1.69]} scale={[.738,.738,.39]}>
      <sphereGeometry args={[1,80,48,0,Math.PI*2,0,Math.PI]}/>
      <meshPhysicalMaterial color="#b7d5ee" metalness={0} roughness={.035} clearcoat={1} clearcoatRoughness={.015} transparent opacity={.10} envMapIntensity={2.0} depthWrite={false}/>
    </mesh>
    {/* Curved wet-film reflection: a tilted portrait screen, attached to cornea. */}
    <mesh position={[0,0,1.69]} scale={[.739,.739,.391]}>
      <sphereGeometry args={[1,64,40]}/>
      <shaderMaterial transparent depthWrite={false} side={T.FrontSide} vertexShader={`varying vec3 n;varying vec3 w;void main(){vec4 p=modelMatrix*vec4(position,1.);w=p.xyz;n=normalize(mat3(modelMatrix)*normal);gl_Position=projectionMatrix*viewMatrix*p;}`} fragmentShader={`varying vec3 n;varying vec3 w;
      void main(){vec3 v=normalize(cameraPosition-w);vec3 r=reflect(-v,normalize(n));vec2 p=vec2(r.x+.45,r.y-.12);p.x+=p.y*.18;vec2 b=abs(p)-vec2(.12,.25);float rect=1.-smoothstep(-.015,.012,max(b.x,b.y));float border=rect*(1.-(1.-smoothstep(-.025,-.018,max(b.x,b.y))));float line=exp(-pow((p.y-.12)/.008,2.))*step(abs(p.x),.08);float cross=step(abs(p.x+.052),.006)*step(abs(p.y+.05),.03)+step(abs(p.y+.05),.006)*step(abs(p.x+.052),.03);float dotp=1.-smoothstep(.009,.015,length(p-vec2(.055,-.05)));float glint=pow(max(0.,dot(normalize(r),normalize(vec3(-.6,.8,.9)))),100.);float a=rect*.075+border*.16+rect*(line*.15+min(cross,1.)*.13+dotp*.15)+glint*.3;gl_FragColor=vec4(.65,.81,1.,a);}`}/>
    </mesh>
    </group>
  </group>;
}

export const disc:V=[-.56,.07,-Math.sqrt(4-.56*.56-.07*.07)];
const zAt=(x:number,y:number)=>-Math.sqrt(Math.max(.1,4-x*x-y*y));
export function retinalPoint(x:number,y:number,lift=.02):V{return [x,y,zAt(x,y)+lift];}
function cellField(){
  const positions:V[]=[];
  for(let row=0;row<25;row++)for(let col=0;col<25;col++){
    const x=-1.22+col*.102+(row%2)*.051+Math.sin(row*4.13+col*1.72)*.012,y=-1.22+row*.102+Math.cos(row*1.71+col*2.93)*.012;
    if(x*x+y*y>1.65*1.65 || Math.hypot(x-disc[0],y-disc[1])<.235)continue;
    positions.push(retinalPoint(x,y,.018));
  }
  const body=new T.InstancedMesh(new T.CylinderGeometry(.020,.027,.112,16),new T.MeshStandardMaterial({color:'#968695',roughness:.52,metalness:.02}),positions.length);
  const tips=new T.InstancedMesh(new T.CapsuleGeometry(.019,.060,6,16),new T.MeshStandardMaterial({color:'#8994aa',roughness:.35}),positions.length);
  const cone=new T.InstancedMesh(new T.ConeGeometry(.030,.13,16),new T.MeshStandardMaterial({color:'#b195b5',roughness:.42}),positions.length);
  const obj=new T.Object3D(),axis=new T.Vector3(0,1,0);
  positions.forEach((p,i)=>{
    const normal=new T.Vector3(...p).normalize().negate();obj.quaternion.setFromUnitVectors(axis,normal);obj.position.set(...p).addScaledVector(normal,.058);obj.updateMatrix();body.setMatrixAt(i,obj.matrix);
    obj.position.set(...p).addScaledVector(normal,.143);obj.updateMatrix();tips.setMatrixAt(i,obj.matrix);
    if(i%8===0){obj.position.set(...p).addScaledVector(normal,.068);obj.updateMatrix();cone.setMatrixAt(i,obj.matrix);}else{obj.scale.setScalar(0);obj.updateMatrix();cone.setMatrixAt(i,obj.matrix);obj.scale.setScalar(1);}
  });return [body,tips,cone];
}
function retinaTexture(){
  const c=document.createElement('canvas');c.width=c.height=512;const x=c.getContext('2d')!;x.fillStyle='#5d3447';x.fillRect(0,0,512,512);
  for(let i=0;i<6500;i++){const a=(i*71.9)%512,b=(i*113.3)%512;x.fillStyle=i%2?'#754657':'#4c2e40';x.fillRect(a,b,1.5,1.5);}
  const t=new T.CanvasTexture(c);t.colorSpace=T.SRGBColorSpace;return t;
}
export function Retina({t,transparent=false}:{t:number;transparent?:boolean}){
  const objects=useMemo(cellField,[]),map=useMemo(retinaTexture,[]);
  objects.forEach(o=>{const m=o.material as T.MeshStandardMaterial;m.transparent=true;m.opacity=smooth(22.15,23.15,t);});
  const vessels=useMemo(()=>Array.from({length:8},(_,i)=>{
    const sx=i%2?1:-1,sy=i<4?1:-1,k=i%4;
    return [retinalPoint(disc[0]+sx*.02,disc[1]+sy*.025,.036),retinalPoint(disc[0]+sx*.06,disc[1]+sy*.16,.036),retinalPoint(disc[0]+sx*(.19+k*.04),disc[1]+sy*.42,.036),retinalPoint(Math.max(-1.3,Math.min(1.3,disc[0]+sx*(.58+k*.1))),sy*(.80+k*.08),.036)];
  }),[]);
  return <>
    <mesh rotation={[Math.PI/2,0,0]}><sphereGeometry args={[1.997,80,48,0,Math.PI*2,.48,Math.PI-.48]}/><meshStandardMaterial map={map} bumpMap={map} bumpScale={.009} side={T.BackSide} roughness={.6} transparent={transparent} opacity={transparent?.3:1}/></mesh>
    {t>=22.15&&t<30.41||t>=32.61&&t<35.22?objects.map((o,i)=><primitive key={i} object={o}/>):null}
    {/* The disc is tissue without receptors, never a physical hole. */}
    <mesh position={[disc[0]+.005,disc[1],disc[2]+.035]} rotation={[0,.284,0]}><circleGeometry args={[.225,64]}/><meshStandardMaterial color="#a98d82" bumpMap={map} bumpScale={.003} roughness={.64} side={T.DoubleSide}/></mesh>
    {vessels.map((points,i)=><Tube key={i} points={points} r={i%3===0?.007:.0038} color={i%2?'#7a3c54':'#9b5061'}/>)}
    {t>=28.43&&t<35.22 && <mesh position={[disc[0],disc[1],disc[2]+.035]} rotation={[0,.284,0]}><ringGeometry args={[.228,.236,64]}/><meshBasicMaterial color="#84b9fb" transparent opacity={.6}/></mesh>}
  </>;
}
const nervePoints:V[]=[disc,[-.65,.04,-2.2],[-.9,.02,-2.65],[-1.35,.02,-3.05],[-1.9,.04,-3.5]];
export function OpticNerve({t}:{t:number}){
  const strands=useMemo(()=>Array.from({length:16},(_,i)=>nervePoints.map(([x,y,z],j):V=>[x+Math.sin(i*2.4)*.065,y+Math.cos(i*2.4)*.065,z+(j===0?.015:0)])),[]);
  const path=useMemo(()=>curve(nervePoints),[]),pos=path.getPoint(((t*1.2)%1));
  return <>
    <Tube points={nervePoints} r={.15} color="#ab91a2" opacity={.42}/>
    {strands.map((s,i)=><Tube key={i} points={s} r={.011} color={i%2?'#6c76c0':'#9a9fbf'}/>)}
    {t>=30.41&&t<32.61&&<Dot at={[pos.x,pos.y,pos.z]} r={.05} color="#a7dcff"/>}
  </>;
}
export function Ray({t}:{t:number}){
  const paths:V[][]=[[[1.35,.0,4.1],[0,0,1.9],disc],[[1.35,.0,4.1],[.10,0,1.9],disc],[[1.35,.0,4.1],[-.1,0,1.9],disc]];
  const phase=((t-35.22)*.8)%1;
  const packet=new T.Vector3(...paths[0][0]).lerp(new T.Vector3(...paths[0][1]),Math.min(1,phase*2));
  if(phase>=.5)packet.copy(new T.Vector3(...paths[0][1])).lerp(new T.Vector3(...disc),(phase-.5)*2);
  return <>
    {t>=35.22&&<Dot at={[packet.x,packet.y,packet.z]} r={.025} color="#c9e6ff"/>}
    {paths.map((points,i)=><Tube key={i} points={points} r={.008} color="#91c6ff" opacity={.36} emissive linear/>)}
    <Dot at={[1.35,0,4.1]} r={.06}/>
    <Dot at={[1.35,0,4.13]} r={.052}/>
    {t>=35.22&&<><Dot at={[disc[0],disc[1],disc[2]+.047]} r={.045} color="#e4efff"/><mesh position={[disc[0],disc[1],disc[2]+.046]}><ringGeometry args={[.09,.095,64]}/><meshBasicMaterial color="#8dbbff" transparent opacity={.5}/></mesh></>}
  </>;
}

export function Brain({t}:{t:number}){
  const g=useMemo(()=>{
    const geo=new T.SphereGeometry(1,144,100);const p=geo.getAttribute('position');
    for(let i=0;i<p.count;i++){
      let x=p.getX(i),y=p.getY(i),z=p.getZ(i);const a=Math.atan2(z,x),b=Math.acos(Math.max(-1,Math.min(1,y)));
      const gyri=.035*Math.sin(17*b+3*Math.sin(a*5))+.021*Math.sin(27*a+2*Math.sin(b*8));
      const r=1+gyri;x*=r*.78;y*=r*.84;z*=r*1.04;p.setXYZ(i,x,y,z);
    }geo.computeVertexNormals();return geo;
  },[]);
  return <group rotation={[.18,-.35+(t-43.14)*.08,0]}>
    <mesh position={[0,-.88,-.10]} rotation={[.2,0,0]}><capsuleGeometry args={[.10,.4,6,16]}/><meshStandardMaterial color="#81768d" roughness={.58}/></mesh>
    {[-1,1].map(s=><mesh key={s} geometry={g} position={[s*.53,0,0]} scale={[.84,1,1]}><meshPhysicalMaterial color={s<0?'#8e7f9d':'#a092aa'} roughness={.57} clearcoat={.03} envMapIntensity={.4}/></mesh>)}
  </group>;
}
