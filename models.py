from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema


db = SQLAlchemy()


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

