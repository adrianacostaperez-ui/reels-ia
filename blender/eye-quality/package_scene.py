"""Portable .blend: geometry, animation, procedural materials and packed textures."""
from pathlib import Path
import bpy
P=Path(__file__).resolve().parent;R=P.parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'out/blender-eye/eye-quality.blend'))
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.adaptive_min_samples=8;s.cycles.adaptive_threshold=.035;s.cycles.use_denoising=True;s.render.resolution_percentage=100;s.frame_set(1)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(P/'eye-quality.blend'),compress=True)
print('PACKED_BLEND_READY',flush=True)
