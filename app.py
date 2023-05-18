import os

import uuid
import secrets
import subprocess
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, send_file
from dotenv import load_dotenv, find_dotenv
from marshmallow import Schema, fields

app = Flask(__name__)

load_dotenv(find_dotenv())

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
API_PORT = os.environ.get("API_PORT")

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{POSTGRES_USER}:" \
                                        f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:" \
                                        f"{POSTGRES_PORT}/{POSTGRES_DB}"


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(255))
    name = db.Column(db.String(255))
    token = db.Column(db.String(255))


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    uuid = fields.String()
    name = fields.String()
    token = fields.String()


class Audio(db.Model):
    __tablename__ = 'audio'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    name_audio = db.Column(db.String())
    audio_file = db.Column(db.LargeBinary())


class AudioSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()


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

    if not User.query.filter_by(name=user_name).first():
        return "Такого пользователя не существует"

    name_audio = uuid.uuid4()
    wav_path = f'./audio_file/file_wav/{name_audio}.wav'
    audio_wav.save(wav_path)

    # Путь для сохранения файла MP3
    mp3_path = f'./audio_file/file_mp3/{name_audio}.mp3'

    # Вызов команды lame для конвертации
    command = f'lame --preset insane "{wav_path}" "{mp3_path}"'
    subprocess.run(command, shell=True)

    # Чтение mp3 файла в бинарном виде для сохранения в БД
    with open(mp3_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    user = User.query.filter_by(name=user_name).first()

    audio = Audio(
        user=user,
        name_audio=name_audio,
        audio_file=audio_data
    )
    db.session.add(audio)
    db.session.commit()

    os.unlink(mp3_path)
    os.unlink(wav_path)

    # Ссылка для скачивания mp3 файла
    return f'http://127.0.0.1:{API_PORT}/record?id={audio.id}&user={user.id}'


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
        return 'Аудио файл не найден', 404

if __name__ == '__main__':
    app.run()
