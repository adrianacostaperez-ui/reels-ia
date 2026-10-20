import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setCodec('h264');
// Software WebGL also works on cloud machines without a GPU.
Config.setChromiumOpenGlRenderer('swangle');
Config.setConcurrency(2);
// Use an existing browser when supplied; otherwise Remotion manages its browser.
if (process.env.REMOTION_BROWSER_EXECUTABLE) {
  Config.setBrowserExecutable(process.env.REMOTION_BROWSER_EXECUTABLE);
}
