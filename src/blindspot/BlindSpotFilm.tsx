import {AbsoluteFill,Audio,interpolate,staticFile,useCurrentFrame} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import * as T from 'three';
import {TestPlate,Caption as ApprovedOpeningCaptions} from './BlindSpotTest';
import {experiment} from './config';
import {fullCaptions} from './full-captions';
import {FullScene} from './FullScenes';

function Captions(){
  const f=useCurrentFrame(),t=f/30;
  if(t<10.8)return <ApprovedOpeningCaptions/>;
  const c=fullCaptions.find(c=>f>=Math.round(c.start*30)&&f<Math.round(c.end*30));if(!c)return null;
  const entrance=interpolate(f,[Math.round(c.start*30),Math.round(c.start*30)+3],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
  return <div style={{position:'absolute',top:180,left:72,right:72,textAlign:'center',fontFamily:'Arial,sans-serif',fontSize:58,fontWeight:700,lineHeight:1.4,letterSpacing:-1.2,color:'#f5f7ff',textShadow:'0 3px 20px #000,0 1px 5px #000',transform:`translateY(${(1-entrance)*7}px)`,opacity:.65+.35*entrance}}>
    {c.text.split(' ').map((word,i)=><span key={i}>{i>0?' ':''}<span style={word===c.highlight?{display:'inline-block',border:'2px solid #73a9ff',borderRadius:5,background:'#153e86c4',padding:'0 10px',boxShadow:'0 0 18px #2464ef22'}:{}}>{word}</span></span>)}
  </div>;
}
function DiagramLabels(){
  const t=useCurrentFrame()/30;
  const label=t>=22.76&&t<24.48?'RETINA':t>=24.48&&t<25.90?'Fotorreceptores · células que detectan luz':t>=28.43&&t<30.41?'Salida del nervio óptico':t>=32.61&&t<35.22?'Punto ciego · sin fotorreceptores':t>=35.22&&t<41.41?'SIN SEÑAL':t>=41.41&&t<43.14?'Zona sin información · esquema':null;
  return <>
    {label&&<div style={{position:'absolute',top:1540,left:80,right:80,textAlign:'center',color:'#b2bed2',fontFamily:'Arial,sans-serif',fontSize:27,letterSpacing:1}}>{label}</div>}
    {t>=46.34&&t<50.34&&<>
      <div style={{position:'absolute',top:430,left:82,color:'#a8bbd5',fontFamily:'Arial,sans-serif',fontSize:25,letterSpacing:2}}>EN PANTALLA</div>
      <div style={{position:'absolute',top:1220,left:82,color:'#a8bbd5',fontFamily:'Arial,sans-serif',fontSize:25,letterSpacing:2}}>LO QUE PERCIBES</div>
    </>}
    {t>=52.74&&t<58.18&&<>
      <div style={{position:'absolute',top:950,left:130,color:'#8cbcea',fontFamily:'Arial,sans-serif',fontSize:24}}>OJO DERECHO</div>
      <div style={{position:'absolute',top:950,right:130,color:'#b8a0e5',fontFamily:'Arial,sans-serif',fontSize:24}}>OJO IZQUIERDO</div>
      <div style={{position:'absolute',top:1510,left:90,right:90,textAlign:'center',color:'#aab9d0',fontFamily:'Arial,sans-serif',fontSize:27}}>{t<56.8?'Campos visuales · esquema':'Información combinada'}</div>
    </>}
  </>;
}
export function BlindSpotFilm(){
  const f=useCurrentFrame(),test=f>=experiment.experimentStartFrame&&f<485;
  return <AbsoluteFill style={{background:experiment.background}}>
    <Audio src={staticFile('audio/punto-ciego-full.wav')}/>
    {test?<TestPlate/>:<>
      <AbsoluteFill style={{background:'radial-gradient(ellipse at 12% 52%,#101b3677,transparent 60%),radial-gradient(ellipse at 92% 61%,#27103c66,transparent 60%)'}}/>
      <ThreeCanvas width={1080} height={1920} camera={{fov:35,near:.025,far:80}} gl={{alpha:true,antialias:true,toneMapping:T.ACESFilmicToneMapping,toneMappingExposure:1.05}}><FullScene/></ThreeCanvas>
      <AbsoluteFill style={{boxShadow:'inset 0 0 110px #0005',pointerEvents:'none'}}/>
      <DiagramLabels/>
    </>}
    <Captions/>
    {f>=324&&f<448&&<div style={{position:'absolute',top:1370,left:96,right:96,textAlign:'center',fontFamily:'Arial,sans-serif',fontSize:30,fontWeight:400,letterSpacing:.1,color:'#a4adbc'}}>Puedes pausar para probar</div>}
  </AbsoluteFill>;
}
