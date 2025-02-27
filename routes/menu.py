from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja,Usuarios,Cliente,Endereco,Administrador,Produto

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
 

    cadastro = validacoes.verificarCadastroCompleto()
    if cadastro:
        return cadastro
    
    mensagem = request.args.get('mensagem', "")

    
    #dados = []
    #if session['typeUser'] == 1:
     #   dados = Administrador.query.filter_by(id_usuario=session['user_id']).first()
    #elif session['typeUser']:
     #   dados = Loja.query.filter_by(id_usuario=session['user_id']).first()
    #else:
     #   dados = Cliente.query.filter_by(id_usuario=session['user_id']).first()

    return render_template('menu/menu.html', mensagem=mensagem,typeUser = session['typeUser'])




