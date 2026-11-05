# Roleta dos planetas — Sorte ou revés da Missão 2

Roleta de seis setores iguais: Lamalume −3, Papiron −1, Mecano +2, Aerívia +3, Planeta 42 +4, Aura Rubre +5 estrelas. Uma única tentativa por estudante/navegador, inclusive no modo de revisão. Resultado e recibo são gravados juntos antes da animação, protegidos pelo bloqueio da carteira quando disponível. Reabrir ou recarregar não permite novo giro. Saldo mínimo zero, seguindo a regra existente da carteira, informado nas instruções e no resultado quando aplicável.

Integração: window.OrbitaLuck abre a roleta na Missão 2; a Missão 1 continua com o jogo da memória. A conclusão da Missão 2 abre a oferta automaticamente. O menu Sorte ou revés da Missão 2 também permite acessá-la durante a revisão do aplicativo. Fechar sem girar não consome a tentativa.

Arquivos: roleta.js, roleta.css, wallet.js, sorte-reves.js, mission.html. Instruções Francisca em assets/sons/missao-2/roleta-instrucoes.mp3, com playbackRate=1.25. Fonte de voz: scripts/narrar-roleta.py.

Verificação: scripts/check-roleta.cjs testa os seis resultados e deltas, proteção contra giros repetidos, persistência, saldo mínimo, posição final da seta, leitura, abertura após conclusão da Missão 2 e preservação da memória na Missão 1. Sem rolagem interna a 1366×768, 1280×720 e 1024×600; layout móvel a 390×844. Prévias em output/roleta-planetas.png e output/roleta-planetas-mobile.png.
