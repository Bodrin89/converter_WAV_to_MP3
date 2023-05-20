import os
import subprocess
from models import User, Audio, db

API_PORT = os.environ.get("API_PORT")


def convert_file(name: str, user_token: str, mp3: str, wav: str, name_save_audio: str) -> str:
    """Выносим конвертацию файла в отдельный процесс"""
    # Вызов команды lame для конвертации
    command = f'lame --preset insane "{wav}" "{mp3}"'
    subprocess.run(command, shell=True)

    # Чтение mp3 файла в бинарном виде для сохранения в БД
    with open(mp3, 'rb') as audio_file:
        audio_data = audio_file.read()
    user = User.query.filter_by(name=name, token=user_token).first()

    audio = Audio(
        user=user,
        name_audio=name_save_audio,
        audio_file=audio_data
    )

    db.session.add(audio)
    db.session.commit()

    # Удаление временных файлов
    os.unlink(mp3)
    os.unlink(wav)

    # Ссылка для скачивания mp3 файла
    download_url = f'http://127.0.0.1:{API_PORT}/record?id={audio.id}&user={user.id}'
    return download_url
