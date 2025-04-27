import requests
from models.Usuario import Usuario
from flask import session
import time


API_URL = "http://localhost:3001/usuarios/"
import jwt


def buscar(dados_usuario):
    if 'token' in session:
        dados = jwt.decode(session['token'], options={"verify_signature": False})
        usuario_api = dados['usuario']
        exp = dados['exp']
        if not exp:
            return None,"Token não tem campo 'exp'"

        agora = int(time.time())
        if agora >= exp:
            return None,"Token expirado"
    else:
        response = requests.post(API_URL +"buscarPorEmail/", json=dados_usuario)
        resposta_json = response.json()
        mensagem = resposta_json.get('message')

        if response.status_code !=200:
            return None,mensagem
        
        token = resposta_json.get('token')
        dados = jwt.decode(token, options={"verify_signature": False})
        usuario_api = dados['usuario']
        session['token'] = token
        
    
    usuario = Usuario(id_usuario=usuario_api["id_usuario"],
                      email_usuario=usuario_api["email_usuario"],
                      pass_usuario=usuario_api["pass_usuario"],
                      verificado=usuario_api["verificado"],
                      typeUser = usuario_api["typeUser"])
    
    return usuario,'Usuário encontrado'

def criarUsuario(email,senha,confirmacao_senha):
    dados_usuario = {
            "email_usuario": email,
            "pass_usuario": senha,
            "confirm_pass": confirmacao_senha,
        }
    
    response = requests.post(API_URL  + "criar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 201:
        return None,mensagem
    
    token = resposta_json.get('token')
    dados = jwt.decode(token, options={"verify_signature": False})
    usuario_api = dados['usuario']

    novo_usuario = Usuario(id_usuario=usuario_api["id_usuario"],
                      email_usuario=usuario_api["email_usuario"],
                      pass_usuario=usuario_api["pass_usuario"],
                      verificado=usuario_api["verificado"],
                      typeUser = usuario_api["typeUser"])
    
    session['token'] = token
    session['user_id'] = novo_usuario.id_usuario
    session['user_email'] = novo_usuario.email_usuario
    
    return novo_usuario, mensagem
    
def login(email,senha):
    
    dados_usuario = {
        "email_usuario": email,
        "pass_usuario": senha
    }
    response = requests.post(API_URL + "login/", json=dados_usuario)
    resposta_json = response.json()
    print(response.status_code)

    mensagem = resposta_json.get('message')
    if response.status_code != 200:
        return None,mensagem
    token = resposta_json.get('token')
    dados = jwt.decode(token, options={"verify_signature": False})
    usuario_api = dados['usuario']
    
    usuario = Usuario(id_usuario=usuario_api["id_usuario"],
                      email_usuario=usuario_api["email_usuario"],
                      pass_usuario=usuario_api["pass_usuario"],
                      verificado=usuario_api["verificado"],
                      typeUser = usuario_api["typeUser"])
    
    session['token'] = token
    session['user_id'] = usuario.id_usuario
    session['user_email'] = usuario.email_usuario
    session['user_verificado'] = usuario.verificado
    session['typeUser'] = usuario.typeUser
    
    return usuario, mensagem
    
def resetarSenha(senha, confirmacao_senha, id_token):

    dados_usuario = {
            "pass_usuario": senha,
            "confirm_pass": confirmacao_senha,
            "id_token": id_token
        }
    response = requests.post(API_URL  + "resetPass/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 201:
        return False, mensagem
    return True, mensagem

def alterarTipo(usuario):

    dados_usuario = {
            "typeUser": usuario.typeUser,
            "id_user": usuario.id_usuario,
        }
    response = requests.post(API_URL  + "Atualizar/Tipo/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 201:
        return False, mensagem
    return True, mensagem