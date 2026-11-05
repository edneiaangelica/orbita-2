# Vídeo de apresentação — Missão Órbita

Vídeo final: `assets/videos/narrativa/orbita-a-missao.mp4` (1280×720, 30 fps, H.264/AAC, aproximadamente 58,47 segundos).

O texto original está preservado, na mesma ordem e divisão em oito trechos, em `scripts/narrativa-texto.json`. Cada trecho possui sua própria ilustração, narração e legenda. A voz utilizada é `pt-BR-FranciscaNeural`, a -8% de velocidade, sem reescrever os enunciados.

As oito ilustrações foram criadas com a ferramenta integrada ImageGen e estão em `assets/imagens/narrativa/cena-01.png` até `cena-08.png`. Os prompts exatos estão em `scripts/narrativa-prompts.json`. O Teleco usa o mascote existente do app como referência. A paleta usa azul royal, berinjela, azul-marinho, branco gelo e acentos dourados.

Animação: movimentos de câmera (aproximação, afastamento e deslocamento lateral), transições de entrada/saída e marcador visual da cena. As ilustrações são animadas por composição no FFmpeg; não há animação articulada dos personagens. Legendas incorporadas no MP4, com versão WebVTT para acessibilidade. A narrativa completa também aparece num painel expansível na página inicial.

## Reprodução e manutenção

- A seção “Conheça a missão Órbita” está em `index.html`, entre o destaque principal e as estatísticas da jornada.
- Não há reprodução automática. A primeira reprodução intencional habilita o som; o botão global permite silenciar.
- `scripts/narrar-historia.py` gera as oito narrações, usando o serviço de voz e acesso à internet. Preserva os arquivos existentes.
- `node scripts/build-narrativa.cjs` monta as cenas e o vídeo final. `FFMPEG_PATH` permite configurar o executável. A montagem usa a fonte Segoe UI do Windows.
- `scripts/check-narrativa.cjs` verifica texto, oito cenas e legendas, dimensões, duração, reprodução, controle de áudio e telas de 1366, 390 e 320 pixels. `PLAYWRIGHT_MODULE` pode apontar para uma instalação externa do Playwright.
- O MP4 foi decodificado integralmente sem erros. A leitura de metadados e a reprodução foram verificadas no Chrome.

Arquivos auxiliares: `assets/videos/narrativa/timeline.json`, `narrativa.vtt` e `poster.jpg`. Intermediários de montagem em `tmp/narrativa`.
