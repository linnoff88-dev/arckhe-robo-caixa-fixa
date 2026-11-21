#!/usr/bin/env python3
"""Exporta base e berço na posição de montagem (Z para cima) para os renders do guia.

Lê só estudo/montagem-ESTUDO.glb; não regenera os STL publicados.
Uso: ../robos-impressos/.venv/bin/python scripts/exporta_partes.py <pasta-saida>
"""
import sys
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
scene = trimesh.load(ROOT / 'estudo/montagem-ESTUDO.glb', force='scene')
for name in ['base', 'berco']:
    transform, geom = scene.graph[name]
    mesh = scene.geometry[geom].copy()
    mesh.apply_transform(transform)
    mesh.export(out / f'{name}.stl')
    print(name, mesh.bounds.round(2).tolist())
