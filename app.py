import os
from concurrent.futures import ProcessPoolExecutor

import uuid
import secrets
from flask import Flask, request, send_file
from dotenv import load_dotenv, find_dotenv

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
def create_user():
    """Создание пользователя"""

    user_name = request.get_json()
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
def load_audio_file():
    """Загрузка wav файла конвертирование его в mp3 """

    user_name = request.form.get('user_name')
    token = request.form.get('token')
    audio_wav = request.files.get('audio')
    if not (user_name and token and audio_wav):
        return {'message': 'Не корректные данные'}, 400

    if not User.query.filter_by(name=user_name, token=token).first():
        return "Такого пользователя не существует", 400

    name_audio = uuid.uuid4()
    wav_path = f'./audio_file/file_wav/{name_audio}.wav'
    audio_wav.save(wav_path)

    # Путь для сохранения файла MP3
    mp3_path = f'./audio_file/file_mp3/{name_audio}.mp3'

    # Создаем пул процессов
    executor = ProcessPoolExecutor(max_workers=1)

    # Запускаем конвертацию файла в отдельном процессе
    future = executor.submit(convert_file, user_name, token, mp3_path, wav_path, name_audio)
    download_url = future.result()
    return download_url


@app.route('/record/')
def download():
    """Скачивание mp3 файла из БД"""

    user_id = request.args.get('user')
    audio_id = request.args.get('id')
    audio = Audio.query.filter_by(user_id=user_id, id=audio_id).first()

    if audio:
        file_path = f'./download/audio_{audio.name_audio}.mp3'
        with open(file_path, 'wb') as file:
            file.write(audio.audio_file)
        result = send_file(file_path, as_attachment=True)

        # Удаление скаченного файла
        os.unlink(file_path)
        return result
    else:
        return 'Аудио файл не найден', 400


if __name__ == '__main__':
    app.run()
