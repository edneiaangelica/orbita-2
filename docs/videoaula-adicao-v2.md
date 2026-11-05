# Adição até 20 — novo roteiro de nove cenas

Vídeo: `assets/videos/missao-2/desafio-1/adicao-ate-20-v2/missao-2-desafio-1-adicao-ate-20-v2.mp4`.

Duração: aproximadamente 89,33 segundos. Horizontal, 1280 × 720, 24 fps, H.264/AAC. Nova versão independente; os vídeos anteriores permanecem preservados.

As nove cenas seguem o roteiro fornecido, incluindo os sete destaques de 4 + 3, duas mãos abertas no novo desafio, o 8 no balão, destaque do 5, sequência de cinco dedos abaixados em 9–13, brilho no resultado, revisão em três etapas e exercício 9 + 4. A última pergunta é seguida por uma cena de silêncio com exatamente 120 quadros (5 segundos), antes da resposta 13.

Narração: Francisca Neural, português brasileiro. Roteiro integral em `scripts/adicao-v2.json`; os trechos de contagem são sintetizados mais lentamente. O renderizador usa atempo=0.74, preservando a altura da voz, e ajusta os tempos de palavras pela mesma proporção. Legendas incorporadas e WebVTT externo.

Ilustrações do personagem e das mãos de 4 + 3 reutilizadas da versão corrigida. Novas poses da mão (5, 4, 3, 2, 1, 0 dedos levantados) criadas e corrigidas no ImageGen integrado: `assets/imagens/missao-2/desafio-1/v2/poses.png`. Prompts completos em `docs/adicao-v2-prompts.txt`. Os dedos abaixam por transições curtas entre as poses ilustradas, após o destaque de cada dedo, sincronizadas à narração.

Fontes: `scripts/narrar-adicao-v2.py` e `scripts/render-adicao-v2.py`. O renderizador aceita `--preview` para gerar a prancha de revisão. O diretório do vídeo inclui poster, legendas, revisão e timeline. Não houve mudança nas páginas ou na configuração das missões.
