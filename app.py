import os
from typing import Union
from concurrent.futures import ProcessPoolExecutor

import uuid
import secrets
from flask import Flask, request, send_file, jsonify, Response
from dotenv import load_dotenv, find_dotenv
from werkzeug.datastructures import FileStorage

from config import Config
from convert_file import convert_file
from models import db, UserSchema, User, Audio

app = Flask(__name__)

load_dotenv(find_dotenv())


app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/create/', methods=['POST'])
def create_user() -> Response:
    """Создание пользователя"""

    user_name: dict = request.get_json()
    user = User(
        uuid=uuid.uuid4(),
        name=user_name.get('user_name'),
        token=secrets.token_hex(16)
    )
    db.session.add(user)
    db.session.commit()
    result = UserSchema(exclude=['id', 'name'])
    return result.dump(user)


@app.route('/load/', methods=['POST'])
def load_audio_file() -> Union[jsonify, str]:
    """Загрузка wav файла конвертирование его в mp3 """

    user_name: str = request.form.get('user_name')
    token: str = request.form.get('token')
    audio_wav: FileStorage = request.files.get('audio')
    if not (user_name and token and audio_wav):
        return jsonify({'message': 'Не корректные данные'}), 400

    if not User.query.filter_by(name=user_name, token=token).first():
        return jsonify({'message': 'Такого пользователя не существует'}), 400

    # Присваиваем уникальное имя файлу, создаем путь для временного хранилища WAV файла и сохраняем его
    name_audio = str(uuid.uuid4())
    wav_path = f'./audio_file/file_wav/{name_audio}.wav'
    audio_wav.save(wav_path)

    # Путь для сохранения файла MP3
    mp3_path = f'./audio_file/file_mp3/{name_audio}.mp3'

    # Создаем пул процессов
    executor = ProcessPoolExecutor(max_workers=1)

    # Запускаем конвертацию файла в отдельном процессе
    future = executor.submit(convert_file, user_name, token, mp3_path, wav_path, name_audio)
    download_url: str = future.result()
    return download_url


@app.route('/record/')
def download() -> Union[Response, jsonify]:
    """Скачивание mp3 файла из БД"""

    user_id: str = request.args.get('user')
    audio_id: str = request.args.get('id')
    audio: Audio = Audio.query.filter_by(user_id=user_id, id=audio_id).first()

    # Проверка на существование файла в БД и запись во временное хранилище для скачивания
    if audio:
        file_path = f'./download/audio_{audio.name_audio}.mp3'
        with open(file_path, 'wb') as file:
            file.write(audio.audio_file)
        result = send_file(file_path, as_attachment=True)

        # Удаление скаченного файла из временного хранилища
        os.unlink(file_path)
        return result
    else:
        return jsonify({'massage': 'Аудио файл не найден'}), 400


if __name__ == '__main__':
    app.run()
