import requests
from models.Produto import Produto
from models.Loja import Loja
from models.Usuario import Usuario
from models.Produto_Loja import Produto_Loja
from models.Endereco import Endereco

from typing import Optional


from flask import session



API_URL = "http://localhost:3001/produtos_loja/"

def buscar(dados_usuario)-> Optional[Produto_Loja]:
    if 'token' in session:
        headers = {
                    "Authorization": f"Bearer {session['token']}"
                }
        response = requests.post(API_URL +"buscar/", json=dados_usuario,headers=headers)
    else:
        response = requests.post(API_URL +"buscar/", json=dados_usuario)

    resposta_json = response.json()
    mensagem = resposta_json.get('message')
    print(mensagem)
    if response.status_code != 200:
        return None,None,mensagem
    produto_loja_api = resposta_json.get('produto_loja')
    distancia = resposta_json.get('distancia')
    endereco_user = resposta_json.get('endereco')

    produto = Produto(
                id_produto= produto_loja_api['produto']['id_produto'],
                nome_produto= produto_loja_api['produto']['nome_produto'],
                categoria=produto_loja_api['produto']['categoria'],
                img= produto_loja_api['produto']['img']
                )
    usuario = Usuario(id_usuario=produto_loja_api["loja"]["usuario"]["id_usuario"],
                        email_usuario=produto_loja_api["loja"]["usuario"]["email_usuario"],
                        pass_usuario=produto_loja_api["loja"]["usuario"]["pass_usuario"],
                        verificado=produto_loja_api["loja"]["usuario"]["verificado"],
                        typeUser = produto_loja_api["loja"]["usuario"]["typeUser"])
    
    loja = Loja(id_loja=produto_loja_api["loja"]["id_loja"],
                      cnpj=produto_loja_api["loja"]["cnpj"],
                      nomeFantasia=produto_loja_api["loja"]["nomeFantasia"],
                      razaoSocial = produto_loja_api["loja"]["razaoSocial"],
                      telefone=produto_loja_api["loja"]["telefone"],
                      celular = produto_loja_api["loja"]["celular"],
                      abertura = produto_loja_api["loja"]["abertura"],
                      usuario = usuario,
                        )
    endereco = Endereco(id = produto_loja_api['endereco']['id'],
                        rua = produto_loja_api['endereco']['rua'],
                        bairro = produto_loja_api['endereco']['bairro'],
                        cidade = produto_loja_api['endereco']['cidade'],
                        cep = produto_loja_api['endereco']['cep'],
                        complemento = produto_loja_api['endereco']['complemento'],
                        uf = produto_loja_api['endereco']['uf'],
                        nmr = produto_loja_api['endereco']['nmr'],
                        latitude = produto_loja_api['endereco']['latitude'],
                        longitude = produto_loja_api['endereco']['longitude'],
                        usuario = usuario
                        )
    if(distancia != None):
        produto_loja = Produto_Loja(
            produto,
            loja,
            endereco,
            distancia,
            produto_loja_api['id_produto_loja']
        )
    else:
        produto_loja = Produto_Loja(
                produto,
                loja,
                endereco,
                None,
                produto_loja_api['id_produto_loja']
            )
        
    return produto_loja,endereco_user, mensagem

def listarProdutoLoja():
    headers = {
                    "Authorization": f"Bearer {session['token']}",
                    "token_dados": f"{session['token_dados']}"

                }
  
    response = requests.post(API_URL +"listarProdutosLoja/",headers=headers)
    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    if response.status_code != 200:
        print(response.status_code)

        print(mensagem)
        return None,mensagem
    produtos_loja_api = resposta_json.get('produtos_loja')
    if(produtos_loja_api == None):
        produtos_loja_api = []
    loja = resposta_json.get('loja')
    usuario = Usuario(id_usuario=loja["usuario"]["id_usuario"],
                            email_usuario=loja["usuario"]["email_usuario"],
                            pass_usuario=loja["usuario"]["pass_usuario"],
                            verificado=loja["usuario"]["verificado"],
                            typeUser = loja["usuario"]["typeUser"])
        
    loja = Loja(
        id_loja=loja["id_loja"],
        cnpj=loja["cnpj"],
        nomeFantasia=loja["nomeFantasia"],
        razaoSocial = loja["razaoSocial"],
        telefone=loja["telefone"],
        celular = loja["celular"],
        abertura = loja["abertura"],
        usuario = usuario,
    )
    produtos_loja = []
    for produto_loja_api in produtos_loja_api:
        
        produto = Produto(
                    id_produto= produto_loja_api['produto']['id_produto'],
                    nome_produto= produto_loja_api['produto']['nome_produto'],
                    categoria=produto_loja_api['produto']['categoria'],
                    img= produto_loja_api['produto']['img']
                    )
       
        produto_loja = Produto_Loja(
            produto,
            loja,
            None,
            None,
            produto_loja_api['id_produto_loja']

        )
        produtos_loja.append(produto_loja)
       
    return produtos_loja, mensagem

def listar(nomes = [],categoria = None ):
    dados_usuario = {
            "nomes": nomes,
            "categoria": categoria,
        }
    if 'token' in session:
        headers = {
                    "Authorization": f"Bearer {session['token']}"
                }
        response = requests.post(API_URL +"listar/", json=dados_usuario,headers=headers)
    else:
        response = requests.post(API_URL +"listar/", json=dados_usuario)

    resposta_json = response.json()
    mensagem = resposta_json.get('message')

    print(mensagem)
    if response.status_code != 200:
        return None,mensagem
    produtos_loja_api = resposta_json.get('produtos_loja')
    if(produtos_loja_api == None):
        produtos_loja_api = []

    produtos_loja = []
    for produto_loja_api in produtos_loja_api:
        
        produto = Produto(
                    id_produto= produto_loja_api['produto']['id_produto'],
                    nome_produto= produto_loja_api['produto']['nome_produto'],
                    categoria=produto_loja_api['produto']['categoria'],
                    img= produto_loja_api['produto']['img']
                    )
        
        
        usuario = Usuario(id_usuario=produto_loja_api["loja"]["usuario"]["id_usuario"],
                        email_usuario=produto_loja_api["loja"]["usuario"]["email_usuario"],
                        pass_usuario=produto_loja_api["loja"]["usuario"]["pass_usuario"],
                        verificado=produto_loja_api["loja"]["usuario"]["verificado"],
                        typeUser = produto_loja_api["loja"]["usuario"]["typeUser"])
        
        endereco = Endereco(id = produto_loja_api['endereco']['id'],
                        rua = produto_loja_api['endereco']['rua'],
                        bairro = produto_loja_api['endereco']['bairro'],
                        cidade = produto_loja_api['endereco']['cidade'],
                        cep = produto_loja_api['endereco']['cep'],
                        complemento = produto_loja_api['endereco']['complemento'],
                        uf = produto_loja_api['endereco']['uf'],
                        nmr = produto_loja_api['endereco']['nmr'],
                        latitude = produto_loja_api['endereco']['latitude'],
                        longitude = produto_loja_api['endereco']['longitude'],
                        usuario = usuario
                        )
        loja = Loja(id_loja=produto_loja_api["loja"]["id_loja"],
                      cnpj=produto_loja_api["loja"]["cnpj"],
                      nomeFantasia=produto_loja_api["loja"]["nomeFantasia"],
                      razaoSocial = produto_loja_api["loja"]["razaoSocial"],
                      telefone=produto_loja_api["loja"]["telefone"],
                      celular = produto_loja_api["loja"]["celular"],
                      abertura = produto_loja_api["loja"]["abertura"],
                      usuario = usuario,
                        )
        distancia = produto_loja_api['distancia']
        produto_loja = Produto_Loja(
            produto,
            loja,
            endereco,
            distancia,
            produto_loja_api['id_produto_loja']
        )
        produtos_loja.append(produto_loja)
       
    return produtos_loja, mensagem

def criar(produto_loja:Produto_Loja):
    dados_usuario = {
        "id_produto": produto_loja.produto.id_produto,
        }
    headers = {
                    "Authorization": f"Bearer {session['token']}",
                    "token_dados": f"{session['token_dados']}"

                }
  
    response = requests.post(API_URL +"criar/", json=dados_usuario,headers=headers)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return False,mensagem

    return True,mensagem


def excluir(produto_loja:Produto_Loja):
    dados_usuario = {
        "id_produto_loja": produto_loja.id_produto_loja,
        }
    headers = {
                    "Authorization": f"Bearer {session['token']}",
                    "token_dados": f"{session['token_dados']}"

                }
    print(produto_loja.id_produto_loja)
    response = requests.delete(API_URL +"excluir/", json=dados_usuario,headers=headers)
    resposta_json = response.json()

    mensagem = resposta_json.get('message')

    if response.status_code != 201:
        return False,mensagem

    return True,mensagem

    