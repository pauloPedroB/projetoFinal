import requests
from models.Loja import Loja
from models.Usuario import Usuario


API_URL = "http://localhost:3001/lojas/"

def buscar(dados_usuario):
    response = requests.post(API_URL +"id_user/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 200:
        return None,mensagem
    loja_api = resposta_json.get('loja')

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
            "id_usuario": loja.usuario.id_usuario,

        }
    response = requests.post(API_URL +"criar/", json=dados_usuario)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return None,mensagem
    loja_api = resposta_json.get('nova_loja')

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
    
    return loja_api,mensagem