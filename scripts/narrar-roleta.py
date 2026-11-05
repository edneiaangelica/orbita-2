import sys,asyncio
from pathlib import Path
sys.path.insert(0,'C:/Users/USUARIO/Desktop/videos-educacionais/.deps')
import edge_tts
text='Você tem uma tentativa! Clique em girar a roleta e espere ela parar. O planeta indicado pela seta define quantas estrelas você ganha ou perde. Confira a tabela antes de girar. Seu saldo não fica abaixo de zero.'
async def main():
 await edge_tts.Communicate(text,'pt-BR-FranciscaNeural',rate='+0%').save(str(Path('assets/sons/missao-2/roleta-instrucoes.mp3')))
asyncio.run(main())
