import requests
from models.Produto import Produto

API_URL = "http://localhost:3001/produtos/"

def buscar(dados_usuario):
    response = requests.post(API_URL +"buscar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    if response.status_code != 200:
        return None,mensagem
    produto_api = resposta_json.get('produto')
    
    produto = Produto(
                id_produto= produto_api['id_produto'],
                nome_produto= produto_api['nome_produto'],
                categoria=produto_api['categoria'],
                img= produto_api['img']
                )
    
    return produto,mensagem

def listar(nomes = [],categoria = None):
    dados_usuario = {
        "nomes": nomes,
        "categoria": categoria
        }
    response = requests.post(API_URL +"listar/", json=dados_usuario)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(response.status_code)
    if response.status_code != 200:
        return None,mensagem
    produtos = resposta_json.get('produtos')
    return produtos,mensagem

def criar(produto:Produto):
    dados_usuario = {
        "nome_produto": produto.nome_produto,
        "img": produto.img,
        "categoria": produto.categoria
        }
    response = requests.post(API_URL +"criar/", json=dados_usuario)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return False,mensagem

    return True,mensagem

def editar(produto:Produto):
    dados_usuario = {
        "id_produto": produto.id_produto,
        "nome_produto": produto.nome_produto,
        "img": produto.img,
        "categoria": produto.categoria
        }
    response = requests.post(API_URL +"editar/", json=dados_usuario)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return False,mensagem

    return True,mensagem

def excluir(produto:Produto):
    dados_usuario = {
        "id_produto": produto.id_produto,
        }
    response = requests.delete(API_URL +"excluir/", json=dados_usuario)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return False,mensagem

    return True,mensagem

    