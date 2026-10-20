"""An actual headless Cycles+OIDN render is the readiness check."""
from pathlib import Path
import bpy,json,os
R=Path(__file__).resolve().parents[2];out=R/'out/blender-eye';out.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=False);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=4;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.threads_mode='FIXED';s.render.threads=5;s.render.resolution_x=128;s.render.resolution_y=128;s.render.resolution_percentage=100;s.render.filepath=str(out/'headless-cycles-oidn.png');bpy.ops.render.render(write_still=True)
p=bpy.context.preferences.addons['cycles'].preferences;p.get_devices()
r={'blenderVersion':bpy.app.version_string,'engine':s.render.engine,'device':s.cycles.device,'devices':[{'name':d.name,'type':d.type} for d in p.devices],'threads':s.render.threads,'denoiser':s.cycles.denoiser,'headlessRenderPassed':(out/'headless-cycles-oidn.png').exists(),'runtime':'official Blender Foundation bpy wheel, Python 3.13, isolated workspace environment'}
(out/'environment.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
