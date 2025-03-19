import requests
from flask import session,redirect,url_for
from services.email_service import enviarEmail

API_URL = "http://localhost:3001/"
ROTA_USUARIOS = 'usuarios/'


def buscarPorId(id):
    dados_usuario = {
            "id_user": id,
        }
    
    response = requests.post(API_URL + ROTA_USUARIOS +"id/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 200:
        return None,mensagem
    usuario = resposta_json.get('usuario')
    return usuario,mensagem

def buscarPorEmail(email):
    
    dados_usuario = {
            "email_usuario": email,
        }
    response = requests.post(API_URL + "buscar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code ==200:
        usuario = resposta_json.get('usuario')
        return usuario,mensagem
    else:
        return None,mensagem

def criarUsuario(email,senha,confirmacao_senha):
    dados_usuario = {
            "email_usuario": email,
            "pass_usuario": senha,
            "confirm_pass": confirmacao_senha,
        }
    
    response = requests.post(API_URL + ROTA_USUARIOS + "criar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code == 201:
            novo_usuario = resposta_json.get('novo_usuario')
            return novo_usuario, mensagem
    else:
        return None,mensagem
    

def login(email,senha):
    
    dados_usuario = {
        "email_usuario": email,
        "pass_usuario": senha
    }
    response = requests.post(API_URL+ ROTA_USUARIOS + "login/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code == 200:
        usuario = resposta_json.get('usuario')
        
        return usuario,mensagem
    
    else:

        return None,mensagem
    
def resetarSenha(senha, confirmacao_senha, id_token):

    dados_usuario = {
            "pass_usuario": senha,
            "confirm_pass": confirmacao_senha,
            "id_token": id_token
        }
    response = requests.post(API_URL + ROTA_USUARIOS + "resetPass/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 201:
        return False, mensagem
    return True, mensagem

