from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Produto,Produto_Loja,Endereco
from models.Loja import Loja
import re
import services.validacoes as validacoes
from geopy.distance import geodesic
from controllers import lojaController
loja_bp = Blueprint('loja', __name__)

@loja_bp.route('/cadastro')
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
        return render_template('cadastroLoja.html',mensagem = mensagem)
    except:
        return redirect(url_for('menu.escolha',mensagem = "Algo deu errado, tente novamente"))


@loja_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        verificarUsuario,usuario = validacoes.verificarUsuario()
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
        
        loja = Loja(id_loja=None,
                      cnpj=cnpj_user,
                      nomeFantasia=nomeFantasia,
                      razaoSocial = razaoSocial,
                      telefone=telefone,
                      celular = celular,
                      abertura = abertura,
                      usuario = usuario,
                        )
        nova_loja,mensagem = lojaController.criar(loja)
        if(nova_loja == None):
            return redirect(url_for('loja.cadastro',mensagem = f"Não foi possível vincular seu usuário a uma loja, {mensagem}"))
        usuario.typeUser = 2        
        session['typeUser'] = usuario.typeUser

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
        loja, mensagem = lojaController.buscar({"id_usuario": session['user_id']})
        if loja == None:
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
        loja, mensagem = lojaController.buscar({"id_usuario": session['user_id']})

        if loja == None:
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
    try:
        verificar = validacoes.verificarCadastroCompleto()
        if verificar:
            return verificar
                
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        produto_loja = Produto_Loja.query.get(id_produto)
        if not produto_loja:
            return redirect(url_for('menu.principal',mensagem = "Produto não encontrado"))
        loja, mensagem = lojaController.buscar({"id_usuario": session['user_id']})
        
        if loja == None:
            return redirect(url_for('menu.principals',mensagem = "Loja não encontrada"))
        produto = Produto.query.filter_by(id_produto=produto_loja.id_produto).first()
        if not produto:
            return redirect(url_for('menu.principal',mensagem = "Produto não encontrado"))
        endereco_loja = Endereco.query.filter_by(id_usuario = loja.id_usuario).first()
        endereco_user = Endereco.query.filter_by(id_usuario = session['user_id']).first()
        distancia = None
        typeUser = session['typeUser']

        if typeUser != 1:
            lat = session['lat']
            long = session['long']
            distancia = geodesic((float(endereco_loja.latitude), float(endereco_loja.longitude)),
                                    (float(lat), float(long))).km
            distancia = round(distancia, 2)
        return render_template('menu/vizualizarProduto.html', mensagem=mensagem,typeUser = typeUser,produto = produto,loja = [loja,endereco_loja,distancia,endereco_user])
    except Exception as e:
        return redirect(url_for('menu.principal',mensagem = f"Algo deu errado, tente novamente: {e}"))
