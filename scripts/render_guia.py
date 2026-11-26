"""Renders do guia a partir do CAD real (Blender, Cycles na CPU).

Uso:
  blender -b -P scripts/render_guia.py -- <pasta-partes> <pasta-saida> [tomada ...]

<pasta-partes> vem de scripts/exporta_partes.py (base.stl e berco.stl na posiçêo de montagem).
Base e berço sêo as malhas reais. Módulo, parafusos e porcas sêo representações simples:
o módulo é o envelope oficial 46 x 46 x 22,5 mm com cantos arredondados de 2 mm.
Nenhum texto é desenhado na imagem; legendas e cotas ficam no HTML (três idiomas).
"""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[1]
argv = sys.argv[sys.argv.index('--') + 1:]
PARTES, SAIDA = Path(argv[0]), Path(argv[1])
QUAIS = set(argv[2:])
SAIDA.mkdir(parents=True, exist_ok=True)
MM = 0.001


# ---------- cena ----------
def limpar():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = int(__import__('os').environ.get('AMOSTRAS', 512))  # este Blender nêo tem OpenImageDenoise
    sc.cycles.adaptive_threshold = 0.006
    sc.cycles.use_denoising = False
    sc.render.threads_mode = 'FIXED'
    sc.render.threads = 16
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'AgX - Medium High Contrast'
    sc.render.film_transparent = False
    w = bpy.data.worlds.new('mundo')
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.010, 0.010, 0.013, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 1.0


def material(nome, cor, rug=0.45, metal=0.0, coat=0.0, camadas=False):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*cor, 1)
    p.inputs['Roughness'].default_value = rug
    p.inputs['Metallic'].default_value = metal
    p.inputs['Coat Weight'].default_value = coat
    if camadas:  # linhas de camada de 0,2 mm, bem discretas
        tc = nt.nodes.new('ShaderNodeTexCoord')
        wave = nt.nodes.new('ShaderNodeTexWave')
        wave.wave_type = 'BANDS'
        wave.bands_direction = 'Z'
        wave.inputs['Scale'].default_value = 1 / (0.2 * MM) / 6.0
        bump = nt.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.06
        bump.inputs['Distance'].default_value = 0.00003
        nt.links.new(tc.outputs['Object'], wave.inputs['Vector'])
        nt.links.new(wave.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], p.inputs['Normal'])
    return m


def suavizar(ob, graus):
    # sombreamento por ângulo: faces planas continuam planas, sem facetas falsas
    for p in ob.data.polygons:
        p.use_smooth = True
    ob.data.use_auto_smooth = True
    ob.data.auto_smooth_angle = math.radians(graus)


def importar(caminho, nome, mat):
    bpy.ops.wm.stl_import(filepath=str(caminho))
    ob = bpy.context.selected_objects[0]
    ob.name = nome
    ob.data.transform(Matrix.Scale(MM, 4))
    ob.data.materials.append(mat)
    suavizar(ob, 30)
    return ob


def caixa(nome, x0, x1, y0, y1, z0, z1, mat, chanfro=0.0):
    bpy.ops.mesh.primitive_cube_add(size=1)
    ob = bpy.context.object
    ob.name = nome
    ob.data.transform(Matrix.Diagonal(((x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM, 1)))
    ob.location = ((x0 + x1) / 2 * MM, (y0 + y1) / 2 * MM, (z0 + z1) / 2 * MM)
    if chanfro:
        b = ob.modifiers.new('arredonda', 'BEVEL')
        b.width = chanfro * MM
        b.segments = 6
        b.limit_method = 'ANGLE'
        b.harden_normals = True
        suavizar(ob, 30)
    ob.data.materials.append(mat)
    return ob


def cilindro(nome, r, comp, mat, verts=32):
    """Cilindro já deitado no eixo Y."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r * MM, depth=comp * MM)
    ob = bpy.context.object
    ob.data.transform(Matrix.Rotation(math.radians(-90), 4, 'X'))
    ob.name = nome
    ob.data.materials.append(mat)
    return ob


def juntar(obs, nome):
    bpy.ops.object.select_all(action='DESELECT')
    for o in obs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.join()
    ob = bpy.context.object
    ob.name = nome
    return ob


def parafuso(nome, x, z, aco):
    """M3 x 16 de cabeça cilíndrica: cabeça no vêo atrás do módulo, corpo para trás (+Y)."""
    cab = cilindro(nome + '-cab', 2.75, 3.0, aco)
    cab.location = (x * MM, 24.0 * MM, z * MM)
    corpo = cilindro(nome + '-corpo', 1.5, 16.0, aco, 24)
    corpo.location = (x * MM, (25.5 + 8.0) * MM, z * MM)
    return juntar([cab, corpo], nome)


def porca(nome, x, z, aco):
    ob = cilindro(nome, 3.15, 2.4, aco, 6)
    ob.location = (x * MM, 36.7 * MM, z * MM)
    return ob


def piso(cor=(0.008, 0.008, 0.010), rug=0.5):
    bpy.ops.mesh.primitive_plane_add(size=4)
    ob = bpy.context.object
    ob.name = 'piso'
    ob.data.materials.append(material('piso', cor, rug))
    return ob


def luz(nome, loc, alvo, energia, tam, cor=(1, 1, 1)):
    d = bpy.data.lights.new(nome, 'AREA')
    d.energy = energia
    d.size = tam
    d.color = cor
    ob = bpy.data.objects.new(nome, d)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc)
    ob.rotation_euler = (Vector(alvo) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    return ob


def camera(loc, alvo, lente=70, orto=None):
    d = bpy.data.cameras.new('cam')
    if orto:
        d.type = 'ORTHO'
        d.ortho_scale = orto
    else:
        d.lens = lente
        d.dof.use_dof = False
    ob = bpy.data.objects.new('cam', d)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = Vector(loc)
    ob.rotation_euler = (Vector(alvo) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = ob
    return ob


def estudio(escala=1.0):
    k = escala
    luz('chave', (-0.20 * k, -0.26 * k, 0.24 * k), (0, 0, 0.04), 1.3 * k * k, 0.16 * k, (1.0, 0.86, 0.68))
    luz('preench', (0.26 * k, -0.18 * k, 0.10 * k), (0, 0, 0.04), 0.35 * k * k, 0.22 * k, (0.80, 0.88, 1.0))
    luz('recorte', (0.10 * k, 0.30 * k, 0.22 * k), (0, 0.01, 0.05), 1.4 * k * k, 0.10 * k, (1.0, 0.78, 0.45))


def render(nome, w, h):
    sc = bpy.context.scene
    sc.render.resolution_x = w
    sc.render.resolution_y = h
    sc.render.resolution_percentage = int(__import__('os').environ.get('PCT', 100))
    sc.render.image_settings.file_format = 'PNG'
    sc.render.filepath = str(SAIDA / f'{nome}.png')
    bpy.ops.render.render(write_still=True)
    print('RENDER', nome)


# ---------- objetos ----------
def montar(modulo=True, fixadores=True):
    mats = {
        'base': material('base', (0.80, 0.52, 0.06), 0.38, coat=0.15, camadas=True),
        'berco': material('berco', (0.045, 0.050, 0.058), 0.42, coat=0.1, camadas=True),
        'carcaca': material('carcaca', (0.80, 0.80, 0.78), 0.5),
        'tela': material('tela', (0.004, 0.005, 0.007), 0.06, coat=0.6),
        'aco': material('aco', (0.62, 0.62, 0.64), 0.28, metal=1.0),
    }
    o = {}
    o['base'] = importar(PARTES / 'base.stl', 'base', mats['base'])
    o['berco'] = importar(PARTES / 'berco.stl', 'berco', mats['berco'])
    if modulo:
        car = caixa('carcaca', -23, 23, 0, 22.5, 32.4, 78.4, mats['carcaca'], 2.0)
        tela = caixa('tela', -14.06, 14.06, -0.15, 0.4, 41.34, 69.46, mats['tela'], 0.4)
        moldura = caixa('moldura', -19.5, 19.5, -0.08, 0.4, 36.0, 74.8, mats['tela'], 1.5)
        o['modulo'] = juntar([car, moldura, tela], 'modulo')
    if fixadores:
        o['p1'] = parafuso('p1', -8, 43, mats['aco'])
        o['p2'] = parafuso('p2', 8, 43, mats['aco'])
        o['n1'] = porca('n1', -8, 43, mats['aco'])
        o['n2'] = porca('n2', 8, 43, mats['aco'])
    return o, mats


def mover(ob, dx=0, dy=0, dz=0):
    ob.location = (ob.location.x + dx * MM, ob.location.y + dy * MM, ob.location.z + dz * MM)


def esconder(ob):
    ob.hide_render = True


def quer(nome):
    return not QUAIS or nome in QUAIS


# ---------- tomadas ----------
def t_conjunto():
    limpar(); montar(); piso(); estudio()
    camera((-0.19, -0.27, 0.15), (0.0, 0.005, 0.036), 72)
    render('r-conjunto', 1600, 1200)


def t_frente():
    limpar(); montar(); piso(); estudio()
    camera((-0.06, -0.33, 0.085), (0.0, 0.0, 0.040), 78)
    render('r-frente-luz', 1600, 1200)


def t_explodida():
    limpar(); o, _ = montar(); piso(); estudio(1.3)
    mover(o['modulo'], dy=-20, dz=36)
    mover(o['berco'], dy=-20)
    for k in ['p1', 'p2']:
        mover(o[k], dy=-40)
    for k in ['n1', 'n2']:
        mover(o[k], dy=16)
    camera((-0.31, -0.16, 0.16), (0.0, -0.006, 0.052), 60)
    render('r-explodida', 1600, 1300)


def t_inema():
    limpar(); o, _ = montar(); piso()
    luz('rasante', (-0.30, -0.10, 0.03), (0, -0.006, 0.005), 0.7, 0.05, (1.0, 0.86, 0.66))
    luz('topo', (0.05, -0.12, 0.25), (0, -0.006, 0.0), 0.15, 0.2, (0.85, 0.9, 1.0))
    luz('recorte', (0.15, 0.25, 0.15), (0, 0.0, 0.03), 0.5, 0.1, (1.0, 0.8, 0.5))
    camera((0.0, -0.150, 0.075), (0.0, -0.004, 0.004), 105)
    render('r-inema', 1600, 900)


def t_costas():
    limpar(); montar(); piso(); estudio()
    camera((0.20, 0.26, 0.13), (0.0, 0.02, 0.040), 72)
    render('r-costas', 1600, 1200)


def t_passos():
    # 1: só o berço, módulo entrando por cima (teste de encaixe)
    limpar(); o, _ = montar(); piso(); estudio()
    esconder(o['base'])
    for k in ['p1', 'p2', 'n1', 'n2']:
        esconder(o[k])
    for k in ['berco', 'modulo']:
        mover(o[k], dz=-30)
    mover(o['modulo'], dz=40)
    camera((-0.19, -0.27, 0.15), (0.0, 0.008, 0.040), 70)
    render('r-passo1', 1200, 900)
    # 2: berço contra a coluna, parafusos pela frente, porcas atrás
    limpar(); o, _ = montar(); piso(); estudio()
    esconder(o['modulo'])
    mover(o['berco'], dy=-14)
    for k in ['p1', 'p2']:
        mover(o[k], dy=-34)
    for k in ['n1', 'n2']:
        mover(o[k], dy=10)
    camera((-0.24, -0.19, 0.14), (0.0, 0.008, 0.035), 72)
    render('r-passo2', 1200, 900)
    # 3: suporte pronto, módulo descendo por cima
    limpar(); o, _ = montar(); piso(); estudio()
    mover(o['modulo'], dz=30)
    camera((-0.21, -0.25, 0.17), (0.0, 0.006, 0.052), 66)
    render('r-passo3', 1200, 900)


def t_mesa():
    """As duas peças na orientaçêo dos STL publicados, na mesa de 256 mm da A1."""
    limpar()
    m_base = material('base', (0.80, 0.52, 0.06), 0.38, coat=0.15, camadas=True)
    m_berco = material('berco', (0.045, 0.050, 0.058), 0.42, coat=0.1, camadas=True)
    base = importar(ROOT / 'guia/downloads/base-ESTUDO.stl', 'base', m_base)
    berco = importar(ROOT / 'guia/downloads/berco-ESTUDO.stl', 'berco', m_berco)
    base.location = (-0.065, -0.020, 0)
    berco.location = (0.030, 0.000, 0)
    # placa texturizada escura de 256 x 256 mm
    bpy.ops.mesh.primitive_cube_add(size=1)
    placa = bpy.context.object
    placa.data.transform(Matrix.Diagonal((0.256, 0.256, 0.002, 1)))
    placa.location = (0.0, 0.013, -0.001)
    m = material('placa', (0.03, 0.03, 0.032), 0.75)
    nt = m.node_tree
    nz = nt.nodes.new('ShaderNodeTexNoise')
    nz.inputs['Scale'].default_value = 900
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.25
    nt.links.new(nz.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], nt.nodes['Principled BSDF'].inputs['Normal'])
    placa.data.materials.append(m)
    bpy.ops.mesh.primitive_plane_add(size=4, location=(0, 0, -0.0025))
    bpy.context.object.data.materials.append(material('piso', (0.012, 0.012, 0.015), 0.6))
    estudio(1.9)
    camera((-0.07, -0.42, 0.36), (-0.012, 0.01, 0.0), 64)
    render('r-mesa', 1600, 1100)


def t_orto():
    """Vistas ortográficas a 10 px/mm (1200 px = 120 mm) para as cotas em SVG no HTML."""
    for nome, loc, alvo in [
        ('r-orto-frente', (0.0, -0.5, 0.040), (0.0, 0.0, 0.040)),
        ('r-orto-lado', (0.5, 0.014, 0.040), (0.0, 0.014, 0.040)),
    ]:
        limpar(); montar(fixadores=False); estudio()
        bpy.context.scene.world.node_tree.nodes['Background'].inputs[0].default_value = (0.016, 0.016, 0.02, 1)
        luz('frontal', (loc[0] * 0.6 - 0.1, loc[1] * 0.6 - 0.05, 0.25), alvo, 10, 0.4, (1, 0.95, 0.9))
        camera(loc, alvo, orto=0.120)
        bpy.context.scene.render.film_transparent = True
        render(nome, 1200, 1200)


for nome, f in [('conjunto', t_conjunto), ('frente', t_frente), ('explodida', t_explodida),
                ('inema', t_inema), ('costas', t_costas), ('passos', t_passos),
                ('mesa', t_mesa), ('orto', t_orto)]:
    if quer(nome):
        f()
