/** Source coordinates refer to the exact uploaded 941 × 1672 photograph. */
export const eye25d = {
  width: 1080,
  height: 1920,
  fps: 30,
  frames: 150,
  sourceWidth: 941,
  sourceHeight: 1672,
  pupil: {x: 570, y: 761},
  initialOverscan: 1.025,
  cameraDistance: 1300,
  dollyDistance: 150,
  lateralTravel: 6,
  verticalTravel: 1.8,
  // Small depth offsets: no mesh, displacement map, local warp or new anatomy.
  planes: {
    skin: {depth: 14, blurStart: 0.18, blurEnd: 1.45},
    lashes: {depth: 8, blurStart: 0.12, blurEnd: 0.7},
    cornea: {depth: 0, blurStart: 0.12, blurEnd: 0.3},
    iris: {depth: -8, blurStart: 0.68, blurEnd: 0.03},
  },
} as const;

/** C2-continuous motion: zero velocity and acceleration at either endpoint. */
export const gentleMove = (t: number) => {
  const u = Math.min(1, Math.max(0, t));
  return u * u * u * (10 + u * (-15 + 6 * u));
};
