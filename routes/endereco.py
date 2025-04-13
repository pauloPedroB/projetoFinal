from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Administrador
import requests
import re
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic
from controllers import EnderecoController,userController
from models.Endereco import Endereco



endereco_bp = Blueprint('endereco', __name__)

import services.validacoes as validacoes

@endereco_bp.route('/cadastro')
def cadastro():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarLojaCliente = validacoes.verificarLojaCliente()
        if verificarLojaCliente:
            return verificarLojaCliente
        endereco,mensagem = EnderecoController.buscar({'id_usuario': session['user_id']})
        if  endereco != None or Administrador.query.filter_by(id_usuario=session['user_id']).first():
            return redirect(url_for('menu.principal'))
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroEnd.html',mensagem = mensagem)
    except Exception as e:
            return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))


@endereco_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        
        verificarLojaCliente = validacoes.verificarLojaCliente()
        if verificarLojaCliente:
            return verificarLojaCliente
    
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
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro
        
        if session['typeUser'] == 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso à essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        endereco,mensagem = EnderecoController.buscar({'id_endereco': id_endereco})
        if endereco == None:
            return redirect(url_for('menu.principal',mensagem = "Endereço não encontrado"))
        
        if endereco.usuario.id_usuario != session['user_id']:
            return redirect(url_for('menu.principal',mensagem = "Você não tem permissão para editar este endereço"))
                
        return render_template('cadastroEnd.html',mensagem = mensagem, endereco = endereco)
    except Exception as e:
            return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))
       
@endereco_bp.route('/update/<id_endereco>',methods=['POST'])
def update(id_endereco):
    try:
        cadastro = validacoes.verificarCadastroCompleto()
        if cadastro:
            return cadastro

        if session['typeUser'] == 1:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso à essa página"))
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""

        endereco,mensagem = EnderecoController.buscar({'id_endereco': id_endereco})
        if not endereco:
            return redirect(url_for('menu.Principal',mensagem = "Endereço não encontrado"))
        
        cep = request.form['CEP']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        uf = request.form['uf']
        cidade = request.form['cidade']
        complemento = request.form['complemento']

        usuario,mensagem = userController.buscar({'id_user': session['user_id']})
        endereco.cep = cep
        endereco.rua = rua
        endereco.nmr = numero
        endereco.bairro = bairro
        endereco.uf = uf
        endereco.cidade = cidade
        endereco.complemento = complemento
        endereco.usuario = usuario
        novo_endereco,mensagem = EnderecoController.editar(endereco)
        if(novo_endereco == None):
            return redirect(url_for('endereco.cadastro',mensagem = f"Não foi possível editar o Endereco, {mensagem}"))

        return redirect(url_for('menu.dados',mensagem = "Endereco editado"))

    except Exception as e:
            return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))
    