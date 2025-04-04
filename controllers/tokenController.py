import requests
from models.Token import Token
from flask import session
from models.Usuario import Usuario
from services.email_service import enviar_validacao,enviar_email_recuperacao


API_URL = "http://localhost:3001/tokens/"

def criarToken(metodo, id, email):
    dados_usuario = {
            "id_user": id,
        }
    response = requests.post(API_URL +"criar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(mensagem)
    print(response.status_code)
    if response.status_code != 201:
        return mensagem
    
    token_api = resposta_json.get('novo_token')
    usuario = Usuario(id_usuario=token_api["id_user"]["id_usuario"],
                      email_usuario=token_api["id_user"]["email_usuario"],
                      pass_usuario=token_api["id_user"]["pass_usuario"],
                      verificado=token_api["id_user"]["verificado"],
                      typeUser = token_api["id_user"]["typeUser"])

    novo_token = Token(id_token=token_api['id_token'],
                       dt_cr=token_api['dt_cr'],
                       usado=token_api["usado"],
                       usuario=usuario)
    if metodo == 1:
        if session.get('user_verificado') is not None:
            return "Email de validação não enviado, motivo: Esse usuário já está validado"
        email = enviar_validacao(email, novo_token.id_token)
        print(email)
    elif metodo == 2:
        email = enviar_email_recuperacao(email, novo_token.id_token)
        print(email)
    print(mensagem)
    return mensagem

def validarToken(id_token,id_usuario):
    response = requests.get(API_URL + f"validar/{id_token}/{id_usuario}")
    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code != 200:
        return False,mensagem

    verificado = resposta_json.get('verificado')
    return True,verificado