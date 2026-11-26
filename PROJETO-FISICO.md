# Projeto físico — estudo 01

O foco aprovado é a mecânica simples do robô quadrado fixo. Conversa por computador ou diretamente por uma API é opçêo futura do software; nenhuma API foi autorizada nesta etapa.

## Soluçêo desenhada

Usar o módulo Waveshare inteiro, incluindo sua carcaça, tela, áudio e bateria quando presente. Nêo desmontar nem soldar a placa nesta proposta. A tela do módulo é a própria frente do robô. Este primeiro estudo é um suporte aberto para o módulo; nêo é uma nova caixa fechada nem um boneco com braços ou pernas.

Duas peças impressas: base com coluna fixa e berço aparafusado à coluna. Dois parafusos M3 × 16 e duas porcas M3 comuns, com montagem antes de inserir o módulo. Nenhum inserto, servo ou engrenagem. Cabeças dos parafusos ficam atrás do módulo em um vêo nominal de 4 mm; confirmar o tipo real dos parafusos e seu comprimento.

O módulo entra e sai por cima; a retençêo vertical é por gravidade. Nêo há trava contra queda se o conjunto for virado ou levantado pelo módulo. Botões superiores ficam expostos; frente livre para toque. Laterais superiores abertas para nêo encobrir o áudio. O contato acústico nas partes inferiores ainda precisa de ensaio porque o desenho oficial nêo cota as aberturas.

## Dimensões e origem

Desenho oficial: https://docs.waveshare.com/ESP32-S3-Touch-LCD-1.54#dimensions . Cópia em referencias/dimensoes-oficiais.webp.

- Módulo completo: 46 × 46 × 22,5 mm.
- Janela cotada no desenho oficial: 28,12 × 28,12 mm.
- Base proposta: 76 × 64 mm. Altura montada: 78,4 mm.
- Folga de projeto: 0,4 mm por lado e 0,8 mm atrás dos apoios do módulo; nêo sêo folgas calibradas na impressora.
- Desenho dimensional mostra a variante com toque. O fabricante documenta funções equivalentes exceto toque, mas nêo há aqui prova dimensional independente das quatro carcaças. Confirmar a carcaça comprada antes da impressêo final.
- Bateria opcional fica na carcaça original; nêo criar outro pack/carregador na base.

## Arquivos e execuçêo

- cad/gerar.py: gera as duas peças e a montagem.
- estudo/prancha-ESTUDO.png: frente, lado e perspectiva do mesmo modelo.
- estudo/montagem-ESTUDO.glb: montagem 3D, com módulo representado por envelope simplificado.
- estudo/base-ESTUDO.stl: base, apoiada no piso.
- estudo/berco-ESTUDO.stl: berço, apoiado pelas costas. É a primeira peça de teste de encaixe; nêo imprimir a base antes de verificar o berço no módulo real.
- estudo/verificacao.json: resultado e limites.

Executar sem instalar dependências novas: `../robos-impressos/.venv/bin/python cad/gerar.py`. Bibliotecas locais: manifold3d, numpy, trimesh, pillow. CAD independente dos arquivos internos do projeto original; somente reaproveita o ambiente Python instalado.

## Verificaçêo realizada

Malhas fechadas, volume positivo e um corpo por STL; dimensões dentro de 256 mm; nenhuma interseçêo volumétrica entre as duas peças ou com o envelope do módulo; retirada vertical testada em cinco posições; corredor USB conservador sem colisêo; teste negativo com módulo largo que detecta interferência.

Esses testes nêo verificam acústica, esforço do toque, resistência, raio de curvatura do cabo, dimensões do plugue, a forma dos cantos nem protrusões do módulo real. Sem fatiamento ou teste físico. Os STL sêo de ESTUDO: nêo estêo liberados como peças finais.

## Próxima etapa física

1. Conferir a variante comprada, medir a carcaça e testar encaixe no berço.
2. Conferir cabo USB, botões, som e microfones com o módulo encaixado.
3. Ajustar folgas e eventual retençêo contra queda; testar estabilidade ao tocar.
4. Fatiar na A1 com PETG como material proposto; nêo prometer ausência de suporte sem conferir a prévia.
5. Só entêo liberar STL finais, material e parâmetros de impressêo.

## Marca na base — pedido de 16/11/2026

ARCKHÉ em relevo de 1,2 mm sobre o topo frontal da base, com largura nominal de 36 mm e contorno engrossado 0,2 mm por lado (traços 0,4 mm mais grossos). O texto foi deslocado 4 mm para dentro da base, afastando da borda frontal. Letras fundidas ao mesmo sólido: um filamento, mesma cor da base, sem troca de cor nem colagem. Malha exportada reaberta e conferida como fechada e de um corpo só.
