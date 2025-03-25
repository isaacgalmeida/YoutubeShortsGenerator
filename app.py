import os
import random
import json
import requests
import re
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, VideoClip
os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"
import moviepy.config as mpc
from dotenv import load_dotenv

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# Define as pastas e URLs a partir das variáveis de ambiente, com valores padrão caso não estejam definidos
output_folder = os.getenv("OUTPUT_FOLDER", "drive/MyDrive/YouTube/shorts")
json_url = os.getenv("JSON_URL", "https://raw.githubusercontent.com/ghostnetrn/frases/refs/heads/main/frases_com_tags.json")
videos_folder = os.getenv("VIDEOS_FOLDER", "drive/MyDrive/YouTube/videos")
musicas_folder = os.getenv("MUSICAS_FOLDER", "drive/MyDrive/YouTube/audio")

os.makedirs(output_folder, exist_ok=True)

generated_ids_file = os.path.join(output_folder, "generated_ids.json")
json_output_file = os.path.join(output_folder, "videos_info.json")

# Carrega os IDs já gerados (se existir)
try:
    with open(generated_ids_file, "r", encoding="utf-8") as f:
        generated_ids = json.load(f)
except Exception:
    generated_ids = []

# Solicita ao usuário quantos vídeos deseja gerar ou se deseja gerar todos
user_input = input("Quantos vídeos deseja gerar? (padrão 3, ou digite 'todos' para gerar todos os não gerados): ")
if user_input.strip().lower() == "todos":
    all_mode = True
    num_videos = None
else:
    all_mode = False
    num_videos = int(user_input) if user_input.strip() != "" else 3

# Busca o JSON com as frases
response = requests.get(json_url)
frases = response.json()

# Filtra as frases que ainda não foram geradas
available_phrases = [frase for frase in frases if frase["id"] not in generated_ids]
if not available_phrases:
    print("Não há novas frases disponíveis para gerar vídeos.")
    exit()

# Se o usuário escolheu "todos", define num_videos como o total disponível
if all_mode:
    num_videos = len(available_phrases)
else:
    if num_videos > len(available_phrases):
        num_videos = len(available_phrases)

print(f"\nSerão gerados {num_videos} vídeos.")

# Lista para armazenar informações dos vídeos gerados nesta execução
new_videos_info = []

for i in range(num_videos):
    # Seleciona a primeira frase dos disponíveis e remove para evitar duplicata
    frase_escolhida = available_phrases[0]
    available_phrases.remove(frase_escolhida)
    generated_ids.append(frase_escolhida["id"])

    # Define o nome final do vídeo e verifica se ele já existe
    final_filename = os.path.join(output_folder, f"{frase_escolhida['id']}.mp4")
    if os.path.exists(final_filename):
        print(f"Vídeo com id {frase_escolhida['id']} já existe. Pulando...")
        continue

    # Seleciona o primeiro vídeo encontrado na pasta
    video_files = os.listdir(videos_folder)
    if not video_files:
        print("Nenhum vídeo encontrado na pasta", videos_folder)
        exit()
    video_arquivo = os.path.join(videos_folder, video_files[0])
    
    # Seleciona aleatoriamente uma música (mantém a seleção aleatória para música)
    musica_arquivo = os.path.join(musicas_folder, random.choice(os.listdir(musicas_folder)))

    print(f"\nGerando vídeo {i+1}:")
    print("Frase escolhida:", frase_escolhida)
    print("Arquivo de vídeo:", video_arquivo)
    print("Arquivo de música:", musica_arquivo)

    # Determina a duração com base no tamanho da frase (entre 12 e 16 segundos)
    num_palavras = len(frase_escolhida["frase"].split())
    duration = max(12, min(16, num_palavras / 3))

    # Carrega o vídeo e a música com MoviePy e corta para a duração desejada
    #video_clip = VideoFileClip(video_arquivo).subclip(0, duration)
    video_clip = VideoFileClip(video_arquivo).subclipped(0, duration)
    #audio_clip = AudioFileClip(musica_arquivo).subclip(0, duration).volumex(0.6)
    audio_clip = AudioFileClip(musica_arquivo).subclipped(0, duration).volumex(0.6)

    video_width, video_height = video_clip.w, video_clip.h

    # Cria um TextClip temporário para obter o tamanho do texto
    temp_txt_clip = TextClip(
        txt=frase_escolhida["frase"],
        fontsize=70,
        color='#1877F2',  # Cor inicial (azul Facebook) para o texto
        font='DejaVuSans-Bold',
        method='caption',
        align='center',
        size=(int(video_width * 0.8), int(video_height * 0.3))
    )
    phrase_w, phrase_h = temp_txt_clip.size
    temp_txt_clip.close()

    # Função para gerar frames do TextClip com cores alternadas (efeito de piscar)
    def make_text_frame(t):
        colors = ['#1877F2', 'yellow', 'lightgray']  # Azul Facebook, amarelo e cinza claro
        idx = int(t) % len(colors)
        txt_clip = TextClip(
            txt=frase_escolhida["frase"],
            fontsize=70,
            color=colors[idx],
            font='DejaVuSans-Bold',
            method='caption',
            align='center',
            size=(int(video_width * 0.8), int(video_height * 0.3))
        )
        return txt_clip.get_frame(0)

    animated_txt_clip = VideoClip(make_text_frame, duration=duration)

    # Seleciona uma cor de fundo aleatória (RGB) e cria o fundo para o texto com transparência de 60%
    bg_color = tuple(random.randint(0, 255) for _ in range(3))
    bg_clip_phrase = ColorClip(size=(phrase_w, phrase_h), color=bg_color).set_duration(duration)
    bg_clip_phrase = bg_clip_phrase.set_opacity(0.6)

    # Compoe o fundo com o texto animado
    phrase_with_bg = CompositeVideoClip(
        [bg_clip_phrase, animated_txt_clip.set_position((0, 0))]
    ).set_duration(duration)

    phrase_pos_x = (video_width - phrase_w) / 2
    phrase_pos_y = (video_height - phrase_h) / 2
    phrase_with_bg = phrase_with_bg.set_position((phrase_pos_x, phrase_pos_y))

    # Cria o TextClip do autor (parte inferior)
    txt_clip_author = TextClip(
        txt=frase_escolhida["autor"],
        fontsize=40,
        color='black',
        bg_color='white',
        method='label'
    ).set_duration(duration)

    author_w, author_h = txt_clip_author.size
    author_pos_x = (video_width - author_w) / 2
    author_pos_y = video_height * 0.85 - (author_h / 2)
    txt_clip_author = txt_clip_author.set_position((author_pos_x, author_pos_y))

    final_clip = CompositeVideoClip([video_clip, phrase_with_bg, txt_clip_author]).set_audio(audio_clip)

    temp_output = os.path.join(output_folder, f"temp_video_{frase_escolhida['id']}.mp4")
    final_clip.write_videofile(temp_output, codec="libx264", audio_codec="aac")

    metadata_title = frase_escolhida["frase"]
    metadata_keywords = f'{frase_escolhida["autor"]},shorts,YouTube,TikTok'
    metadata_comment = f'Frase: {frase_escolhida["frase"]} | Autor: {frase_escolhida["autor"]}'

    ffmpeg_command = (
        f'ffmpeg -i "{temp_output}" '
        f'-metadata title="{metadata_title}" '
        f'-metadata comment="{metadata_comment}" '
        f'-metadata keywords="{metadata_keywords}" '
        f'-codec copy "{final_filename}"'
    )
    os.system(ffmpeg_command)
    print("Vídeo final salvo em:", final_filename)

    if os.path.exists(temp_output):
        os.remove(temp_output)

    # Atualiza as informações do vídeo gerado (sem as tags)
    new_videos_info.append({
        "id": frase_escolhida["id"],
        "frase": frase_escolhida["frase"]
    })

# Lê os dados existentes (se houver) e anexa os novos
try:
    with open(json_output_file, "r", encoding="utf-8") as f:
        existing_videos_info = json.load(f)
except Exception:
    existing_videos_info = []

existing_videos_info.extend(new_videos_info)

with open(json_output_file, "w", encoding="utf-8") as f:
    json.dump(existing_videos_info, f, indent=4, ensure_ascii=False)

print("\nArquivo JSON de vídeos gerado:", json_output_file)

with open(generated_ids_file, "w", encoding="utf-8") as f:
    json.dump(generated_ids, f, indent=4, ensure_ascii=False)

print("\nIDs gerados atualizados em:", generated_ids_file)
