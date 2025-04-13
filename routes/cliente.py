from flask import Blueprint, render_template, request, redirect, url_for, session
import re
import services.validacoes as validacoes
from controllers import clienteController,userController
from models.Cliente import Cliente


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
                
        

        cliente = Cliente(
            id_cliente=None,
            cpf=cpf,
            nome=nome,
            telefone = telefone,
            dtNascimento=dtNascimento,
            genero = genero,
            carro = carro,
            usuario = usuario,
        )
        novo_Cliente,mensagem = clienteController.criar(cliente)
        if(novo_Cliente == None):
            return redirect(url_for('cliente.cadastro',mensagem = f"Não foi possível cadastrar o Cliente, {mensagem}"))
        usuario.typeUser = 3
        session['typeUser'] = usuario.typeUser
        
        return redirect(url_for('endereco.cadastro'))
    
    except Exception as e:
        return redirect(url_for('cliente.cadastro',mensagem = f"Algo deu errado, tente novamente: {e}"))
    
@cliente_bp.route('/editar/<id_cliente>')
def editar(id_cliente):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        cliente, mensagem = clienteController.buscar({"id_cliente": id_cliente})
        if not cliente:
            return redirect(url_for('menu.principal',mensagem = "Cliente não encontrado"))
        
        if cliente.usuario.id_usuario != session['user_id']:
            return redirect(url_for('menu.principal',mensagem = "Você não tem permissão para editar este Perfil"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroCliente.html',mensagem = mensagem,cliente = cliente)
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))

