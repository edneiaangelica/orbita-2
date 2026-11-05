# Navegação do diário

`diario.html` é a galeria apenas dos planetas disponíveis. Os links levam a `diario-planeta.html?planeta=lamalume` e `diario-planeta.html?planeta=umbralia`. A página de detalhes oferece retorno à galeria e o botão “Ler texto integral” no topo. O diálogo reúne todos os trechos na ordem dos cards, com rolagem, fechamento visível e Escape.

Os cards não têm mais o botão “Ver imagem e história”. A própria imagem abre o popup. Todos continuam liberados inicialmente, conforme solicitado.

A última imagem de Lamalume, `assets/imagens/diario/lamalume/pergunta.png`, foi refeita pela ferramenta integrada image_gen com a imagem de Umbrália como referência de identidade do capitão adulto. Prompt em `lamalume-capitao-prompt.json`.

O gerador `scripts/build-diario.cjs` mantém as duas páginas. Os testes de navegação, conteúdo integral, popups, layout e compras futuras estão em `scripts/check-diario.cjs`.
