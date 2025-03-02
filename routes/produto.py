from flask import Blueprint, render_template, request, redirect, url_for, session,current_app
from classes import db,Produto,Produto_Loja,Loja
import os

import services.validacoes as validacoes
produto_bp = Blueprint('produto', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@produto_bp.route('/produtos')
def produtos():
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        typeUser = session['typeUser']
        if typeUser != 1 and typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
            
        mensagem = request.args.get('mensagem', "")

        produtos = Produto.query.all()
        produtos_loja = None
        if typeUser == 2:
            loja = Loja.query.filter_by(id_usuario=session['user_id']).first()

            produtos_loja = (
                db.session.query(Produto,Produto_Loja)
                .join(Produto_Loja, Produto.id_produto == Produto_Loja.id_produto)
                .join(Loja, Produto_Loja.id_loja == loja.id_loja)
                .all()
            )

        return render_template('menu/produtos.html', mensagem=mensagem,produtos = produtos, produtos_loja = produtos_loja,typeUser = session['typeUser'])
    except:
        return redirect(url_for('menu.principal',mensagem = "Algo deu errado, tente novamente"))

@produto_bp.route('/vizualizar/<id>')
def vizualizar(id):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        
        if session['typeUser'] != 1 and session['typeUser'] != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))

        mensagem = request.args.get('mensagem', "")
        produto = Produto.query.get(id)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
                
        return render_template('menu/vizualizarProduto.html', mensagem=mensagem,produto = produto)
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))


@produto_bp.route('/cadastro')
def cadastro():
    try:

        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")


        return render_template('menu/criarProduto.html', mensagem=mensagem)
    except:
        return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

@produto_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")

        nome = request.form['name']
        file = request.files["imagem"]

        if not nome or len(nome) < 3:
            return redirect(url_for("produto.cadastro", mensagem = "Nome do produto inválido"))

        if not file:
            return redirect(url_for("produto.cadastro", mensagem = "Imagem é obrigatória"))
        if not allowed_file(file.filename):
            return redirect(url_for("produto.cadastro", mensagem = "Formato de imagem inválido. Use PNG, JPG ou JPEG."))
        filename = file.filename
        # Salva o arquivo na pasta de uploads
        file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        # Armazena o nome da imagem em um arquivo de texto
        with open("imagens.txt", "a") as f:
            f.write(filename + "\n")
        novo_produto = Produto(nome_produto = nome, img = filename)
        db.session.add(novo_produto)
        db.session.commit()
        return redirect(url_for('produto.produtos',mensagem = "Produto Cadastrado com Sucesso"))
    except:
        return redirect(url_for('produto.cadastro',mensagem = "Algo deu errado, tente novamente"))

@produto_bp.route('/excluir/<id>',methods=['POST'])
def excluir(id):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")

        produto = Produto.query.get(id)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

        db.session.delete(produto)
        db.session.commit()
      

      
        return redirect(url_for('produto.produtos', mensagem = "Produto deletado com sucesso"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
    
@produto_bp.route('/editar/<id>',methods=['POST'])
def editar(id):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")

        produto = Produto.query.get(id)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

        return render_template('menu/criarProduto.html', mensagem=mensagem,produto = produto)

    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
    
@produto_bp.route('/update/<id>',methods=['POST'])
def update(id):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")

        produto = Produto.query.get(id)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
        
        nome = request.form['name']
        file = request.files["imagem"]

        if not nome or len(nome) < 3:
            return redirect(url_for("produto.cadastro", mensagem = "Nome do produto inválido"))

        if file:
            if not allowed_file(file.filename):
                return redirect(url_for("produto.cadastro", mensagem = "Formato de imagem inválido. Use PNG, JPG ou JPEG."))
            filename = file.filename
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
             # Armazena o nome da imagem em um arquivo de texto
            with open("imagens.txt", "a") as f:
                f.write(filename + "\n")
            produto.img = filename
        produto.nome_produto = nome
        db.session.commit()
        return redirect(url_for('produto.produtos',mensagem = "Produto Editado com Sucesso"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        