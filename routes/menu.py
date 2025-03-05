from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja,Usuarios,Cliente,Endereco,Administrador,Produto,Produto_Loja
from sqlalchemy import func
import services.validacoes as validacoes
menu_bp = Blueprint('menu', __name__)



@menu_bp.route('/escolha')
def escolha():
    verificar = validacoes.verificarCadastro()
    if verificar:  
        return verificar
    
    verificarUsuario = validacoes.verificarUsuario()
    if verificarUsuario:
        return verificarUsuario
    mensagem = request.args.get('menu/mensagem', "")
    
    return render_template('menu/clienteLoja.html', mensagem=mensagem)

@menu_bp.route('/principal')
def principal():
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        typeUser = session['typeUser']
        mensagem = request.args.get('mensagem', "")
        pesquisa = request.args.get('pesquisa',"")
        R = 6371
        distancia = None


        if pesquisa != "" and typeUser != 1: 
            distancia = func.round(  
                R * func.acos(
                    func.cos(func.radians(session["lat"])) * func.cos(func.radians(Endereco.latitude)) *
                    func.cos(func.radians(Endereco.longitude) - func.radians(session["long"])) +
                    func.sin(func.radians(session["lat"])) * func.sin(func.radians(Endereco.latitude))
                ),
                2  
            ).label("distancia")

            produtos_lojas = db.session.query(
                Produto_Loja, Loja, Produto, Endereco, distancia
            ) \
                .join(Loja, Produto_Loja.id_loja == Loja.id_loja) \
                .join(Produto, Produto_Loja.id_produto == Produto.id_produto) \
                .join(Endereco, Endereco.id_usuario == Loja.id_usuario) \
                .filter(Produto.nome_produto.ilike(f"%{pesquisa}%")) \
                .order_by(distancia).limit(20) \
                .all()
        elif pesquisa != "": 
            produtos_lojas = db.session.query(
                Produto_Loja, Loja, Produto
            ) \
                .join(Loja, Produto_Loja.id_loja == Loja.id_loja) \
                .join(Produto, Produto_Loja.id_produto == Produto.id_produto) \
                .filter(Produto.nome_produto.ilike(f"%{pesquisa}%")) \
                .limit(20) \
                .all()
        else:
             produtos_lojas = db.session.query(Produto_Loja, Loja, Produto) \
            .join(Loja, Produto_Loja.id_loja == Loja.id_loja) \
            .join(Produto, Produto_Loja.id_produto == Produto.id_produto) \
            .order_by(func.random()) \
            .limit(20) \
            .all()
            
        return render_template('menu/menu.html', mensagem=mensagem,typeUser = typeUser,produtos_lojas = produtos_lojas,pesquisa = pesquisa)

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
            dados = Cliente.query.filter_by(id_usuario = session['user_id']).first()
        if not dados:
            return redirect(url_for('menu.principal', mensagem="Não encontramos um Cliente ou Loja vinculado ao seu Usuário",typeUser = typeUser))
        endereco = Endereco.query.filter_by(id_usuario=session['user_id']).first()


            
        return render_template('menu/dados.html', mensagem=mensagem,typeUser = session['typeUser'],dados = dados,endereco = endereco)

    except Exception as e:
        session.clear()
        return redirect(url_for('auth.inicio',mensagem = f"Erro ao acessar o Sistema {e}"))




