# Aerívia — Diário de bordo

Álbum com 12 ilustrações originais em aquarela, criadas com a ferramenta integrada de geração de imagens. Arquivos finais em `assets/imagens/diario/aerivia/`; prompts e fontes em `docs/aerivia-prompts.json`.

O planeta aparece na galeria e abre sua página própria. Todas as imagens ficam disponíveis na prévia; clicar abre imagem e texto em um diálogo ampliado. O botão superior abre o texto integral. A identidade do capitão segue a imagem de Umbrália, adaptada à aquarela.

O planeta tem fundo transparente. Os nomes dos arquivos e as legendas seguem o material enviado; a grafia de “Aeriviana” foi corrigida na legenda do almoço. A ordem 9 preserva a descrição fornecida, embora Umbrália também esteja cadastrada como 9. Custos futuros seguem o padrão dos álbuns: 650 para o planeta e 500 para os demais cards; nenhuma recompensa ou cobrança foi ativada.

Verificação: `scripts/check-diario.cjs` cobre a galeria, os 12 diálogos, o texto integral, saldo inalterado e telas de 1440, 768, 390 e 320 pixels, além da regressão dos outros quatro álbuns. Capturas em `output/diario/aerivia-*.png`.
