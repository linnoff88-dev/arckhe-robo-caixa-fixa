# Publicação — 16/11/2026

- Guia PT: https://inematds.github.io/robo-caixa-fixa/guia/
- EN: https://inematds.github.io/robo-caixa-fixa/guia/en/
- ES: https://inematds.github.io/robo-caixa-fixa/guia/es/
- Downloads de STL e ZIP responderam 200 e foram comparados byte a byte com os arquivos locais.
- GitHub Pages: Actions 43949345490 concluída com sucesso; commit 0fd6389.
- Portal: push 3e625ca em NeiMaldaner/portal; 13 testes passaram, build Next e tsc concluídos. Entrada em Projetos e no feed, traduções EN/ES.
- Buscas: push 334331b em inematds/inemabuscas; 450 projetos, nenhum removido.
- PRO: push c40cd75 em inematds/inemapro; base com 19729 itens, 1 novo e nenhum removido; 41 testes passaram; novo item classificado em robotica-ia-fisica.
- INEMA.ROBOT: https://t.me/c/2412734678/3027 ; MENU atualizado, mensagem 3041. Tópico e MENU lidos de volta. Skill postar-telegram aplicada.
- Vídeo pedido para lives6: em produção, ainda sem URL. Pasta local ~/projetos/output/robo-caixa-fixa-video-20261116/. Roteiro revisado para público de impressora A1, nota 9; avatar pelo estúdio HeyGen, API só leitura/download, conforme autorização permanente.

Publicação não equivale a validação física. Arquivos de estudo: sem fatiamento, impressão e encaixe de bancada conferidos. Bambu Studio oficial só x86-64; host é ARM.

Avatar enviado no estúdio em16/11, id05ac8a010da746e2b1df47436697f5d0; geração pendente na última consulta. Download e preparação em serviços systemd; bilhete de continuação no output. Sem alegar vídeo publicado até recibo real do YouTube.

## Vídeo concluído — 16/11/2026

- YouTube lives6 (INEMA Robot): https://www.youtube.com/watch?v=BEY94Ag9BWk ; público, capa aplicada. Recibo: `/home/nmaldaner/projetos/output/robo-caixa-fixa-video-20261116/producao/yt-publicacao.log`.
- Release: https://github.com/inematds/robo-caixa-fixa/releases/tag/video-v1.0.0 ; assets robo-caixa-fixa.mp4 e robo-caixa-fixa.srt.
- QA: 132,181s, 1920×1080, 25fps, 81 cues; decode sem erro; −18,9LUFS, pico−3,5dBFS; strict/check/snapshots aprovados.
- YouTube sem escopo youtube.force-ssl para SRT separado; legenda embutida e SRT de download preservados.
- Integração: player PT nos três guias, aviso EN/ES traduzido pelo inema-traduz, READMEs com link. Conferência local 3 idiomas × desktop/mobile sem overflow.
- Portal vídeo: push `44d63c3` em NeiMaldaner/portal, apenas catálogo/feed de vídeos; 13 testes, build e TypeScript OK. Sem republicar buscas/PRO.
- INEMA.ROBOT tópico3027: mensagens3042 e3043 lidas de volta, link https://t.me/c/2412734678/3043 ; sem novo MENU.
- MP4 da Release baixado publicamente e comparado byte a byte com o aprovado.
