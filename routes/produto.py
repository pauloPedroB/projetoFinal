from flask import Blueprint, render_template, request, redirect, url_for, session,current_app
from classes import db,Produto
import os

import services.validacoes as validacoes
produto_bp = Blueprint('produto', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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
        
    erro = request.args.get('erro', "")


    return render_template('menu/criarProduto.html', erro=erro)

@produto_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return render_template('menu/menu.html', mensagem="Você não possuí acesso de administrador",typeUser = session['typeUser'])
            
        mensagem = request.args.get('mensagem', "")

        nome = request.form['name']
        file = request.files["imagem"]

        if not nome or len(nome) < 3:
            return redirect(url_for("produto.cadastro", erro = "Nome do produto inválido"))

        if not file:
            return redirect(url_for("produto.cadastro", erro = "Imagem é obrigatória"))
        if not allowed_file(file.filename):
            return redirect(url_for("produto.cadastro", erro = "Formato de imagem inválido. Use PNG, JPG ou JPEG."))
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
    except:
        return redirect(url_for('produto.cadastro',erro = "Algo deu errado, tente novamente"))

@produto_bp.route('/excluir/<id>',methods=['POST'])
def excluir(id):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return render_template('menu/menu.html', mensagem="Você não possuí acesso de administrador",typeUser = session['typeUser'])
            
        mensagem = request.args.get('mensagem', "")

        produto = Produto.query.get(id)
        if not produto:
            return redirect(url_for('produto.produtos',erro = "Produto não encontrado"))

        db.session.delete(produto)
        db.session.commit()
      

      
        return redirect(url_for('produto.produtos', erro = "Produto deletado com sucesso"))
    except:
        return redirect(url_for('produto.cadastro',erro = "Algo deu errado, tente novamente"))

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        