from flask import Blueprint, render_template, request, redirect, url_for, session

endereco_bp = Blueprint('endereco', __name__)

import validacoes

@endereco_bp.route('/cadastro')
def cadastro():
    
    verificar = validacoes.verificarCadastro()
    if verificar:
        return verificar

     
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroEnd.html',erro = erro)