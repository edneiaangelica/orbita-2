# Tempus

Álbum integrado ao Diário de bordo com 12 cenas, legendas e texto integral fornecidos pelo usuário. Mantém a prévia desbloqueada e os valores futuros de 650/500 moedas dos álbuns anteriores.

Ilustrações originais geradas com a ferramenta integrada de imagens: fantasia de relojoaria com prata escovada, ouro, personagens de pele perolada e montanhas de engrenagens. Arquivos em `assets/imagens/diario/tempus/`; prompts e origens em `docs/tempus-prompts.json`.

Entrada: `diario-planeta.html?planeta=tempus`. Tema visual específico em `diario.css`; conteúdo em `diario-tempus.js`. Inclusão preservada no gerador `scripts/build-diario.cjs`.

Verificação em `scripts/check-diario.cjs`: galeria com oito planetas, abertura das 12 cenas, texto integral, saldo inalterado e layouts de 1440, 768, 390 e 320 pixels. Capturas em `output/diario/tempus-*.png`.

Use `DIARY_PLANET_ONLY=tempus` para executar somente a galeria e o novo álbum. A suíte geral chegou à verificação de menus e encontrou um link ausente para `diario.html` em outra página; essa navegação não foi alterada neste trabalho.
