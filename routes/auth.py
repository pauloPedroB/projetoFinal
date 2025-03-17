# /routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from classes import db, Usuarios, Tokens
import services.validacoes as validacoes
from services.email_service import enviarEmail
from werkzeug.security import generate_password_hash, check_password_hash
import requests



# Criando o Blueprint de autenticação
auth_bp = Blueprint('auth', __name__)


API_URL = "http://localhost:3001/usuarios/"

# Função auxiliar para verificar login
def verificarLog(mensagem=None):
    if mensagem == None:
        mensagem = ""
    if 'user_id' in session:
        return redirect(url_for('menu.principal',mensagem = mensagem))
    return None


def logout():
    session.clear()

@auth_bp.route('/inicio')
def inicio():
    
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""

    verificar = verificarLog(mensagem)
    if verificar:
        return verificar

    
    return render_template('index.html',mensagem=mensagem)

@auth_bp.route('/cadastro')
def cadastro():
    verificar = verificarLog()
    if verificar:
        return verificar
    
    mensagem = request.args.get('mensagem', '')  # Se erro for None, retorna ""
    return render_template('cadastro.html', mensagem=mensagem)

@auth_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        
        email = request.form['email']
        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']

        validacao, mensagem = validacoes.validar_cadastro(email, senha, confirmacao_senha)

        if not validacao:
            return redirect(url_for('auth.cadastro', mensagem=mensagem))
        
        dados_usuario = {
            "email_usuario": email,
            "pass_usuario": senha,
        }
        
        response = requests.post(API_URL + "criar/", json=dados_usuario)
        resposta_json = response.json()
        print(resposta_json)

        if response.status_code == 201:
            novo_usuario = resposta_json.get('novo_usuario')
            session['user_id'] = novo_usuario['id_usuario']
            session['user_email'] = novo_usuario['email_usuario']

            enviarEmail(1, session['user_id'], session['user_email'])
            return redirect(url_for('menu.escolha'))
        
        else:
            mensagem = resposta_json.get('message')
            return redirect(url_for('auth.cadastro', mensagem=mensagem))
        
    except Exception as e:
        return redirect(url_for('auth.cadastro', mensagem=f"Erro ao tentar se cadastrar {e}"))
    

@auth_bp.route('/entrar', methods=['POST'])
def entrar():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        nome = request.form['email']
        senha = request.form['password']

        dados_usuario = {
            "email_usuario": nome,
            "pass_usuario": senha
        }
        response = requests.post(API_URL + "login/", json=dados_usuario)
        resposta_json = response.json()
        print(resposta_json)

        if response.status_code == 200:
            usuario = resposta_json.get('usuario')
            session['user_id'] = usuario['id_usuario']
            session['user_email'] = usuario['email_usuario']
            session['user_verificado'] = usuario['verificado']
            session['typeUser'] = usuario['typeUser']
            return redirect(url_for('menu.principal'))
        
        else:
            mensagem = resposta_json.get('message')
            return redirect(url_for('auth.inicio', mensagem=mensagem))
    
    except Exception as e:
        return redirect(url_for('auth.inicio', mensagem=f'Erro ao tentar acessar o sistema{e}'))

    
@auth_bp.route('/recuperar')
def recuperar():
    verificar = verificarLog()
    if verificar:
        return verificar
    return render_template('recuperar.html')


@auth_bp.route('/recuperarsenha', methods=['POST'])
def recuperarsenha():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        email = request.form['email']
        
        dados_usuario = {
            "email_usuario": email,
        }
        response = requests.post(API_URL + "buscar/", json=dados_usuario)
        resposta_json = response.json()
        print(resposta_json)
        if response.status_code ==200:
            usuario = resposta_json.get('usuario')
            enviarEmail(2, usuario['id_usuario'], usuario['email_usuario'])
            return redirect(url_for('auth.inicio', mensagem='Email de recuperação enviada para sua caixa de mensagens'))
        else:
            mensagem = resposta_json.get('message')
            return redirect(url_for('auth.inicio', mensagem=mensagem))
    except Exception as e:
            return redirect(url_for('auth.inicio', mensagem=f'Algo deu errado, tente novamente: {e}'))

        


@auth_bp.route('/recuperar/<token>')
def senhas(token):
    try:
        logout()
        mensagem = request.args.get('mensagem', '')

        return render_template('senhas.html',token = token,mensagem = mensagem)
    except Exception as e:
        return redirect(url_for('auth.inicio', mensagem= f'Algo deu errado ao procurar o seu token, repita o processo de recuperação: {e}'))
    
@auth_bp.route('/alterarsenha', methods=['POST'])
def alterarsenha():
    try:
        logout()

        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']
        id_token = request.form['token']

        verificar_senha, mensagem = validacoes.validar_senha(senha, confirmacao_senha)

        if not verificar_senha:
            return redirect(url_for('auth.senhas',mensagem=mensagem,token = id_token))

        buscandoToken = requests.get(f"http://localhost:3001/tokens/buscar/{id_token}")
        resposta_json = buscandoToken.json()
        if buscandoToken.status_code ==200:
            token = resposta_json.get('token')
            response = requests.get(f"http://localhost:3001/tokens/validar/{token['id_token']}/{token['id_user']['id_usuario']}")
            if(response.status_code == 200):
                
            else:
                resposta_json = response.json()
                mensagem = resposta_json.get('message')
                return redirect(url_for('auth.inicio', mensagem=mensagem))
        else:
            mensagem = resposta_json.get('message')
            return redirect(url_for('auth.inicio', mensagem=mensagem))

        return redirect(url_for('auth.inicio', mensagem="Senha alterada com sucesso."))
    except Exception as e:
        return redirect(url_for('auth.senhas',mensagem=f"Erro ao tentar alterar senha: {e}",token = id_token))

    


@auth_bp.route('/sair')
def sair():
    logout()
    return redirect(url_for('auth.inicio'))
