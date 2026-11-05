# Missão 2 — Desafio 3: Probleminhas de adição e subtração

Vídeo: `assets/videos/missao-2/desafio-3/probleminhas/missao-2-desafio-3-probleminhas.mp4`.

Duração aproximada de 100,12 segundos, horizontal HD 1280 × 720, 24 fps, H.264/AAC. Narração em português brasileiro, Francisca Neural. Texto integral em `scripts/problemas.json`.

As dez cenas seguem o roteiro fornecido: abertura, estrelas se juntando, oito figurinhas de Ana mais cinco entregues pela amiga, reunião das treze figurinhas, retirada e comparação de bolinhas, quinze carrinhos de Pedro e quatro entregues ao irmão, onze carrinhos restantes, cartões de revisão, leitura do enunciado com lupa e encerramento.

As quantidades são compostas programaticamente com instâncias individuais das ilustrações: oito figurinhas em duas fileiras de quatro; outras cinco em grupo separado; treze na formação final; quinze carrinhos em três fileiras de cinco; quatro movidos para o irmão e onze destacados junto de Pedro. Na comparação, cinco e três bolinhas ficam alinhadas, com duas em destaque na fileira maior.

Ana, amiga, Pedro, irmão, figurinha e carrinho foram gerados pelo ImageGen integrado em `assets/imagens/missao-2/desafio-3/ilustracoes.png`. Prompt completo em `docs/problemas-prompt.txt`. As figuras são animadas por composição, deslocamentos e destaques; os personagens não têm animação corporal articulada.

Fontes: `scripts/narrar-problemas.py`, `scripts/render-problemas.py` e definição visual `scripts/cenas-problemas.py`. A montagem ajusta o tempo da voz preservando a altura e alinha os eventos de animação aos tempos das palavras. O renderizador aceita `--preview`. Junto ao MP4: poster, legendas WebVTT, timeline e prancha de revisão.

Os arquivos anteriores e a configuração das missões permanecem preservados.
