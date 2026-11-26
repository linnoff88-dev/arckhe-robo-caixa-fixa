#!/usr/bin/env python3
"""Estudo mecânico: módulo completo removível, suporte fixo em duas peças.

Executar com o Python CAD já instalado em ../robos-impressos/.venv/bin/python.
Eixos próprios: X lateral, Y para trás, Z para cima. Unidade: mm.
"""
from pathlib import Path
import json
import numpy as np
import trimesh
from manifold3d import Manifold, OpType, CrossSection, FillRule
from PIL import Image, ImageDraw, ImageFont
from skimage.measure import find_contours

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'estudo'
OUT.mkdir(exist_ok=True)


def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1-x0, y1-y0, z1-z0]).translate([x0,y0,z0])


def union(parts):
    return Manifold.batch_boolean(parts, OpType.Add)


def hole(x, z, y0, length, diameter=3.4):
    return Manifold.cylinder(length, diameter/2, diameter/2, 32).rotate([-90,0,0]).translate([x,y0,z])


def mesh(solid):
    m = solid.to_mesh()
    return trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3], np.asarray(m.tri_verts), process=True)


def cradle():
    parts = [box(-25.8,25.8,26.5,29.5,30,54)]
    for sign in [-1,1]:
        def xb(a,b,y0,y1,z0,z1):
            a,b=sorted([sign*a,sign*b]);return box(a,b,y0,y1,z0,z1)
        parts += [xb(17,25.8,-2.4,29.5,30,32.4),
                  xb(23.4,25.8,19,29.5,30,44),
                  xb(17,23.4,23.3,29.5,32.3,38),
                  xb(20.5,25.8,-2.4,0,32.3,38)]
    solid=union(parts)
    for x in [-8,8]: solid -= hole(x,43,26,5)
    return solid


def marca():
    """Letras engrossadas em 0,4 mm, relevo de 1,2 mm, afastadas da borda."""
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 200)
    bounds = font.getbbox('ARCKHÉ')
    mask = Image.new('L', (bounds[2]-bounds[0]+20,bounds[3]-bounds[1]+20), 0)
    ImageDraw.Draw(mask).text((10-bounds[0],10-bounds[1]), 'ARCKHÉ', font=font, fill=255)
    contours = find_contours(np.asarray(mask), 127.5)
    paths = [np.column_stack([c[:,1],-c[:,0]]) for c in contours]
    xy = np.vstack(paths)
    scale = 36/(xy[:,0].max()-xy[:,0].min())
    middle = (xy.min(axis=0)+xy.max(axis=0))/2
    # Área frontal do topo; texto legível de frente para o robô.
    paths = [(p-middle)*scale + [0,-6.5] for p in paths]
    outline = CrossSection(paths, FillRule.EvenOdd).simplify(0.03).offset(0.2).simplify(0.01)
    return outline.extrude(1.35).translate([0,0,4.85])


plain_base=union([box(-38,38,-18,46,0,5), box(-14,14,29.5,35.5,4.9,54)])
base=plain_base + marca()
assert base.volume() > plain_base.volume()
for x in [-8,8]: base -= hole(x,43,29,8)
head=cradle()
# Dimensões do conjunto COM carcaça: desenho oficial Waveshare, nêo placa nua.
module=box(-23,23,0,22.5,32.4,78.4)
# Área de imagem 28,12 x 28,12; centrada apenas para visualizaçêo ilustrativa.
display=box(-14.06,14.06,-0.12,0,41.34,69.46)

assembly={'base':mesh(base),'berco':mesh(head)}
print_parts={'base':assembly['base'].copy(),'berco':assembly['berco'].copy()}
# Berço apoiado pela face traseira: as paredes nascem no plano da mesa.
print_parts['berco'].apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2,[1,0,0]))
report={'status':'estudo; nêo liberado para impressêo final',
        'marca':{'texto':'ARCKHÉ','largura_nominal_mm':36,'engrossamento_contorno_por_lado_mm':0.2,'relevo_mm':1.2,'recuo_adicional_mm':4,'centro_y_mm':-6.5,'posicao':'topo frontal da base','cor':'mesmo filamento da base; sólido único'},
        'modulo_mm':[46,22.5,46], 'modulo_dimensao_fonte':'https://docs.waveshare.com/ESP32-S3-Touch-LCD-1.54#dimensions',
        'folga_lateral_por_lado_mm':0.4,'folga_traseira_mm':0.8,
        'fixacao':'2 parafusos M3 x 16 e 2 porcas M3; confirmar na bancada',
        'pecas':{},'checagens':{}}
for name,m in print_parts.items():
    m.apply_translation(-m.bounds[0])
    m.export(OUT/f'{name}-ESTUDO.stl')
    dims=m.extents
    ok=bool(m.is_watertight and m.is_volume and len(m.split())==1 and np.all(dims<=256))
    report['pecas'][name]={'malha_fechada':bool(m.is_watertight),'volume_positivo':bool(m.is_volume),
                         'corpos':len(m.split()),'dimensoes_impressao_mm':dims.round(2).tolist(),
                         'volume_cm3':round(m.volume/1000,2),'geometria_basica_ok':ok}
    assert ok, name
for name,part in [('base',base),('berco',head)]:
    vol=(part ^ module).volume()
    report['checagens'][f'interferencia_modulo_{name}_mm3']=round(vol,6)
    assert vol < 0.01
report['checagens']['interferencia_pecas_mm3']=round((base ^ head).volume(),6)
assert (base ^ head).volume() < 0.01
# Prova de que o ensaio de encaixe detecta um módulo maior que o vêo.
oversize=box(-24,24,0,22.5,32.4,78.4)
negative=(head ^ oversize).volume()
assert negative > 1
report['checagens']['negativo_modulo_largo_mm3']=round(negative,2)
for dz in [1,5,15,30,60]:
    moving=module.translate([0,0,dz])
    assert (head ^ moving).volume() < 0.01
    assert (base ^ moving).volume() < 0.01
report['checagens']['retirada_vertical_5_posicoes']='passou para envelope retangular do módulo'
# Volume de acesso USB conservador proposto: NêO substitui o plugue real.
usb=box(-8,8,2,16,7,32.4)
for name,part in [('base',base),('berco',head)]:
    v=(part ^ usb).volume();assert v<0.01
    report['checagens'][f'corredor_usb_{name}_mm3']=round(v,6)
report['limites']=['Sem teste físico ou fatiamento.',
 'Plugue USB, raio do cabo, aba de proteçêo touch, áudio e pressêo sobre o módulo precisam de conferência física.',
 'Retençêo vertical por gravidade: módulo sai por cima; nêo transportar segurando pelo módulo.',
 'Posiçêo dos microfones e do alto-falante nêo está cotada; laterais superiores ficam abertas, mas a acústica nêo foi validada.',
 'Sem análise de resistência, tombamento sob toque ou suporte do fatiador.']
(OUT/'verificacao.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
scene=trimesh.Scene()
colors={'base':[215,166,55,255],'berco':[70,80,91,255],'modulo':[236,235,228,255],'tela':[44,146,167,255]}
objects={**assembly,'modulo':mesh(module),'tela':mesh(display)}
for name,m in objects.items():
    m.visual.face_colors=colors[name];scene.add_geometry(m,node_name=name)
scene.export(OUT/'montagem-ESTUDO.glb')

# Prancha técnica raster: projeções do mesmo modelo, nêo ilustraçêo por IA.
im=Image.new('RGB',(1600,1000),'#f2f0e9');draw=ImageDraw.Draw(im)
draw.text((35,25),'ROBO CAIXA FIXA - ESTUDO MECANICO 01',fill='#18232c',font_size=30)
draw.text((35,70),'Modulo completo removivel / 2 pecas impressas / 2 parafusos / sem motores',fill='#33434b',font_size=21)

def render(origin,scale,rotation,label):
    R=np.asarray(rotation,float);faces=[]
    for name,m in objects.items():
        vv=np.asarray(m.vertices)@R.T
        for face in m.faces:
            points=vv[face]
            normal=np.cross(points[1]-points[0],points[2]-points[0]); norm=np.linalg.norm(normal)
            shade=0.75+0.25*abs(normal[2]/norm) if norm else 1
            col=tuple(int(c*shade) for c in colors[name][:3])
            xy=[(origin[0]+p[0]*scale,origin[1]-p[1]*scale) for p in points]
            faces.append((float(points[:,2].mean()),xy,col))
    for _,xy,col in sorted(faces,key=lambda f:f[0]):draw.polygon(xy,fill=col)
    draw.text((origin[0]-130,origin[1]+90),label,fill='#25343d',font_size=20)

render((300,650),5,[[1,0,0],[0,0,1],[0,-1,0]],'FRENTE / altura 78,4 mm')
render((825,650),5,[[0,1,0],[0,0,1],[1,0,0]],'LADO / base 64 mm')
render((1280,650),4,[[0.866,0.5,0],[-0.25,0.433,0.866],[0.433,-0.75,0.5]],'PERSPECTIVA')
draw.text((35,865),'TAMANHO DO MODULO: 46 x 46 x 22,5 mm (Waveshare) / base: 76 x 64 mm',fill='#25343d',font_size=22)
draw.text((35,905),'ESTUDO: verificar encaixe, cabo USB, audio e estabilidade antes da impressao final.',fill='#8b3c22',font_size=21)
im.save(OUT/'prancha-ESTUDO.png')
print(json.dumps(report,ensure_ascii=False,indent=2))
