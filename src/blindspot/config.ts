/** All coordinates are output pixels in a 1080 × 1920 portrait frame.
 * Re-render after adjusting separation. Never animate these values.
 * On a 6.5 cm-wide display, 680 px corresponds to about 4.1 cm:
 * approximately 15 cm viewing distance for a 15° temporal blind spot.
 * This is a starting geometry, not a physical-device calibration.
 */
export const experiment = {
  width: 1080,
  height: 1920,
  fps: 30,
  durationInFrames: 450,
  fixationX: 190,
  separationPx: 680,
  stimulusY: 1030,
  crossSizePx: 46,
  crossStrokePx: 6,
  dotRadiusPx: 15,
  background: '#05070b',
  stimulusColor: '#f0f3fa',
  experimentStartFrame: 58,
  pauseStartFrame: 324, // Original MP3 10.8 s; word has finished, inside the natural gap.
  pauseDurationFrames: 120,
} as const;
