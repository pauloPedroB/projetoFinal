import requests
from models.Endereco import Endereco
from models.Usuario import Usuario
from typing import Optional

API_URL = "http://localhost:3001/enderecos/"

def buscar(dados_usuario)-> Optional[Endereco]:
    response = requests.post(API_URL +"id_user/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(f'resposta {mensagem}')
    if response.status_code != 200:
        return None,mensagem
    endereco_api = resposta_json.get('endereco')
    usuario = Usuario(id_usuario=endereco_api["usuario"]["id_usuario"],
                        email_usuario=endereco_api["usuario"]["email_usuario"],
                        pass_usuario=endereco_api["usuario"]["pass_usuario"],
                        verificado=endereco_api["usuario"]["verificado"],
                        typeUser = endereco_api["usuario"]["typeUser"])
    
    endereco = Endereco(id = endereco_api['id'],
                        rua = endereco_api['rua'],
                        bairro = endereco_api['bairro'],
                        cidade = endereco_api['cidade'],
                        cep = endereco_api['cep'],
                        complemento = endereco_api['complemento'],
                        uf = endereco_api['uf'],
                        nmr = endereco_api['nmr'],
                        latitude = endereco_api['latitude'],
                        longitude = endereco_api['longitude'],
                        usuario = usuario
                        )
    return endereco,mensagem

def criar(endereco:Endereco):
    dados_usuario = {
  
            "rua": endereco.rua,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade,
            "cep": endereco.cep,
            "complemento": endereco.complemento,
            "uf": endereco.uf,
            "nmr": endereco.nmr,
            "id_usuario": endereco.usuario.id_usuario,
        }
    response = requests.post(API_URL +"criar/", json=dados_usuario)
    print(response.status_code)

    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return None,mensagem
    endereco_api = resposta_json.get('novo_endereco')

    usuario = Usuario(id_usuario=endereco_api["usuario"]["id_usuario"],
                        email_usuario=endereco_api["usuario"]["email_usuario"],
                        pass_usuario=endereco_api["usuario"]["pass_usuario"],
                        verificado=endereco_api["usuario"]["verificado"],
                        typeUser = endereco_api["usuario"]["typeUser"])
    
    endereco = Endereco(id = endereco_api['id'],
                        rua = endereco_api['rua'],
                        bairro = endereco_api['bairro'],
                        cidade = endereco_api['cidade'],
                        cep = endereco_api['cep'],
                        complemento = endereco_api['complemento'],
                        uf = endereco_api['uf'],
                        nmr = endereco_api['nmr'],
                        latitude = endereco_api['latitude'],
                        longitude = endereco_api['longitude'],
                        usuario = usuario
                        )
    
    return endereco,mensagem

def editar(endereco:Endereco):
    dados_usuario = {
        "rua": endereco.rua,
        "bairro": endereco.bairro,
        "cidade": endereco.cidade,
        "cep": endereco.cep,
        "complemento": endereco.complemento,
        "uf": endereco.uf,
        "nmr": endereco.nmr,
        "id_usuario": endereco.usuario.id_usuario,
        "id_endereco": endereco.id,
    }
    response = requests.post(API_URL +"editar/", json=dados_usuario)
    print(response.status_code)

    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return None,mensagem
    endereco_api = resposta_json.get('novo_endereco')

    usuario = Usuario(id_usuario=endereco_api["usuario"]["id_usuario"],
                        email_usuario=endereco_api["usuario"]["email_usuario"],
                        pass_usuario=endereco_api["usuario"]["pass_usuario"],
                        verificado=endereco_api["usuario"]["verificado"],
                        typeUser = endereco_api["usuario"]["typeUser"])
    
    endereco = Endereco(id = endereco_api['id'],
                        rua = endereco_api['rua'],
                        bairro = endereco_api['bairro'],
                        cidade = endereco_api['cidade'],
                        cep = endereco_api['cep'],
                        complemento = endereco_api['complemento'],
                        uf = endereco_api['uf'],
                        nmr = endereco_api['nmr'],
                        latitude = endereco_api['latitude'],
                        longitude = endereco_api['longitude'],
                        usuario = usuario
                        )
    
    return endereco,mensagem