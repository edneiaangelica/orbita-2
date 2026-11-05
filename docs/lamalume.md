# Lamalume no diário

Lamalume é o planeta 02 e abre por padrão em `diario.html`. O seletor permite alternar entre Lamalume e Umbrália, e `?planeta=lamalume` / `?planeta=umbralia` preserva a seleção ao recarregar.

Os 12 cards e o planeta estão liberados (`previewUnlocked: true`), sem consumir saldo. Valores de 650 moedas para planeta/card 1 e 500 para os demais permanecem cadastrados para ativação futura.

As 12 imagens estão em `assets/imagens/diario/lamalume/`, nomeadas conforme a tabela. Foram aproveitadas as ilustrações fofas e divertidas já existentes em `assets/imagens/mundos/lamalume/`, preservando os originais. Duas foram editadas com a ferramenta integrada `image_gen`: o planeta recebeu fundo transparente, e o nascimento passou a mostrar o casulo de barro aberto com a concha em seu interior. Prompts em `lamalume-prompts.json`.

Textos e legendas em `diario-lamalume.js`, com ajustes mínimos de pontuação, concordância e padronização do nome Lamalume. O diálogo “— Sou bonito?” mantém uma quebra de linha própria.

Validação em `scripts/check-diario.cjs`: todos os popups de Lamalume e seus textos, carregamento das imagens, seletor, seleção após recarga, larguras 1440/390/320 e regressão dos fluxos de Umbrália. Capturas em `output/diario/lamalume-*.png`.
