import {Composition,registerRoot} from 'remotion';
import {BlindSpotFilm} from './BlindSpotFilm';
const Root=()=> <Composition id="BlindSpotFull" component={BlindSpotFilm} width={1080} height={1920} fps={30} durationInFrames={1898}/>;
registerRoot(Root);
