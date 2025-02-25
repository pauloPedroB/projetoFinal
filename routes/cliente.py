from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja, Cliente

import validacoes

cliente_bp = Blueprint('cliente', __name__)





@cliente_bp.route('/cadastro')
def cadastro():
    verificar = validacoes.verificarCadastro()
    if verificar:
        return verificar
    verificarLojaCliente = validacoes.verificarUsuario()
    if verificarLojaCliente:
        return verificarLojaCliente
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroCliente.html',erro = erro)

@cliente_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarLojaCliente = validacoes.verificarUsuario()
        if verificarLojaCliente:
            return verificarLojaCliente
        cpf = request.form['CPF']
        nome = request.form['name']
        dtNascimento = request.form['data']
        telefone = request.form['telefone']
        genero = request.form['genero']
        carro = request.form['carro']

        cadastro,mensagem = validacoes.validar_cadastroCliente(cpf,nome,telefone,dtNascimento,genero,carro)
        if cadastro == False:
            return redirect(url_for('cliente.cadastro',erro = mensagem))
        elif(Cliente.query.filter_by(cpf=cpf).first()):
            return redirect(url_for('cliente.cadastro',erro = "Já possuí um cliente cadastrado com esse CPF"))
        novo_Cliente = Cliente(cpf=cpf, dtNascimento = dtNascimento, nome = nome, telefone = telefone, genero = genero, carro = carro, id_usuario = session['user_id'])
        db.session.add(novo_Cliente)
        db.session.commit()
        return redirect(url_for('menu'))
    
    except:
        return redirect(url_for('cliente.cadastro',erro = "Algo deu errado, tente novamente"))

