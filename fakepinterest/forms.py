from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from fakepinterest.models import Usuario
from flask_login import current_user


class FormLogin(FlaskForm):
    email_username = StringField('Nome do Usuário ou E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    lembrar_dados = BooleanField('Lembrar Login')
    botao_submit_login = SubmitField('Entrar')

    def validate_email_username(self, email_username):
        usuario = Usuario.query.filter_by(username=email_username.data).first()
        email = Usuario.query.filter_by(email=email_username.data).first()
        if not usuario and not email:
            raise ValidationError('E-mail ou Usuário não existe.')
        


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(4, 20),  
                                                          Regexp(r'^[A-Za-z0-9_.-]+$',message='Use apenas letras, números, "_" , "-" ou "." (sem espaços)')])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Usuário já cadastrado, use outro nome de usuário ou faça login para continuar')
        

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado, use outro e-mail ou faça login para continuar')
        

class PostFoto(FlaskForm):
    imagem = FileField('Foto', validators=[DataRequired(),  FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas!')])
    enviar_foto = SubmitField('Enviar')
    