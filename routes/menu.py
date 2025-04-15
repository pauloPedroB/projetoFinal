from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja,Endereco,Produto,Produto_Loja
from sqlalchemy import func
import services.validacoes as validacoes
import string
from sqlalchemy import or_
import nltk
from nltk.corpus import stopwords,wordnet
from controllers import clienteController,produto_lojaController


nltk.download('stopwords')
nltk.download("omw-1.4")
nltk.download("wordnet")
nltk.download("wordnet_ic")


menu_bp = Blueprint('menu', __name__)

def encontrar_sinonimos(palavra):
    sinonimos = set()
    for synset in wordnet.synsets(palavra, lang="por"):  # Busca em português
        for lemma in synset.lemmas(lang="por"):
            sinonimos.add(lemma.name())
    return list(sinonimos)

def pesquisar(pesquisa,categoria = None):
    #Removendo pontuações
    pesquisa = pesquisa.translate(str.maketrans('', '', string.punctuation))

    palavras = pesquisa.split()
    stop_words = set(stopwords.words('portuguese'))
    palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stop_words]
    palavras_final = []
    
    for palavra in palavras_filtradas:
        sinonimos = encontrar_sinonimos(palavra)
        for sinonimo in sinonimos:
            sinonimo = sinonimo.replace("_", " ")
            partes = sinonimo.split()
            for parte in partes:
                if parte not in stop_words:
                    palavras_final.append(parte.lower())
        if parte not in stop_words:
            palavras_final.append(palavra)
    
    palavras_final = list(dict.fromkeys(palavras_final))
 
    

    print(palavras_final)

    produtos,recado = produto_lojaController.listar(session['user_id'],palavras_final,categoria)
    return produtos


@menu_bp.route('/escolha')
def escolha():
    verificar = validacoes.verificarCadastro()
    if verificar:  
        return verificar
    
    verificarUsuario,usuario = validacoes.verificarUsuario()
    if verificarUsuario:
        return verificarUsuario
    mensagem = request.args.get('menu/mensagem', "")
    
    return render_template('menu/clienteLoja.html', mensagem=mensagem)

@menu_bp.route('/principal')
def principal():
    try:
        mensagem = request.args.get('mensagem', "")

        cadastro = validacoes.verificarCadastroCompleto(mensagem)
        if cadastro:
            return cadastro
        pesquisa = request.args.get('pesquisa',"")
       
        if pesquisa != "": 
           produtos_lojas = pesquisar(pesquisa)
           print(produtos_lojas)      
        else:
             produtos_lojas = db.session.query(Produto_Loja, Loja, Produto) \
            .join(Loja, Produto_Loja.id_loja == Loja.id_loja) \
            .join(Produto, Produto_Loja.id_produto == Produto.id_produto) \
            .order_by(func.random()) \
            .limit(20) \
            .all()
        categorias = db.session.query(Produto.categoria).distinct().all()
        categorias_unicas = [c[0] for c in categorias]
        typeUser = session['typeUser']

            
        return render_template('menu/menu.html', mensagem=mensagem,typeUser = typeUser,produtos_lojas = produtos_lojas,pesquisa = pesquisa,categorias = categorias_unicas)

    except Exception as e:
        session.clear()
        return redirect(url_for('auth.inicio',mensagem = f"Erro ao acessar o Sistema {e}"))
    
@menu_bp.route('/dados')
def dados():
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        typeUser = session['typeUser']
        mensagem = request.args.get('mensagem', "")
        if typeUser == 1:
            return redirect(url_for('menu.principal', mensagem="Você não possuí acesso a essa página",typeUser = typeUser))

        if typeUser == 2:
            dados = Loja.query.filter_by(id_usuario = session['user_id']).first()
        if typeUser == 3:
            dados, mensagem = clienteController.buscar({"id_usuario": session['user_id']})
        if not dados:
            return redirect(url_for('menu.principal', mensagem="Não encontramos um Cliente ou Loja vinculado ao seu Usuário",typeUser = typeUser))
        endereco = Endereco.query.filter_by(id_usuario=session['user_id']).first()


            
        return render_template('menu/dados.html', mensagem=mensagem,typeUser = session['typeUser'],dados = dados,endereco = endereco)

    except Exception as e:
        session.clear()
        return redirect(url_for('auth.inicio',mensagem = f"Erro ao acessar o Sistema {e}"))




