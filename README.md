# Projeto de Geração de Vídeos Automáticos

Este projeto gera vídeos automáticos para plataformas como YouTube Shorts e TikTok, utilizando frases obtidas de um JSON hospedado no GitHub. A partir de um vídeo e uma faixa de áudio escolhidos aleatoriamente, o script adiciona uma sobreposição de texto (com a frase e o autor) e gera o vídeo final com metadados.

## Funcionalidades

- Busca frases a partir de um JSON remoto.
- Seleciona vídeos e áudios aleatórios de pastas locais.
- Cria sobreposições de texto com a frase e o autor utilizando o MoviePy.
- Gera o vídeo final com metadados embutidos utilizando FFmpeg.
- Atualiza arquivos JSON com informações dos vídeos gerados e os IDs já utilizados.

## Pré-requisitos

- **Python 3.6 ou superior**

### Dependências Python

Instale as dependências utilizando o pip:

```bash
pip install -r requirements.txt
```

### Dependências de Sistema

- **FFmpeg:** Necessário para o processamento e geração final do vídeo.
- **ImageMagick:** Utilizado pelo MoviePy para renderização dos textos (confirme se o caminho configurado em `mpc.change_settings` está correto para o seu sistema).

## Estrutura de Diretórios

O script espera encontrar os seguintes diretórios (ajuste conforme necessário):

- **Vídeos:** `drive/MyDrive/YouTube/videos`
- **Áudios:** `drive/MyDrive/YouTube/audio`
- **Saída dos vídeos gerados:** `drive/MyDrive/YouTube/shorts`

Certifique-se de que esses diretórios existam e contenham os arquivos necessários. (insira audios em mp3 na pasta e também os videos no formato para shorts, que podem ser feitos no Canva)

## Como Usar

1. Configure os diretórios e certifique-se de que os vídeos e áudios estão disponíveis nos caminhos especificados.
2. Execute o script:

   ```bash
   python app.py
   ```

   2.1. Em docker:

   ```bash
   docker-compose up --build
   ```

3. O script solicitará quantos vídeos deseja gerar. Você pode informar um número ou digitar `todos` para processar todas as frases que ainda não foram utilizadas.
4. Os vídeos gerados serão salvos na pasta de saída definida, e os arquivos JSON (`generated_ids.json` e `videos_info.json`) serão atualizados automaticamente.

## Considerações

- Verifique se o FFmpeg e o ImageMagick estão corretamente instalados e configurados no seu sistema.
- O JSON com as frases é baixado do repositório GitHub, mas pode ser modificado conforme sua necessidade.
- Caso queira ajustar configurações de layout ou estilo dos textos, edite os parâmetros dos `TextClip` e `CompositeVideoClip`.
