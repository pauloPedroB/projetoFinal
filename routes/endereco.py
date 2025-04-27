from flask import Blueprint, render_template, request, redirect, url_for, session
from controllers import EnderecoController,userController
from models.Endereco import Endereco
from models.Usuario import Usuario


endereco_bp = Blueprint('endereco', __name__)

import services.validacoes as validacoes

@endereco_bp.route('/cadastro')
def cadastro():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        mensagem = request.args.get('mensagem', "")

        lojaCliente = validacoes.verificarLojaCliente(mensagem)
        if type(lojaCliente) != Usuario:
            return lojaCliente
        endereco,mensagem = EnderecoController.buscar()
        usuario,mensagem = userController.buscar({'id_user': session['user_id']})

        if  endereco != None:
            return redirect(url_for('menu.principal'))
        elif usuario.typeUser == 1:
            return redirect(url_for('menu.principal'))
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroEnd.html',mensagem = mensagem)
    except Exception as e:
        return redirect(url_for('menu.principal', mensagem = f"Algo deu errado, tente novamente: {e}"))


@endereco_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        mensagem = request.args.get('mensagem', "")
        
        lojaCliente = validacoes.verificarLojaCliente(mensagem)
        if type(lojaCliente) != Usuario:
            return lojaCliente
    
        cep = request.form['CEP']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        uf = request.form['uf']
        cidade = request.form['cidade']
        complemento = request.form['complemento']
        
        
        
        usuario,mensagem = userController.buscar({'id_user': session['user_id']})
        
        endereco = Endereco(
                        id=None,
                        rua = rua,
                        bairro = bairro,
                        cidade = cidade,
                        cep = cep,
                        complemento = complemento,
                        uf = uf,
                        nmr = numero,
                        latitude= None,
                        longitude= None,
                        usuario = usuario
                        )
        novo_endereco,mensagem = EnderecoController.criar(endereco)
        if(novo_endereco == None):
            return redirect(url_for('endereco.cadastro',mensagem = f"Não foi possível cadastrar o Endereco, {mensagem}"))
        
        return redirect(url_for('menu.principal'))
    except Exception as e:
        return redirect(url_for('endereco.cadastro', mensagem = f"Algo deu errado, tente novamente: {e}"))

@endereco_bp.route('/editar/<id_endereco>')
def editar(id_endereco):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        
        if session['typeUser'] == 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso à essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        if str(endereco.id) != id_endereco:
            return redirect(url_for('menu.principal',mensagem = "Você não tem permissão para editar este endereço"))
                
        return render_template('cadastroEnd.html',mensagem = mensagem, endereco = endereco)
    except Exception as e:
            return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))
       
@endereco_bp.route('/update/<id_endereco>',methods=['POST'])
def update(id_endereco):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario

        if session['typeUser'] == 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso à essa página"))
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        
        cep = request.form['CEP']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        uf = request.form['uf']
        cidade = request.form['cidade']
        complemento = request.form['complemento']

        endereco.cep = cep
        endereco.rua = rua
        endereco.nmr = numero
        endereco.bairro = bairro
        endereco.uf = uf
        endereco.cidade = cidade
        endereco.complemento = complemento
        novo_endereco,mensagem = EnderecoController.editar(endereco)
        if(novo_endereco == None):
            return redirect(url_for('endereco.cadastro',mensagem = f"Não foi possível editar o Endereco, {mensagem}"))

        return redirect(url_for('menu.dados',mensagem = "Endereco editado"))

    except Exception as e:
            return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))
    