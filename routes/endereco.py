from flask import Blueprint, render_template, request, redirect, url_for, session

endereco_bp = Blueprint('endereco', __name__)

import validacoes

@endereco_bp.route('/cadastro')
def cadastro():
    
    verificar = validacoes.verificarCadastro()
    if verificar:
        return verificar
    verificarLojaCliente = validacoes.verificarLojaCliente()
    if verificarLojaCliente:
        return verificarLojaCliente
     
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroEnd.html',erro = erro)

@endereco_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:

        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        
        verificarLojaCliente = validacoes.verificarLojaCliente()
        if verificarLojaCliente:
            return verificarLojaCliente
        
        erro = request.args.get('erro')
        if erro == None:
            erro = ""
    except:
        return render_template('cadastroEnd.html',erro = "Algo deu errado, tente novamente")
