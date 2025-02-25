from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja
import re
import validacoes

loja_bp = Blueprint('loja', __name__)

@loja_bp.route('/cadastro')
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
    return render_template('cadastroLoja.html',erro = erro)

@loja_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarLojaCliente = validacoes.verificarUsuario()
        if verificarLojaCliente:
            return verificarLojaCliente
        cnpj_user = request.form['CNPJ']
        nomeFantasia = request.form['nomeFantasia']
        razaoSocial = request.form['razaoSocial']
        telefone = request.form['telefone']
        celular = request.form['celular']
        abertura = request.form['abertura']

        cadastro,mensagem = validacoes.validar_cadastroLoja(cnpj_user,nomeFantasia,razaoSocial,telefone,celular,abertura)
        if cadastro == False:
            return redirect(url_for('loja.cadastro',erro = mensagem))
        elif(Loja.query.filter_by(cnpj=cnpj_user).first()):
            return redirect(url_for('loja.cadastro',erro = "Já possuí uma loja vinculada com esse CNPJ"))
        cnpj_user = re.sub(r'\D', '', cnpj_user)
        nova_loja = Loja(cnpj=cnpj_user, nomeFantasia = nomeFantasia, razaoSocial = razaoSocial, telefone = telefone, celular = celular, abertura = abertura, id_usuario = session['user_id'])
        db.session.add(nova_loja)
        db.session.commit()

        return redirect(url_for('menu'))
        
    except:
        return redirect(url_for('loja.cadastro',erro = "Algo deu errado, tente novamente"))

