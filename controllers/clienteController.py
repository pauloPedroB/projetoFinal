import requests
from models.Cliente import Cliente
from models.Usuario import Usuario
from flask import session
import jwt
import time



API_URL = "http://localhost:3001/clientes/"

def buscar(dados_usuario):
    if 'token_dados' in session:
        dados = jwt.decode(session['token_dados'], options={"verify_signature": False})
        cliente_api = dados['cliente']
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
        cliente_api = dados['cliente']
        session['token_dados'] = token_dados

    usuario = Usuario(id_usuario=cliente_api["usuario"]["id_usuario"],
                        email_usuario=cliente_api["usuario"]["email_usuario"],
                        pass_usuario=cliente_api["usuario"]["pass_usuario"],
                        verificado=cliente_api["usuario"]["verificado"],
                        typeUser = cliente_api["usuario"]["typeUser"])
    
    cliente = Cliente(id_cliente=cliente_api["id_cliente"],
                      cpf=cliente_api["cpf"],
                      nome=cliente_api["nome"],
                      telefone = cliente_api["telefone"],
                      dtNascimento=cliente_api["dtNascimento"],
                      genero = cliente_api["genero"],
                      carro = cliente_api["genero"],
                      usuario = usuario,
                        )
    
    return cliente,mensagem

def criar(cliente:Cliente):
    dados_usuario = {
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "dtNascimento": cliente.dtNascimento,
            "telefone": cliente.telefone,
            "genero": cliente.genero,
            "carro": cliente.carro,

        }
    headers = {
        "Authorization": f"Bearer {session['token']}"
    }
    response = requests.post(API_URL +"criar/", json=dados_usuario,headers=headers)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(response.status_code)
    if response.status_code != 201:
        return None,mensagem
    token_dados = resposta_json.get('token_dados')
    dados = jwt.decode(token_dados, options={"verify_signature": False})
    cliente_api = dados['cliente']

    usuario = Usuario(id_usuario=cliente_api["usuario"]["id_usuario"],
                        email_usuario=cliente_api["usuario"]["email_usuario"],
                        pass_usuario=cliente_api["usuario"]["pass_usuario"],
                        verificado=cliente_api["usuario"]["verificado"],
                        typeUser = cliente_api["usuario"]["typeUser"])
    
    cliente = Cliente(id_cliente=cliente_api["id_cliente"],
                      cpf=cliente_api["cpf"],
                      nome=cliente_api["nome"],
                      telefone = cliente_api["telefone"],
                      dtNascimento=cliente_api["dtNascimento"],
                      genero = cliente_api["genero"],
                      carro = cliente_api["genero"],
                      usuario = usuario,
                        )
    
    session['token_dados'] = token_dados
    session.pop('token', None)
    
    return cliente,mensagem