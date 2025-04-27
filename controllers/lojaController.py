import requests
from models.Loja import Loja
from models.Usuario import Usuario
from flask import session
import jwt
import time


API_URL = "http://localhost:3001/lojas/"

def buscar(dados_usuario):
    if 'token_dados' in session:
        dados = jwt.decode(session['token_dados'], options={"verify_signature": False})
        loja_api = dados['loja']
        exp = dados['exp']
        if not exp:
            return None,"Token não tem campo 'exp'"

        agora = int(time.time())
        if agora >= exp:
            return None,"Token expirado"
        mensagem = 'Cliente encontrado'
    else:
        headers = {
                "Authorization": f"Bearer {session['token']}"
            }
        response = requests.post(API_URL +"id_user/", json=dados_usuario,headers=headers)
        resposta_json = response.json()
        mensagem = resposta_json.get('message')

        if response.status_code != 200:
            return None,mensagem
        token_dados = resposta_json.get('token_dados')
        dados = jwt.decode(token_dados, options={"verify_signature": False})
        loja_api = dados['loja']
        session['token_dados'] = token_dados
        

    usuario = Usuario(id_usuario=loja_api["usuario"]["id_usuario"],
                        email_usuario=loja_api["usuario"]["email_usuario"],
                        pass_usuario=loja_api["usuario"]["pass_usuario"],
                        verificado=loja_api["usuario"]["verificado"],
                        typeUser = loja_api["usuario"]["typeUser"])
    
    loja = Loja(id_loja=loja_api["id_loja"],
                    cnpj=loja_api["cnpj"],
                    nomeFantasia=loja_api["nomeFantasia"],
                    razaoSocial = loja_api["razaoSocial"],
                    telefone=loja_api["telefone"],
                    celular = loja_api["celular"],
                    abertura = loja_api["abertura"],
                    usuario = usuario,
                        )
    
    return loja,mensagem

def criar(loja:Loja):
    dados_usuario = {
  
            "cnpj": loja.cnpj,
            "nomeFantasia": loja.nomeFantasia,
            "razaoSocial": loja.razaoSocial,
            "telefone": loja.telefone,
            "celular": loja.celular,
            "abertura": loja.abertura,

        }
    headers = {
                "Authorization": f"Bearer {session['token']}"
            }
    response = requests.post(API_URL +"criar/", json=dados_usuario,headers=headers)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return None,mensagem
    token_dados = resposta_json.get('token_dados')
    dados = jwt.decode(token_dados, options={"verify_signature": False})
    loja_api = dados['loja']

    usuario = Usuario(id_usuario=loja_api["usuario"]["id_usuario"],
                        email_usuario=loja_api["usuario"]["email_usuario"],
                        pass_usuario=loja_api["usuario"]["pass_usuario"],
                        verificado=loja_api["usuario"]["verificado"],
                        typeUser = loja_api["usuario"]["typeUser"])
    
    loja = Loja(id_loja=loja_api["id_loja"],
                      cnpj=loja_api["cnpj"],
                      nomeFantasia=loja_api["nomeFantasia"],
                      razaoSocial = loja_api["razaoSocial"],
                      telefone=loja_api["telefone"],
                      celular = loja_api["celular"],
                      abertura = loja_api["abertura"],
                      usuario = usuario,
                        )
    session['token_dados'] = token_dados
    
    session.pop('token', None)
    
    
    return loja,mensagem

    