# Diário de bordo — Umbrália

Página: `diario.html`, acessível pelo menu do início, avatar e trilhas.

Visualização inicial liberada: `previewUnlocked: true` em `diario-data.js` abre o planeta e todos os 12 cards sem moedas nem gravação de compras. Para ativar as regras de compra abaixo futuramente, alterar essa opção para `false`.

12 ilustrações originais geradas com a ferramenta integrada `image_gen`, salvas em `assets/imagens/diario/umbralia/`. Prompts em `umbralia-prompts.json`. Planeta PNG RGBA com transparência real; cenas em PNG 1536 × 1024. Nomes e legendas seguem a tabela. O item 9, sem indicação original de imagem, recebeu `o-equilibrio-dos-umbralhenses.png` / “O difícil equilíbrio dos umbralhenses”. O capitão usa a cena 3 da narrativa existente como referência.

650 moedas desbloqueiam o planeta e o primeiro card, sem cobrança duplicada. Cada um dos outros 11 cards custa 500 moedas. Total da coleção: 6.150 moedas. As miniaturas e os textos aparecem na grade; a compra libera a ampliação da imagem e a leitura no popup. O popup permite anterior/próxima entre imagens adquiridas, setas do teclado, Escape e fechamento pelo fundo.

Saldo e compras são persistidos juntos em `orbita2-wallet-v1`, com `coins` inteiro não negativo e `purchases` como lista de IDs. O saldo inicial é zero. Nenhum saldo de demonstração é dado ao usuário. Não foi definida uma regra de ganhos; a ligação com as recompensas das missões continua pendente. Os contadores de moedas existentes leem a mesma carteira. A estrela não foi alterada.

As compras usam Web Locks para serializar gravações entre abas. Se o navegador não oferecer a API ou o armazenamento falhar, a compra não é concluída. Esta versão é local, sem conta/backend: os dados pertencem ao navegador, não representam uma carteira validada por servidor. Ao integrar contas, saldo e compras devem ser validados e gravados por uma transação no servidor.

Validação: `scripts/check-diario.cjs` com Playwright/Chrome em contexto isolado. Cobre os 12 arquivos, requisito do planeta, saldo insuficiente, cancelamento, débito correto, persistência após recarga, coleção completa, reabertura gratuita, popup, navegação, compra concorrente, falha de armazenamento e links do menu. Layout verificado em 1440, 768, 390 e 320 px; capturas em `output/diario/`. Os saldos do teste existem apenas no contexto descartável do teste.

Os outros oito planetas e Aura Rubre aguardam seus conteúdos; apenas Umbrália foi implementado nesta etapa.
