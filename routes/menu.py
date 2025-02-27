from flask import Blueprint, render_template, request, redirect, url_for, session

import validacoes
menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/escolha')
def escolha():
    verificar = validacoes.verificarCadastro()
    if verificar:  
        return verificar
    
    verificarUsuario = validacoes.verificarUsuario()
    if verificarUsuario:
        return verificarUsuario
    mensagem = request.args.get('mensagem', "")
    
    return render_template('clienteLoja.html', mensagem=mensagem)

@menu_bp.route('/principal')
def principal():
 

    cadastro = validacoes.verificarCadastroCompleto()
    if cadastro:
        return cadastro
    
    mensagem = request.args.get('mensagem', "")
    
    return render_template('menu.html', mensagem=mensagem)
