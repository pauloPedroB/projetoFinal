from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db, Cliente,Usuarios
import re
import services.validacoes as validacoes

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/cadastro')
def cadastro():
    verificar = validacoes.verificarCadastro()
    if verificar:
        return verificar
    verificarLojaCliente = validacoes.verificarUsuario()
    if verificarLojaCliente:
        return verificarLojaCliente
    
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""
    return render_template('cadastroCliente.html',mensagem = mensagem)

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

        cpf = re.sub(r'\D', '', cpf)

        cadastro,mensagem = validacoes.validar_cadastroCliente(cpf,nome,telefone,dtNascimento,genero,carro)
        if cadastro == False:
            return redirect(url_for('cliente.cadastro',mensagem = mensagem))
        elif(Cliente.query.filter_by(cpf=cpf).first()):
            return redirect(url_for('cliente.cadastro',mensagem = "Já possuí um cliente cadastrado com esse CPF"))
        usuario = Usuarios.query.filter(Usuarios.id_usuario == session['user_id']).first()
        usuario.typeUser = 3
        session['typeUser'] = usuario.typeUser

        
        novo_Cliente = Cliente(cpf=cpf, dtNascimento = dtNascimento, nome = nome, telefone = telefone, genero = genero, carro = carro, id_usuario = session['user_id'])
        db.session.add(novo_Cliente)
        db.session.commit()
        return redirect(url_for('endereco.cadastro'))
    
    except:
        return redirect(url_for('cliente.cadastro',mensagem = "Algo deu errado, tente novamente"))

