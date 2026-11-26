ï»¿# RobêÂ´ caixa fixa

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![RobêÂ´ caixa fixa](guia/assets/banner.jpg)](https://inematds.github.io/robo-caixa-fixa/guia/)

**[PortuguêÂªs](README.md) êÂ· [English](README.en.md) êÂ· [EspaêÂ±ol](README.es.md)**

## O que êÂ©

Quem quer um robêÂ´ de mesa costuma esbarrar na parte mecêÂ¢nica: servos, engrenagens e fios. O RobêÂ´ caixa fixa êÂ© um suporte impresso em 3D que transforma o mêÂ³dulo Waveshare ESP32-S3 com tela de 1,54 polegadas numa cabeêÂ§a fixa sobre uma base. O mêÂ³dulo fica inteiro, com carcaêÂ§a e eletrêÂ´nica de fêÂ¡brica. VocêÂª precisa de uma impressora 3D, do Bambu Studio, de filamento, do mêÂ³dulo e de dois parafusos com porca. O desenho foi conferido no computador, mas ainda nêÂ£o foi impresso. O rosto na tela e a conversa por IA ainda nêÂ£o existem: este guia cobre sêÂ³ o suporte.

## Guia e downloads

**https://inematds.github.io/robo-caixa-fixa/guia/**

O guia tem os STL, pacote ZIP, montagem 3D, verificaêÂ§êÂµes e passo a passo de fatiamento para a A1. Comece pelo berêÂ§o. Os arquivos sêÂ£o de estudo e ainda nêÂ£o foram validados fisicamente; nêÂ£o hêÂ¡ G-code nem perfil 3MF validado.

## O processo, do inêÂ­cio ao fim

Quem faz: ê°Å¸Â§Â  sessêÂ£o com o Nei êÂ· ê¢Å¡â¢ê¯Â¸Â script êÂ· ê°Å¸Â¤â `claude -p`.

1. ê¢Å¡â¢ê¯Â¸Â Gerar as peêÂ§as e a verificaêÂ§êÂ£o: `../robos-impressos/.venv/bin/python cad/gerar.py` (grava `estudo/`).
2. ê°Å¸Â§Â  Copiar STL, GLB e `verificacao.json` de `estudo/` para `guia/downloads/` e refazer o ZIP de teste, sêÂ³ quando a geometria mudar.
3. ê¢Å¡â¢ê¯Â¸Â Exportar as peêÂ§as montadas para o render: `../robos-impressos/.venv/bin/python scripts/exporta_partes.py <pasta>`.
4. ê¢Å¡â¢ê¯Â¸Â Renderizar as imagens do guia no Blender (CPU, ~25 min): `blender -b -P scripts/render_guia.py -- <pasta> <saida>`; converter para `guia/assets/r-*.jpg` e `r-orto-*.webp`.
5. ê°Å¸Â§Â  Banners PT/EN/ES pelo Codex (`gerar-banner.sh` da skill projetos-landing-guia, estilos live e grade), com o render do conjunto como referêÂªncia de forma; conferir o texto de cada um.
6. ê°Å¸Â§Â  Escrever o guia PT (`guia/index.html`); ê¢Å¡â¢ê¯Â¸Â traduzir para `guia/en/` e `guia/es/` com `inema-traduz`.
7. ê°Å¸Â¤â Revisor independente; conferir 360 px, imagens e visualizador 3D por HTTP local.
8. ê°Å¸Â§Â  OK do Nei, commit e push; o GitHub Pages publica sozinho.
9. ê°Å¸Â§Â  Teste fêÂ­sico do berêÂ§o na A1 (pendente) antes de liberar STL finais.

## Arquivos do projeto

- [Projeto fêÂ­sico](PROJETO-FISICO.md).
- [DefiniêÂ§êÂ£o e variantes](DEFINICAO.md).
- [Gerador CAD](cad/gerar.py).
- [VerificaêÂ§êÂ£o](estudo/verificacao.json).

Duas peêÂ§as e dois parafusos M3 êâ 16 com porcas, a conferir na bancada. INEMA em relevo de 1,2 mm, engrossado e recuado 4 mm. Programa do rosto e IA ficam para uma etapa futura.

## VêÂ­deo do projeto

https://www.youtube.com/watch?v=BEY94Ag9BWk

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>