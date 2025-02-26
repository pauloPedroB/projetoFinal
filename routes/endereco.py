from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Endereco

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
        if(Endereco.query.filter_by(id_usuario = session['user_id']).first()):
            return redirect(url_for('endereco.cadastro',erro = "Já existe um endereço vinculado à esse usuário, se precisa atualizar esse endereço, atualize-o na página de perfil"))
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
    
def validarCadastroEndereco(cep,rua, numero, bairro, complemento, uf):
    print('/Tem que fazer')

