import {Composition, registerRoot} from 'remotion';
import {BlindSpotTest} from './BlindSpotTest';
import {experiment} from './config';
const Root=()=> <Composition id="BlindSpotTest15s" component={BlindSpotTest} width={experiment.width} height={experiment.height} fps={experiment.fps} durationInFrames={experiment.durationInFrames}/>;
registerRoot(Root);
