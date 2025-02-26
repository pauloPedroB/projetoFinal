from flask import Blueprint, render_template, request, redirect, url_for, session,current_app
from classes import db,Produto
import os

import services.validacoes as validacoes
produto_bp = Blueprint('produto', __name__)


@produto_bp.route('/vizualizar')
def produtos():
 

    cadastro = validacoes.verificarCadastroCompleto()
    if cadastro:
        return cadastro
    
    if session['typeUser'] != 1:
        return render_template('menu/menu.html', mensagem="Você não possuí acesso de administrador",typeUser = session['typeUser'])
        
    mensagem = request.args.get('mensagem', "")

    produtos = Produto.query.all()

    return render_template('menu/produtos.html', mensagem=mensagem,produtos = produtos)

@produto_bp.route('/cadastro')
def cadastro():
 

    cadastro = validacoes.verificarCadastroCompleto()
    if cadastro:
        return cadastro
    
    if session['typeUser'] != 1:
        return render_template('menu/menu.html', mensagem="Você não possuí acesso de administrador",typeUser = session['typeUser'])
        
    mensagem = request.args.get('mensagem', "")


    return render_template('menu/criarProduto.html', erro=mensagem)

@produto_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    cadastro = validacoes.verificarCadastroCompleto()
    if cadastro:
        return cadastro
    if session['typeUser'] != 1:
        return render_template('menu/menu.html', mensagem="Você não possuí acesso de administrador",typeUser = session['typeUser'])
        
    mensagem = request.args.get('mensagem', "")

    nome = request.form['name']
    file = request.files["imagem"]

    if file:
        filename = file.filename
        # Salva o arquivo na pasta de uploads
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        # Armazena o nome da imagem em um arquivo de texto
        with open("imagens.txt", "a") as f:
            f.write(filename + "\n")

        novo_produto = Produto(nome_produto = nome, img = filename)
        db.session.add(novo_produto)
        db.session.commit()

    return redirect(url_for('produto.produtos'))