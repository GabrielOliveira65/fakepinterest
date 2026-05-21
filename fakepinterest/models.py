from fakepinterest import database, login_manager
from datetime import datetime, timezone
from flask_login import UserMixin
from sqlalchemy.orm import validates

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref='usuario', lazy=True)
    vUsername = database.Column(database.String, nullable=False)


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default="default.png")
    data_criacao = database.Column(database.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    deleted = database.Column(database.Boolean, default=False, nullable = False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    