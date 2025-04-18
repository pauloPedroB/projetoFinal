from flask import Blueprint, render_template, request, redirect, url_for, session
from models.Loja import Loja
import re
import services.validacoes as validacoes
from controllers import lojaController,produtoController,produto_lojaController
from models.Produto_Loja import Produto_Loja
from models.Usuario import Usuario



loja_bp = Blueprint('loja', __name__)

@loja_bp.route('/cadastro')
def cadastro():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        
        verificarUsuario = validacoes.verificarUsuario()
        if type(verificarUsuario) != Usuario:
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
        if type(verificarUsuario) != Usuario:
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
                      usuario = verificarUsuario,
                        )
        nova_loja,mensagem = lojaController.criar(loja)
        if(nova_loja == None):
            return redirect(url_for('loja.cadastro',mensagem = f"Não foi possível vincular seu usuário a uma loja, {mensagem}"))
        verificarUsuario.typeUser = 2        
        session['typeUser'] = verificarUsuario.typeUser

        return redirect(url_for('endereco.cadastro'))
        
    except:
        return redirect(url_for('loja.cadastro',mensagem = "Algo deu errado, tente novamente"))

@loja_bp.route('/vincular/<id_produto>',methods=['POST'])
def vincular(id_produto):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        
        typeUser = session['typeUser']
        if typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        loja, mensagem = lojaController.buscar({"id_usuario": session['user_id']})
        if loja == None:
            return redirect(url_for('produto.produtos',mensagem = "Loja não encontrada"))
        produto, mensagem = produtoController.buscar({'id_produto': id_produto})
        if produto == None:
            return redirect(url_for('produto.produtos',mensagem = "Produto não encontrado"))
        produto_loja = Produto_Loja(
            produto,
            loja,
            None,
            None,
            None
        )
        
        criado, mensagem = produto_lojaController.criar(produto_loja,session['user_id'])
        if(criado == False):
            return redirect(url_for('produto.produtos',mensagem = f"Produto Não vinculado a sua Loja: {mensagem}"))

        return redirect(url_for('produto.produtos',mensagem = "Produto vinculado a sua Loja"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))

@loja_bp.route('/desvincular/<id_produto>',methods=['POST'])
def desvincular(id_produto):
    try:
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
        
        typeUser = session['typeUser']
        if typeUser != 2:
            return redirect(url_for('menu.principal',mensagem = "Você não possuí acesso a essa página"))
        
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        
        produto_loja,endereco_user,mensagem = produto_lojaController.buscar({'id_produto_loja': id_produto, 'id_usuario': session['user_id']})
        
        if not produto_loja:
            return redirect(url_for('produto.produtos',mensagem = "Esse produto não foi vinculado à sua loja anteriormente"))
        excluir, mensagem = produto_lojaController.excluir(produto_loja,session['user_id'])
        if(excluir == False):
            return redirect(url_for('produto.produtos',mensagem = f"Produto Não desvinculado a sua Loja {mensagem}"))
        
        return redirect(url_for('produto.produtos',mensagem = "Produto desvinculado a sua Loja"))
    except:
        return redirect(url_for('produto.produtos',mensagem = "Algo deu errado, tente novamente"))
@loja_bp.route('/produto/<id_produto>')
def produto(id_produto):
        usuario,endereco = validacoes.verificarCadastroCompleto()
        if type(usuario) != Usuario:
            return usuario
                
        mensagem = request.args.get('mensagem')
        if mensagem == None:
            mensagem = ""
        typeUser = session['typeUser']

        produto_loja,endereco_user,mensagem = produto_lojaController.buscar({'id_produto_loja': id_produto, 'id_usuario': session['user_id']})
        distancia = "%.2f" % produto_loja.distancia
        loja = produto_loja.loja
        endereco_loja = produto_loja.endereco
        produto = produto_loja.produto
        return render_template('menu/vizualizarProduto.html', mensagem=mensagem,typeUser = typeUser,produto = produto,loja = [loja,endereco_loja,distancia,endereco_user])
