import requests
from models.Cliente import Cliente
from models.Usuario import Usuario


API_URL = "http://localhost:3001/clientes/"

def buscar(dados_usuario):
    response = requests.post(API_URL +"id_user/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 200:
        return None,mensagem
    cliente_api = resposta_json.get('cliente')

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

def criar(cliente):
    dados_usuario = {
            "cpf": cliente.cpf,
            "nome": cliente.nome,
            "dtNascimento": cliente.dtNascimento,
            "telefone": cliente.telefone,
            "genero": cliente.genero,
            "carro": cliente.carro,
            "id_usuario": cliente.usuario.id_usuario,

        }
    response = requests.post(API_URL +"criar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(response.status_code)
    if response.status_code != 201:
        return None,mensagem
    cliente_api = resposta_json.get('novo_cliente')

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