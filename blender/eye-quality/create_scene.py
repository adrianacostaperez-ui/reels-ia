"""Native Cycles human-eye macro. Real millimetre geometry, no Three.js."""
import bpy,bmesh,math,random,sys,argparse,time,json
from pathlib import Path
from mathutils import Vector,Matrix
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[1];OUT=ROOT/'out/blender-eye';OUT.mkdir(exist_ok=True,parents=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--scale',type=int,default=50);ap.add_argument('--samples',type=int,default=32);ap.add_argument('--frame',type=int,default=75);a=ap.parse_args(args)
random.seed(50818);rng=np.random.default_rng(50818)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.materials):bpy.data.materials.remove(d)
S=bpy.context.scene;S.render.engine='CYCLES';S.cycles.device='CPU';S.cycles.samples=64;S.cycles.use_adaptive_sampling=True;S.cycles.adaptive_threshold=.018;S.cycles.adaptive_min_samples=16;S.cycles.use_denoising=True;S.cycles.denoiser='OPENIMAGEDENOISE';S.cycles.seed=5892;S.cycles.use_animated_seed=False
S.cycles.max_bounces=8;S.cycles.diffuse_bounces=2;S.cycles.glossy_bounces=3;S.cycles.transmission_bounces=6;S.cycles.caustics_reflective=False;S.cycles.caustics_refractive=False;S.cycles.transparent_max_bounces=8;S.cycles.sample_clamp_indirect=3
S.render.threads_mode='FIXED';S.render.threads=5;S.render.use_persistent_data=True
S.render.resolution_x=1080;S.render.resolution_y=1920;S.render.resolution_percentage=100;S.render.fps=30;S.frame_start=1;S.frame_end=150
S.render.image_settings.file_format='PNG';S.render.image_settings.color_depth='16';S.render.film_transparent=False
S.view_settings.view_transform='AgX';S.view_settings.look='AgX - Medium High Contrast';S.view_settings.exposure=-.8
# OIDN is integrated in the official Cycles build; no auxiliary EXR pass required.
W=bpy.data.worlds.new('Black studio');S.world=W;W.use_nodes=True;W.node_tree.nodes['Background'].inputs['Color'].default_value=(.002,.003,.006,1);W.node_tree.nodes['Background'].inputs['Strength'].default_value=.035

def material(name,color,rough=.4,sub=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes.get('Principled BSDF');n.inputs['Base Color'].default_value=(*color,1);n.inputs['Roughness'].default_value=rough
 if sub:n.inputs['Subsurface Weight'].default_value=sub;n.inputs['Subsurface Radius'].default_value=(1,.42,.22);n.inputs['Subsurface Scale'].default_value=.0007
 return m,n

def mesh(name,v,f,mat,uv=None):
 g=bpy.data.meshes.new(name);g.from_pydata(v,[],f);g.update();o=bpy.data.objects.new(name,g);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 for p in g.polygons:p.use_smooth=True
 if uv:
  u=g.uv_layers.new(name='UVMap')
  for p in g.polygons:
   for li in p.loop_indices:u.data[li].uv=uv[g.loops[li].vertex_index]
 # Parametric rings duplicate their 0/2pi vertices for UVs. Weld the geometry
 # after assigning loop UVs so smooth normals do not leave a radial seam.
 bm=bmesh.new();bm.from_mesh(g);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-9);bm.to_mesh(g);bm.free();g.update()
 return o

def tube(name,pts,radii,mat):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.resolution_u=10;c.bevel_depth=1;c.bevel_resolution=3
 sp=c.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,co,r in zip(sp.bezier_points,pts,radii):p.co=co;p.radius=r;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(mat);return o

def texture(m,filename,noncolor=False):
 n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=bpy.data.images.load(str(P/'assets'/filename),check_existing=True)
 if noncolor:n.image.colorspace_settings.name='Non-Color'
 return n

# Sclera: soft scattering, fine capillaries and non-uniform wet surface.
sclera,bs=material('Sclera | capillaries and collagen',(.70,.67,.62),.23,.16)
t=texture(sclera,'sclera-color.png');sclera.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
bs.inputs['Coat Weight'].default_value=.34;bs.inputs['Coat Roughness'].default_value=.07
n=sclera.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=11500;n.inputs['Detail'].default_value=2.3
b=sclera.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.16;b.inputs['Distance'].default_value=.000015;sclera.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);sclera.node_tree.links.new(b.outputs['Normal'],bs.inputs['Normal'])
v=[];uv=[];f=[];R=.012;NN=256;MM=112;theta0=math.asin(.00615/R)
for j in range(MM+1):
 th=theta0+(math.pi-theta0)*j/MM
 for i in range(NN+1):
  ph=i/NN*2*math.pi;v.append((R*math.sin(th)*math.cos(ph),R*math.sin(th)*math.sin(ph),R*math.cos(th)));uv.append((i/NN,j/MM))
for j in range(MM):
 for i in range(NN):k=j*(NN+1)+i;f.append((k,k+NN+1,k+NN+2,k+1))
globe=mesh('Scleral globe',v,f,sclera,uv);solid=globe.modifiers.new('Real scleral tissue thickness','SOLIDIFY');solid.thickness=.00045;solid.offset=-1

# Iris: 110k vertices of curved stroma with real crypt depressions.
iris,bs=material('Iris | layered stroma PBR',(.25,.36,.35),.43)
t=texture(iris,'iris-color.png');iris.node_tree.links.new(t.outputs['Color'],bs.inputs['Base Color'])
h=texture(iris,'iris-height.png',True);b=iris.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.26;b.inputs['Distance'].default_value=.00005;iris.node_tree.links.new(h.outputs['Color'],b.inputs['Height']);iris.node_tree.links.new(b.outputs['Normal'],bs.inputs['Normal'])
noise=iris.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2400;noise.inputs['Detail'].default_value=3.0
rough=iris.node_tree.nodes.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.34;rough.inputs['To Max'].default_value=.52;iris.node_tree.links.new(noise.outputs['Fac'],rough.inputs['Value']);iris.node_tree.links.new(rough.outputs['Result'],bs.inputs['Roughness'])
v=[];uv=[];f=[];NN=1152;MM=96
crypts=[(float(rng.uniform(0,math.tau)),float(rng.choice([.34,.56,.78])),float(rng.uniform(.008,.025))) for _ in range(65)]
for j in range(MM+1):
 u=j/MM
 for i in range(NN+1):
  ph=i/NN*math.tau;ri=.0020+.000012*math.sin(ph*71)+.000009*math.sin(ph*113);r=ri+u*(.00606-ri)
  relief=(.000007*math.sin(ph*239+math.sin(u*32)*1.3)+.000004*math.sin(ph*449+u*42))*math.sin(u*math.pi)
  crypt=0
  for ca,cr,cw in crypts:
   da=(ph-ca+math.pi)%math.tau-math.pi
   if abs(da)<cw*3 and abs(u-cr)<.12:crypt-=.000045*math.exp(-.5*((da/cw)**2+((u-cr)/.045)**2))
  z=.01036+.00013*(1-u)+.000045*math.sin(u*math.pi*3)+relief+crypt
  v.append((r*math.cos(ph),r*math.sin(ph),z));uv.append((.5+r*math.cos(ph)/.0123,.5+r*math.sin(ph)/.0123))
for j in range(MM):
 for i in range(NN):k=j*(NN+1)+i;f.append((k,k+NN+1,k+NN+2,k+1))
mesh('Iris stroma with crypt geometry',v,f,iris,uv)
# Narrow limbus and the frilled pupillary margin are separate anatomical layers.
limbus,bs=material('Limbus | translucent dark grey',(.025,.037,.035),.29,.08)
pupilmat,bs=material('Pupil interior | light absorption',(.0003,.0004,.0005),1)
bpy.ops.mesh.primitive_uv_sphere_add(segments=80,ring_count=48,radius=.004,location=(0,0,.005));pupil=bpy.context.object;pupil.name='Dark pupil cavity';pupil.data.materials.append(pupilmat)
for p in pupil.data.polygons:p.use_smooth=True
# Radially irregular edge just outside the true aperture.
pts=[]
for i in range(300):
 a0=i/299*math.tau;r=.002015+.000015*math.sin(a0*71);pts.append((r*math.cos(a0),r*math.sin(a0),.01050))
tube('Pupillary frill',pts,[.000035]*len(pts),limbus)

# Cornea: real refracting interface, anterior bulge with wet tear film.
cornea=bpy.data.materials.new('Cornea | transparent IOR 1.376');cornea.use_nodes=True;ns=cornea.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');glass=ns.new('ShaderNodeBsdfGlass');glass.inputs['Color'].default_value=(.995,.998,1,1);glass.inputs['Roughness'].default_value=.009;glass.inputs['IOR'].default_value=1.376;cornea.node_tree.links.new(glass.outputs['BSDF'],out.inputs['Surface'])
v=[];uv=[];f=[];NN=256;MM=96;CR=.0078;cz=.00550;thmax=math.asin(.0062/CR)
for j in range(MM+1):
 th=thmax*j/MM
 for i in range(NN+1):ph=i/NN*math.tau;v.append((CR*math.sin(th)*math.cos(ph),CR*math.sin(th)*math.sin(ph),cz+CR*math.cos(th)));uv.append((i/NN,j/MM))
for j in range(MM):
 for i in range(NN):k=j*(NN+1)+i;f.append((k,k+NN+1,k+NN+2,k+1))
cornea_obj=mesh('Anterior cornea',v,f,cornea,uv);cornea_obj.visible_shadow=False

# Eyelids and adjacent skin fill the frame; eye is never an isolated ball.
skin,bs=material('Skin | pores, vascular colour, subsurface',(.27,.115,.075),.43,.12)
nd=skin.node_tree.nodes;lk=skin.node_tree.links
geom=nd.new('ShaderNodeTexCoord');coarse=nd.new('ShaderNodeTexNoise');coarse.inputs['Scale'].default_value=450;coarse.inputs['Detail'].default_value=3;lk.new(geom.outputs['Object'],coarse.inputs['Vector'])
ramp=nd.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.15;ramp.color_ramp.elements[0].color=(.21,.075,.047,1);ramp.color_ramp.elements[1].position=.85;ramp.color_ramp.elements[1].color=(.35,.17,.11,1);lk.new(coarse.outputs['Fac'],ramp.inputs['Fac'])
attr=nd.new('ShaderNodeAttribute');attr.attribute_name='lid_rim';mix=nd.new('ShaderNodeMixRGB');mix.inputs[2].default_value=(.32,.09,.075,1);lk.new(attr.outputs['Fac'],mix.inputs[0]);lk.new(ramp.outputs['Color'],mix.inputs[1]);lk.new(mix.outputs[0],bs.inputs['Base Color'])
pores=nd.new('ShaderNodeTexVoronoi');pores.inputs['Scale'].default_value=7800;lk.new(geom.outputs['Object'],pores.inputs['Vector'])
bump=nd.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.000045;lk.new(pores.outputs['Distance'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],bs.inputs['Normal'])
rough=nd.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.33;rough.inputs['To Max'].default_value=.52;lk.new(coarse.outputs['Fac'],rough.inputs['Value']);lk.new(rough.outputs[0],bs.inputs['Roughness'])

def lidpoint(th,u=0):
 x=.0124*math.cos(th);upper=math.sin(th)>=0;y=math.sin(th)*(.0060 if upper else .0048)+.0007*x/.0124
 z=math.sqrt(max(.000001,R*R-x*x-y*y))+.00013
 xx=(1-u)*x+u*.047*math.cos(th);yy=(1-u)*y+u*.050*math.sin(th)
 # Rolled rim then an orbital fold and softly receding facial surface.
 zz=(1-u)**1.6*z+u*.0065+.0007*math.exp(-((u-.035)/.027)**2)-.00038*math.exp(-((u-.105)/.025)**2)
 zz+=.00004*math.sin(th*19+u*71)*math.sin(th*7-u*38)*min(1,u*20)
 return xx,yy,zz
v=[];uv=[];f=[];NN=384;MM=90
for j in range(MM+1):
 u=j/MM
 for i in range(NN+1):th=i/NN*math.tau;v.append(lidpoint(th,u));uv.append((i/NN,u))
for j in range(MM):
 for i in range(NN):k=j*(NN+1)+i;f.append((k,k+NN+1,k+NN+2,k+1))
lid=mesh('Continuous eyelids and orbital skin',v,f,skin,uv);solid=lid.modifiers.new('Eyelid tissue volume','SOLIDIFY');solid.thickness=.0016;solid.offset=-1;attribute=lid.data.attributes.new('lid_rim','FLOAT','POINT')
for loop in lid.data.loops:
 u=lid.data.uv_layers.active.data[loop.index].uv.y
 attribute.data[loop.vertex_index].value=.55*math.exp(-u*90)
wet,bs=material('Waterline | moist mucosa',(.32,.13,.11),.16,.18);bs.inputs['Coat Weight'].default_value=.8;bs.inputs['Coat Roughness'].default_value=.035
for lower in [False,True]:
 start=math.pi if lower else 0;pts=[]
 for i in range(220):th=start+i/219*math.pi;x,y,z=lidpoint(th);pts.append((x,y,z+.00005))
 tube('Lower tear meniscus' if lower else 'Upper moist lid margin',pts,[.000075 if lower else .00009]*len(pts),wet)
# Flesh of the inner canthus, protected by the eyelids.
bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=32,radius=1,location=(-.0118,-.00055,.0030));c=bpy.context.object;c.name='Lacrimal caruncle';c.scale=(.0008,.00055,.0007);c.data.materials.append(wet)
for p in c.data.polygons:p.use_smooth=True
hair,bs=material('Eyelashes | brown keratin',(.008,.0045,.003),.36)
for lower,count in [(False,80),(True,42)]:
 for i in range(count):
  th=(i+.5)/count*math.pi+(math.pi if lower else 0)+random.uniform(-.012,.012)
  x,y,z=lidpoint(th,.003);sgn=-1 if lower else 1;length=random.uniform(.0010,.0021) if lower else random.uniform(.0016,.0033);side=math.cos(th)*.5
  pts=[(x,y,z),(x+side*length*.15,y+sgn*length*.15,z+length*.35),(x+side*length*.6,y+sgn*length*.5,z+length*.55),(x+side*length,y+sgn*length*.8,z+length*.30)]
  root=random.uniform(.000023,.000037) if not lower else random.uniform(.000014,.000024)
  tube('Lash',pts,[root,root*.77,root*.36,.0000025],hair)
# Fine vellus hairs catch the grazing key light without becoming a fur surface.
fuzz,bs=material('Fine vellus hair',(.14,.075,.04),.48)
for i in range(190):
 th=random.uniform(0,math.tau);u=random.uniform(.035,.30);x,y,z=lidpoint(th,u);length=random.uniform(.00012,.0004)
 tube('Vellus',[(x,y,z+.000015),(x+length*.3,y+length*.35,z+length*.25),(x+length*.5,y+length*.65,z+length*.3)],[.000007,.000004,.000001],fuzz)

# Physical studio sources. Large neutral key, cool grazing rims and a dark room.
def area(name,loc,power,size,color,target=(0,0,.009),shape='DISK',size_y=None):
 data=bpy.data.lights.new(name,'AREA');data.energy=power;data.color=color;data.shape=shape;data.size=size
 if size_y is not None:data.size_y=size_y
 o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Large photographic key',(-.060,.070,.040),.30,.045,(.86,.93,1),shape='RECTANGLE',size_y=.025)
area('Soft low fill',(-.070,-.030,.010),.035,.035,(.62,.75,1))
area('Blue grazing rim',(-.04,.006,.02),.025,.020,(.16,.38,1),shape='RECTANGLE',size_y=.005)
area('Violet rim',(.04,.025,.024),.020,.018,(.48,.22,1),shape='RECTANGLE',size_y=.004)
# Small white strip gives a narrow wet highlight on the cornea and tear meniscus.
area('White strip',(.060,.020,.030),.022,.006,(1,.94,.85),shape='RECTANGLE',size_y=.030)

camdata=bpy.data.cameras.new('100mm macro');cam=bpy.data.objects.new('100mm macro',camdata);bpy.context.collection.objects.link(cam);S.camera=cam;camdata.lens=100;camdata.sensor_width=18;camdata.sensor_fit='HORIZONTAL';camdata.clip_start=.001;camdata.clip_end=10
focus=bpy.data.objects.new('Focus | iris stroma',None);bpy.context.collection.objects.link(focus);focus.location=(.0005,.0002,.01135)
camdata.dof.use_dof=True;camdata.dof.focus_object=focus;camdata.dof.aperture_fstop=7.1;camdata.dof.aperture_blades=9
# Gentle physical dolly, no 2D zoom or interpolation of frozen renders.
for frame,z,x in [(1,.150,.0032),(75,.135,.0022),(150,.118,.0010)]:
 cam.location=(x,.0021,z);target=Vector((.0004,.0003,.0109));d=(target-cam.location).normalized();right=d.cross(Vector((0,1,0))).normalized();up=right.cross(d);cam.rotation_euler=Matrix((right,up,-d)).transposed().to_euler();cam.keyframe_insert(data_path='location',frame=frame);cam.keyframe_insert(data_path='rotation_euler',frame=frame)
for fc in getattr(cam.animation_data.action,'fcurves',[]):
 for kp in fc.keyframe_points:kp.interpolation='BEZIER';kp.handle_left_type='AUTO_CLAMPED';kp.handle_right_type='AUTO_CLAMPED'
# No text, overlays, diagrams, emission tricks or neon bloom.
S.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'eye-quality.blend'))
print('SCENE_READY',sum(len(o.data.polygons) for o in S.objects if o.type=='MESH'),'polygons',flush=True)
if a.preview:
 S.frame_set(a.frame);S.render.resolution_percentage=a.scale;S.cycles.samples=a.samples;S.render.filepath=str(OUT/f'preview-{a.frame}.png');t0=time.time();bpy.ops.render.render(write_still=True);print('PREVIEW_SECONDS',time.time()-t0,flush=True)
