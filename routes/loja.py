from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Loja,Usuarios,Produto,Produto_Loja,Endereco
import re
import services.validacoes as validacoes
from geopy.distance import geodesic

loja_bp = Blueprint('loja', __name__)

@loja_bp.route('/cadastro')
def cadastro():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarUsuario = validacoes.verificarUsuario()
        if verificarUsuario:
            return verificarUsuario
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        return render_template('cadastroLoja.html',mensagem = mensagem)
    except:
        return redirect(url_for('menu.escolha',mensagem = "Algo deu errado, tente novamente"))


@loja_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarUsuario = validacoes.verificarUsuario()
        if verificarUsuario:
            return verificarUsuario
        
        cnpj_user = request.form['CNPJ']
        nomeFantasia = request.form['nomeFantasia']
        razaoSocial = request.form['razaoSocial']
        telefone = request.form['telefone']
        celular = request.form['celular']
        abertura = request.form['abertura']
        cnpj_user = re.sub(r'\D', '', cnpj_user)

        cadastro,mensagem = validacoes.validar_cadastroLoja(cnpj_user,nomeFantasia,razaoSocial,telefone,celular,abertura)
        if cadastro == False:
            return redirect(url_for('loja.cadastro',mensagem = mensagem))
        elif(Loja.query.filter_by(cnpj=cnpj_user).first()):
            return redirect(url_for('loja.cadastro',mensagem = "Já possuí uma loja vinculada com esse CNPJ"))
        usuario = Usuarios.query.filter(Usuarios.id_usuario == session['user_id']).first()
        usuario.typeUser = 2
        session['typeUser'] = usuario.typeUser

        nova_loja = Loja(cnpj=cnpj_user, nomeFantasia = nomeFantasia, razaoSocial = razaoSocial, telefone = telefone, celular = celular, abertura = abertura, id_usuario = session['user_id'])
        db.session.add(nova_loja)
        db.session.commit()

        return redirect(url_for('endereco.cadastro'))
        
    except:
        return redirect(url_for('loja.cadastro',mensagem = "Algo deu errado, tente novamente"))

@loja_bp.route('/vincular/<id_produto>',methods=['POST'])
def vincular(id_produto):
    try:
        verificar = validacoes.verificarCadastroCompleto()
        if verificar:
            return verificar
        
        typeUser = session['typeUser']
        if typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        loja = Loja.query.filter_by(id_usuario=session['user_id']).first()
        if not loja:
            return redirect(url_for('produto.produtos',mensagem = "Loja não encontrada"))
        produto = Produto.query.get(id_produto)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
        
        produto_loja = Produto_Loja.query.filter_by(id_produto = produto.id_produto, id_loja = loja.id_loja).first()
        if produto_loja:
            return redirect(url_for('produto.produtos',mensagem = "Esse produto Já foi vinculado à sua loja anteriormente"))

        novo_produto_loja = Produto_Loja(id_produto = id_produto, id_loja = loja.id_loja)
        db.session.add(novo_produto_loja)
        db.session.commit()
        
        return redirect(url_for('produto.produtos',mensagem = "Produto vinculado a sua Loja"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))

@loja_bp.route('/desvincular/<id_produto>',methods=['POST'])
def desvincular(id_produto):
    try:
        verificar = validacoes.verificarCadastroCompleto()
        if verificar:
            return verificar
        
        typeUser = session['typeUser']
        if typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        loja = Loja.query.filter_by(id_usuario=session['user_id']).first()
        if not loja:
            return redirect(url_for('produto.produtos',mensagem = "Loja não encontrada"))
        produto = Produto.query.get(id_produto)
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
        
        produto_loja = Produto_Loja.query.filter_by(id_produto = produto.id_produto, id_loja = loja.id_loja).first()
        if not produto_loja:
            return redirect(url_for('produto.produtos',mensagem = "Esse produto não foi vinculado à sua loja anteriormente"))
        db.session.delete(produto_loja)

        db.session.commit()
        
        return redirect(url_for('produto.produtos',mensagem = "Produto desvinculado a sua Loja"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
@loja_bp.route('/produto/<id_produto>')
def produto(id_produto):
        verificar = validacoes.verificarCadastroCompleto()
        if verificar:
            return verificar
        
        typeUser = session['typeUser']
    
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        produto_loja = Produto_Loja.query.get(id_produto)
        if not produto_loja:
            return redirect(url_for('menu.principal',mensagem = "Produto não encontrado"))
        loja = Loja.query.filter_by(id_loja=produto_loja.id_loja).first()
        if not loja:
            return redirect(url_for('produto.produtos',mensagem = "Loja não encontrada"))
        produto = Produto.query.filter_by(id_produto=produto_loja.id_produto).first()
        if not produto:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
        endereco_loja = Endereco.query.filter_by(id_usuario = loja.id_usuario).first()
        distancia = None
        if session['typeUser'] != 1:
            lat = session['lat']
            long = session['long']
            distancia = geodesic((float(endereco_loja.latitude), float(endereco_loja.longitude)),
                                    (float(lat), float(long))).km

        
        return render_template('menu/vizualizarProduto.html', mensagem=mensagem,produto = produto,loja = [loja,endereco_loja,distancia])