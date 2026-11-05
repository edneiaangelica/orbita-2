# Missão 2 — Adição e subtração até 20

Implementada na tela Trilhas, ao lado da Missão 1, conforme confirmação do usuário. Três desafios com 15 questões cada: dez questões do anexo e cinco novas por desafio. Questões de resposta digitada e quiz tipo 3 mantêm o comportamento da missão anterior, incluindo tentativas, feedbacks, recompensas e revisão.

Arquivos de conteúdo: mission-2-data.js e scripts/audio-missao-2.json. Os 135 áudios de enunciados e feedbacks usam Francisca pt-BR e ficam em assets/sons/missao-2. Os três vídeos são os arquivos existentes nas pastas assets/videos/missao-2/desafio-1, desafio-2 e desafio-3. O terceiro tem o nome vd-explica-d2-m3.mp4.

Feedbacks específicos e variados para as 15 questões de cada desafio. Correções editoriais: 16 árvores passou a 16 cadernos; a dica de 14 − 4 pede o número restante, evitando confusão entre quantidade de dezenas e resultado; a dica da compra de cadernos descreve a situação em vez de depender apenas da expressão ao todo.

mission-catalog.js seleciona a missão por parâmetro de URL; mission.js mantém progresso, áudios e recompensas separados por missão. A chave de progresso da Missão 1 foi preservada. Os caminhos dos vídeos da Missão 1 foram ajustados à organização atual de pastas.

Validação: scripts/check-missao-2.cjs verifica gabaritos, 45 telas, vídeos, feedbacks, quiz, caminho do áudio, persistência e separação do progresso e layout móvel. scripts/check-mission.cjs verifica a integridade da Missão 1. Prévias em output/missao-2-trilha.png e output/missao-2-mobile.png.
