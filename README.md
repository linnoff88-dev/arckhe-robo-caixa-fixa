# RobÃ´ caixa fixa

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="48" />
  <p><strong>Arckhé AI</strong></p>
</div>


[![RobÃ´ caixa fixa](guia/assets/banner.jpg)](https://inematds.github.io/robo-caixa-fixa/guia/)

**[PortuguÃªs](README.md) Â· [English](README.en.md) Â· [EspaÃ±ol](README.es.md)**

## O que Ã©

Quem quer um robÃ´ de mesa costuma esbarrar na parte mecÃ¢nica: servos, engrenagens e fios. O RobÃ´ caixa fixa Ã© um suporte impresso em 3D que transforma o mÃ³dulo Waveshare ESP32-S3 com tela de 1,54 polegadas numa cabeÃ§a fixa sobre uma base. O mÃ³dulo fica inteiro, com carcaÃ§a e eletrÃ´nica de fÃ¡brica. VocÃª precisa de uma impressora 3D, do Bambu Studio, de filamento, do mÃ³dulo e de dois parafusos com porca. O desenho foi conferido no computador, mas ainda nÃ£o foi impresso. O rosto na tela e a conversa por IA ainda nÃ£o existem: este guia cobre sÃ³ o suporte.

## Guia e downloads

**https://inematds.github.io/robo-caixa-fixa/guia/**

O guia tem os STL, pacote ZIP, montagem 3D, verificaÃ§Ãµes e passo a passo de fatiamento para a A1. Comece pelo berÃ§o. Os arquivos sÃ£o de estudo e ainda nÃ£o foram validados fisicamente; nÃ£o hÃ¡ G-code nem perfil 3MF validado.

## O processo, do inÃ­cio ao fim

Quem faz: ðŸ§  sessÃ£o com o Nei Â· âš™ï¸ script Â· ðŸ¤– `claude -p`.

1. âš™ï¸ Gerar as peÃ§as e a verificaÃ§Ã£o: `../robos-impressos/.venv/bin/python cad/gerar.py` (grava `estudo/`).
2. ðŸ§  Copiar STL, GLB e `verificacao.json` de `estudo/` para `guia/downloads/` e refazer o ZIP de teste, sÃ³ quando a geometria mudar.
3. âš™ï¸ Exportar as peÃ§as montadas para o render: `../robos-impressos/.venv/bin/python scripts/exporta_partes.py <pasta>`.
4. âš™ï¸ Renderizar as imagens do guia no Blender (CPU, ~25 min): `blender -b -P scripts/render_guia.py -- <pasta> <saida>`; converter para `guia/assets/r-*.jpg` e `r-orto-*.webp`.
5. ðŸ§  Banners PT/EN/ES pelo Codex (`gerar-banner.sh` da skill projetos-landing-guia, estilos live e grade), com o render do conjunto como referÃªncia de forma; conferir o texto de cada um.
6. ðŸ§  Escrever o guia PT (`guia/index.html`); âš™ï¸ traduzir para `guia/en/` e `guia/es/` com `inema-traduz`.
7. ðŸ¤– Revisor independente; conferir 360 px, imagens e visualizador 3D por HTTP local.
8. ðŸ§  OK do Nei, commit e push; o GitHub Pages publica sozinho.
9. ðŸ§  Teste fÃ­sico do berÃ§o na A1 (pendente) antes de liberar STL finais.

## Arquivos do projeto

- [Projeto fÃ­sico](PROJETO-FISICO.md).
- [DefiniÃ§Ã£o e variantes](DEFINICAO.md).
- [Gerador CAD](cad/gerar.py).
- [VerificaÃ§Ã£o](estudo/verificacao.json).

Duas peÃ§as e dois parafusos M3 Ã— 16 com porcas, a conferir na bancada. INEMA em relevo de 1,2 mm, engrossado e recuado 4 mm. Programa do rosto e IA ficam para uma etapa futura.

## VÃ­deo do projeto

https://www.youtube.com/watch?v=BEY94Ag9BWk

---

<div align="center">
  <img src="capa/logo.svg" alt="Arckhé AI" height="32" />
  <p><strong>Arckhé AI</strong></p>
</div>