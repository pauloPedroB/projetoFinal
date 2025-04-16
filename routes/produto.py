from flask import Blueprint, render_template, request, redirect, url_for, session,current_app
from models.Produto import Produto
import os
import string
import nltk
from nltk.corpus import stopwords,wordnet
from controllers import produtoController,produto_lojaController,lojaController
from models.Usuario import Usuario


nltk.download('stopwords')
nltk.download("omw-1.4")
nltk.download("wordnet")
nltk.download("wordnet_ic")



import services.validacoes as validacoes
produto_bp = Blueprint('produto', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def encontrar_sinonimos(palavra):
    sinonimos = set()
    for synset in wordnet.synsets(palavra, lang="por"):  # Busca em português
        for lemma in synset.lemmas(lang="por"):
            sinonimos.add(lemma.name())
    return list(sinonimos)



def pesquisar(pesquisa, categoria = None):
    #Removendo pontuações
    pesquisa = pesquisa.translate(str.maketrans('', '', string.punctuation))

    pesquisa = pesquisa.lower()


    palavras = pesquisa.split()
    palavras = list(dict.fromkeys(palavras))


    stop_words = set(stopwords.words('portuguese'))
    palavras_filtradas = [palavra for palavra in palavras if palavra not in stop_words]
    print(palavras_filtradas)
    palavras_final = []
    
    for palavra in palavras_filtradas:
        sinonimos = encontrar_sinonimos(palavra)
        for sinonimo in sinonimos:
            sinonimo = sinonimo.replace("_", " ")
            partes = sinonimo.split()
            for parte in partes:
                if parte not in stop_words:
                    palavras_final.append(parte.lower())
        if palavra not in stop_words:
            palavras_final.append(palavra)
    
    palavras_final = list(dict.fromkeys(palavras_final))

    print(palavras_final)

    produtos,recado = produtoController.listar(palavras_final,categoria)
    
    return produtos

@produto_bp.route('/produtos')
def produtos():
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        typeUser = session['typeUser']
        if typeUser != 1 and typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
            
        mensagem = request.args.get('mensagem', "")
        pesquisa = request.args.get('pesquisa',"")
        categoria = request.args.get('categoria',"0")


        if pesquisa != "" and categoria != "0":
            produtos = pesquisar(pesquisa,categoria)
        elif categoria != "0":
            produtos,recado = produtoController.listar([], categoria)
        elif pesquisa:
           produtos = pesquisar(pesquisa)
        else:
            produtos,recado = produtoController.listar([])

        produtos_loja = None
        if typeUser == 2:
            loja, recado = lojaController.buscar({"id_usuario": session['user_id']})
            if loja == None:
                return redirect(url_for('menu.principal',mensagem = "Loja não encontrada"))

            produtos_loja, recado = produto_lojaController.listarProdutoLoja(loja.id_loja,session['user_id'])
        #categorias = db.session.query(Produto.categoria).distinct().all()
        #categorias_unicas = [c[0] for c in categorias]
        categorias_unicas = []
        return render_template('menu/produtos.html', mensagem=mensagem,produtos = produtos, produtos_loja = produtos_loja,typeUser = session['typeUser'],categorias = categorias_unicas,pesquisa = pesquisa,categoria = categoria)
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))

@produto_bp.route('/vizualizar/<id>')
def vizualizar(id):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        
        if session['typeUser'] != 1 and session['typeUser'] != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))

        mensagem = request.args.get('mensagem', "")
        produto, mensagem = produtoController.buscar({'id_produto': id})
        if produto == None:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
                
        return render_template('menu/vizualizarProduto.html', mensagem=mensagem,produto = produto)
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))


@produto_bp.route('/cadastro')
def cadastro():
    try:

        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")


        return render_template('menu/criarProduto.html', mensagem=mensagem)
    except:
        return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

@produto_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
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
        produto = Produto(
                nome_produto= nome,
                categoria="qualquer", #arrumar isso
                img= filename,
                )
        criar, mensagem = produtoController.criar(produto)
        if(criar == False):
            return redirect(url_for('produto.cadastro',mensagem = f'O Produto não foi criado: {mensagem}'))

        return redirect(url_for('produto.produtos',mensagem = "Produto Cadastrado com Sucesso"))
    except:
        return redirect(url_for('produto.cadastro',mensagem = "Algo deu errado, tente novamente"))

@produto_bp.route('/excluir/<id>',methods=['POST'])
def excluir(id):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")
        produto, mensagem = produtoController.buscar({'id_produto': id})

        if produto == None:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

        excluir, mensagem = produtoController.excluir(produto)
        if (excluir == False):
            return redirect(url_for('produto.produtos',mensagem = f"Produto não excluído: {mensagem}"))

        return redirect(url_for('produto.produtos', mensagem = "Produto deletado com sucesso"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
    
@produto_bp.route('/editar/<id>',methods=['POST'])
def editar(id):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")

        produto, mensagem = produtoController.buscar({'id_produto': id})
        if produto == None:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))

        return render_template('menu/criarProduto.html', mensagem=mensagem,produto = produto)

    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
    
@produto_bp.route('/update/<id>',methods=['POST'])
def update(id):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        if session['typeUser'] != 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso de administrador"))
            
        mensagem = request.args.get('mensagem', "")
        produto, mensagem = produtoController.buscar({'id_produto': id})
        if produto == None:
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
        editar, mensagem = produtoController.editar(produto)
        if (editar == False):
            return redirect(url_for('produto.produtos',mensagem = f"Produto não editado: {mensagem}"))
        return redirect(url_for('produto.produtos',mensagem = "Produto Editado com Sucesso"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        