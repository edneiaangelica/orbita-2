# Missão 1 — Os números

Abra `index.html` e clique em **Ir para minha trilha** ou **Trilhas**. Cada desafio abre primeiro sua videoaula, com a instrução solicitada e o botão **Responder às questões**. A atividade mantém enunciado, imagem e opções visíveis durante a leitura.

São três desafios de 15 questões. As dez primeiras preservam o roteiro fornecido; as cinco últimas seguem as substituições solicitadas. No Desafio 3, as questões 11 a 15 são quizzes tipo 3, em texto, sobre composição de números, com gabaritos A, A, C, C e B e contas completas nos feedbacks de acerto.

## Leitura

A voz padrão é **pt-BR-FranciscaNeural**, substituição autorizada pelo usuário para Viola. Há 157 arquivos MP3 locais: enunciados sem descrição da imagem ou alternativas, feedbacks de acerto e erro e feedbacks específicos das alternativas. O botão global de som interrompe a narração; clicar em Ouvir questão ou Ouvir feedback liga o som. O player permite pausar, repetir e ajustar volume. Trocar de questão ou voltar ao vídeo interrompe a leitura.

As vozes brasileiras do navegador são alternativas opcionais. A ausência delas não impede os MP3. A implementação não apresenta outra voz como Viola.

## Estrutura das questões

`mission-data.js` contém os dados e `mission.js` os renderizadores:

- `qt1`: enunciado com imagem; alternativas em texto.
- `qt2`: enunciado em texto; alternativas `{label, image}`.
- `qt3`: enunciado e alternativas em texto.
- `qt4`: imagem no enunciado e nas alternativas.
- `click`: seleção direta, com a mesma validação das alternativas.
- `input`: resposta numérica digitada.
- `at1`: ordenar `items`; `answer` contém a sequência correta. Arraste no computador ou use as setas no teclado/celular.
- `at2`: dinheiro; `denominations` e `answer` são inteiros em centavos. Aceita arraste e clique; clicar no dinheiro escolhido remove uma unidade.

Campos comuns: `id`, `prompt`, `success`, `error`, `difficulty`. `errors` é uma lista opcional de feedbacks por alternativa. `imageAlt` descreve a informação visual para acessibilidade. Nos quizzes, `answer` é o índice da alternativa, começando em zero.

O progresso fica no navegador, em `orbita2-mission1-v1`; não requer login. Não há sincronização entre dispositivos.

## Verificação e manutenção

- `node scripts/check-mission.cjs`: valida contagens, gabaritos originais, feedbacks, imagens, vídeos, arquivos de áudio e referências da interface.
- `node scripts/serve.cjs`: prévia local em `http://127.0.0.1:4173`, com suporte a intervalos para vídeo/áudio.
- `node scripts/build-mission.cjs`: recompõe os dados a partir do roteiro em `docs/missao-1-original.txt` e das questões complementares.
- `node scripts/prepare-audio.cjs`: cria o roteiro de narração em `scripts/audio-manifest.json`.
- `scripts/generate-audio.py`: geração com `edge_tts`, requer acesso à internet. Aceita um identificador como argumento para regravar só um áudio. Os arquivos entregues já estão prontos; não é necessário gerar novamente para utilizar a missão.

Testado no navegador: início → trilha → desafio → videoaula → questões; imagens e opções durante a leitura; reprodução dos MP3 de questão e feedback; erro, acerto e feedback específico; ordenação pelas setas; troca de desafio e retorno à videoaula.


## Interface revisada

No PC, enunciado e imagem ficam à esquerda; respostas e conferência ficam à direita. O feedback abre em um diálogo com mascote de acerto ou erro, fechamento por botão ou Escape e leitura opcional. A navegação e a seleção de voz estão no botão de ícone. As questões finais não exibem o rótulo de dificuldade.

Os 45 arquivos `*-prompt.mp3` leem apenas `prompt`; os antigos `*-question.mp3` foram preservados mas não são utilizados. `scripts/generate-audio.py --prompts` regrava somente os enunciados.

Imagem corrigida: `assets/imagens/missao-1-novas/d1-q12-corrigida.png`, editada com a ferramenta integrada ImageGen. Prompt: “Correct ONLY the vertical yellow rod: it MUST contain exactly TEN equal cubes stacked vertically with nine clearly visible internal horizontal dividing lines. Keep the TWO separate unit cubes to the right, same yellow gold material, white background and clean educational 3D illustration style. Total is twelve cubes. No text, labels, numbers, extra objects. Adjust framing to fit ten cubes without clipping.” A barra foi conferida visualmente: dez cubinhos e duas unidades separadas.
