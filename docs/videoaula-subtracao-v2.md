# Subtração até 20 — roteiro de dez cenas

Vídeo: `assets/videos/missao-2/desafio-2/subtracao-ate-20-v2/missao-2-desafio-2-subtracao-ate-20-v2.mp4`.

Duração: aproximadamente 90,33 segundos. Horizontal, 1280 × 720, 24 fps, H.264/AAC. Voz Francisca Neural em português brasileiro. O novo roteiro completo está em `scripts/subtracao-v2.json`.

As dez cenas incluem abertura, 8 − 4 com dedos abaixando um a um durante a contagem 1–4, nova contagem dos dedos restantes antes do resultado, estratégia para 15 − 4, balão com 15, quatro dedos representando as retiradas, sequência 14–13–12–11 com dedos abaixando, resultado, revisão em três etapas e exercício 16 − 3.

Depois de “Quanto deu?”, há uma pausa de exatamente cinco segundos (120 quadros). Só depois começa “Quinze, quatorze, treze!”, com os três dedos abaixando em sequência. A equação completa é revelada na fala seguinte.

Foram reutilizadas as ilustrações geradas no ImageGen e revisadas na aula de adição: personagem e sequência de seis poses da mão. A animação dos dedos usa transições breves entre poses, com destaque antes de cada dobra. Prompts de origem: `docs/adicao-v2-prompts.txt`.

Fontes: `scripts/narrar-subtracao-v2.py` e `scripts/render-subtracao-v2.py`. O renderizador aceita `--preview`; `scripts/cenas-subtracao-v2.py` guarda as definições das cenas. O áudio é ajustado com atempo=0.78, preservando a altura da voz; os tempos das palavras recebem o mesmo ajuste. Legendas incorporadas, WebVTT, poster, prancha de revisão e timeline acompanham o MP4.

As versões anteriores e a configuração das missões foram preservadas.
