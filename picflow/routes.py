from flask import render_template, url_for, redirect, flash, abort
from picflow import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from picflow.forms import FormLogin, FormCriarConta, PostFoto
from picflow.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
import cloudinary.uploader
import io

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    form_login = FormLogin()
    if form_login.validate_on_submit():
        if '@' in form_login.email_username.data:
            usuario = Usuario.query.filter_by(email=form_login.email_username.data).first()
        else:
            usuario = Usuario.query.filter_by(username=form_login.email_username.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data):
            login_user(usuario)
            return redirect(url_for('user_profile'))
        else:
            flash("Senha incorreta", 'alert-danger')
    return render_template('homepage.html', form=form_login)
    
@app.route('/registrar', methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data.lower(), email=form_criarconta.email.data, senha=senha, vUsername=form_criarconta.username.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for('user_profile'))
    return render_template('criar_conta.html', form=form_criarconta)

@app.route('/perfil')
@login_required
def user_profile():
    return redirect(url_for('perfil', usuario=current_user.username))

def salvar_imagem(imagem):
    resultado = cloudinary.uploader.upload(imagem)
    return resultado['secure_url']

@app.route('/perfil/<usuario>', methods=['GET', 'POST'])
@login_required
def perfil(usuario):
    usuario_data = Usuario.query.filter(Usuario.username.ilike(usuario)).first()
    if not usuario_data:
        return redirect(url_for('user_profile'))
    
    fotos = Foto.query.filter_by(deleted=False, id_usuario=usuario_data.id).order_by(Foto.data_criacao.desc()).all() 

    if usuario_data.id == current_user.id:
        form_foto = PostFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.imagem.data
            url = salvar_imagem(arquivo)
            foto = Foto(imagem=url , id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
            return redirect(url_for('user_profile'))
        return render_template('perfil_usuario.html', usuario=current_user, form=form_foto, fotos=fotos)
       
    else:
        return render_template('perfil_usuario.html', usuario=usuario_data, form=None, fotos=fotos)  

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


@app.route('/feed')
@login_required
def feed():
    fotos = Foto.query.filter_by(deleted=False).order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos=fotos)

@app.route('/excluir_foto/<id>')
@login_required
def excluir_foto(id):
    foto = Foto.query.get_or_404(id)
    if current_user == foto.usuario:
        print("O usuario é o dono da foto")
        foto.deleted = True
        database.session.commit()
        return redirect(url_for('user_profile'))
    else:
        print("Não é o dono da foto")
        return redirect(url_for('user_profile'))
    
@app.route('/foto/<id>')
@login_required
def visualizar_foto(id):
    foto = Foto.query.get_or_404(id)
    if foto.deleted == False:
        return render_template('foto.html', foto=foto)
    else:
        return redirect(url_for('feed'))