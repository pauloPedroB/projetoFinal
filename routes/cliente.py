from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db, Cliente
import re
import services.validacoes as validacoes
from controllers.userController import alterarTipo

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/cadastro')
def cadastro():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarUsuario,usuario = validacoes.verificarUsuario()
        if verificarUsuario:
            return verificarUsuario
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroCliente.html',mensagem = mensagem)
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))


@cliente_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarUsuario,usuario = validacoes.verificarUsuario()
        if verificarUsuario:
            return verificarUsuario
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
        
        usuario.typeUser = 3
        retorno, mensagem = alterarTipo(usuario)
        if(retorno == False):
            return redirect(url_for('cliente.cadastro',mensagem = f"Não foi possível vincular seu usuário a um cliente, {mensagem}"))

        session['typeUser'] = usuario.typeUser
        novo_Cliente = Cliente(cpf=cpf, dtNascimento = dtNascimento, nome = nome, telefone = telefone, genero = genero, carro = carro, id_usuario = usuario.id_usuario)
        print(novo_Cliente)
        db.session.add(novo_Cliente)
        db.session.commit()
        return redirect(url_for('endereco.cadastro'))
    
    except Exception as e:
        return redirect(url_for('cliente.cadastro',mensagem = f"Algo deu errado, tente novamente: {e}"))
    
@cliente_bp.route('/editar/<id_cliente>')
def editar(id_cliente):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        
        cliente = Cliente.query.get(id_cliente)
        if not cliente:
            return redirect(url_for('menu.Principal',mensagem = "Cliente não encontrado"))
        
        
        if cliente.id_usuario != session['user_id']:
            return redirect(url_for('menu.Principal',mensagem = "Você não tem permissão para editar este Perfil"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroCliente.html',mensagem = mensagem,cliente = cliente)
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))

