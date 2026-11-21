# Definição inicial — 15/11/2026

## Pedido

Novo projeto, copiando o que for útil do robos-impressos, com apenas uma placa: Raspberry Pi, Arduino ou ESP32. Caixa fixa, sem movimento da cabeça.

## Escolha do Nei — 15/11/2026

Pedido literal após enviar o anúncio: “VOU USAR ESTE NA CAIXA”.

- Placa escolhida: anúncio https://pt.aliexpress.com/item/1005011874532154.html
- O HTML público do vendedor confirma o título “Placa ESP32-S3 com LCD 1.54 e IA DeepSeek”. Os nomes das imagens mencionam N16R8; essa informação ainda não foi conferida na variante escolhida.
- Uma única placa ESP32-S3 no robô, sem Raspberry Pi e sem Arduino auxiliar.
- Não é a CoreS3 Lite. Não copiar dimensões, firmware ou pinagem dela como se fossem desta placa.
- Variante com/sem toque, conteúdo do kit (microfone, falante, bateria), dimensões externas, furos, conectores e pinagem ainda não confirmados.
- A expressão “IA DeepSeek” no anúncio não comprova IA rodando na placa, serviço incluído ou funcionamento sem computador/internet. Nenhuma nuvem foi autorizada ou ativada.
- O painel original de 3,5 polegadas precisará de adaptação para a tela menor. Nenhuma dimensão de encaixe será definida a partir apenas da diagonal da tela.

## Comparação histórica para esta aplicação

| Alternativa | Uso adequado | Limite relevante |
|---|---|---|
| Raspberry Pi 4 | Tela, áudio e programas Linux no próprio robô | Exige sistema em microSD, fonte adequada e ventilação; conversa com IA depende do motor escolhido e não está pronta |
| ESP32-S3 com PSRAM | Rosto animado, captura e reprodução de áudio e Wi-Fi | Para o sistema de conversa já existente neste ecossistema, usa o computador de casa; uma placa no robô não significa sistema independente do computador |
| Arduino Uno R3 | Comandos e interações simples | Memória e recursos limitados para tela gráfica e conversa por voz; não é a recomendação para esta proposta |

ESP32 também pode ser programado pela Arduino IDE; isso não exige uma placa Arduino Uno adicional.

## Reaproveitamento

Copiados o copo e o painel do rosto em STL, e um render do robô original para referência. Os nomes e hashes estão em referencias/proveniencia.json.

O copo original tem abertura para pescoço e não inclui ventilação. O painel é dimensionado para a tela de 3,5 polegadas do Raspberry Pi. Ambos precisam de revisão antes de servir para o projeto fixo; a tela não deve ser presumida compatível com ESP32.

Não são necessários Arduino auxiliar, servos, engrenagens, garfo e articulações. Bateria, carregador e conversores serão reavaliados conforme a alimentação escolhida.

## Projetos existentes que podem fornecer software

- ../robo-cores3-lite: uma placa ESP32-S3 pronta (M5Stack CoreS3 Lite), tela, áudio e câmera. Servidor local documentado; firmware completo e placa ainda não validados juntos segundo o README consultado. Reutilização futura, sem copiar segredos nem mudar esse projeto.
- ../robo-chaveiro: outra variante ESP32-S3; não confundir sua placa e pinagem com a CoreS3 Lite.

## Decisões pendentes

1. Rosto e conversa por voz, ou apenas rosto e interações simples?
2. Precisa trabalhar sem o computador de casa? Internet e serviços externos são outra decisão.
3. Variante exata da placa ESP32-S3 escolhida, ficha dimensional e tamanho externo desejado.
4. Fonte externa ou bateria.

## Próximas entregas após escolher a arquitetura

1. Lista de componentes e dimensões confirmadas.
2. Corpo e tampa fixos, suportes, acesso aos conectores e ventilação.
3. Peça de teste e validação das malhas e montagem antes dos STL finais.
4. Programa mínimo de rosto; áudio e conversa se fizerem parte do escopo.

## Fontes consultadas

- Raspberry Pi 4: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
- ESP32-S3: https://www.espressif.com/en/products/socs/esp32-s3
- CoreS3 Lite: https://docs.m5stack.com/en/core/CoreS3-Lite
- Arduino Uno R3: https://docs.arduino.cc/hardware/uno-rev3

Nenhum serviço externo de IA autorizado ou ativado neste projeto.

## Variantes conferidas nas fotos do anúncio — 15/11/2026

A imagem original do vendedor está em referencias/variantes-anuncio.jpg; URLs e opções em referencias/placa-escolhida.json.

| Modelo na imagem do vendedor | Toque | Bateria |
|---|---|---|
| ESP32-S3-LCD-1.54-EN | Não | Não |
| ESP32-S3-LCD-1.54 | Não | Sim |
| ESP32-S3-Touch-LCD-1.54-EN | Sim | Não |
| ESP32-S3-Touch-LCD-1.54 | Sim | Sim |

Todas são anunciadas como 1,54 polegadas. A frente preta da versão com toque é maior nas imagens, mas isso não demonstra tela com área de imagem maior. O rótulo traseiro fotografado pelo vendedor declara TFT LCD de 1,54 polegadas, 240 × 240 pixels. Não deduzir dimensões de fixação dessas fotos.

O rótulo traseiro mostra WAVESHARE, QMI8658, ES7210, ES8311, ST7789, 8 MB PSRAM e 16 MB flash: isso distingue este anúncio da placa SpotPear muma e da M5Stack CoreS3 Lite. Verificar os componentes reais e o esquema antes do firmware.

Requisito de projeto: considerar opções com/sem bateria e com/sem toque. A variante de referência ainda não foi escolhida; não presumir que as frentes sejam mecanicamente intercambiáveis.

## Diretriz do Nei — foco físico

“acho q a ideia q se roda direto com deepkseek deve ser direto com api e tambem pode ser uma opcao depois no software. mas focamos na parte fisiocam , desenhando apra ser o mais simples e funcionar nosso designer”.

Prioridade: projeto físico. Caminho de conversa e API adiado; não é bloqueio para desenhar, nem autorização de uso da API. Estudo físico 01 em PROJETO-FISICO.md: módulo inteiro em suporte de duas peças. Dimensões oficiais obtidas; encaixe real ainda pendente. As dúvidas anteriores sobre voz/servidor ficam para a fase de software.
