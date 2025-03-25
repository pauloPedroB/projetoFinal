import requests
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import mysql.connector



def extrair_nome_meio(url):
    padrao = r"https?://(?:www\.)?jocar\.com\.br/([^/]+)/"
    resultado = re.search(padrao, url)
    
    if resultado:
        return resultado.group(1)  # Retorna o nome do meio
    else:
        return None

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Victor@12",
    database="projetoAutomoveis"
)
cursor = db.cursor()


pasta_imagens = "static/uploads/"
os.makedirs(pasta_imagens, exist_ok=True)

url = "https://www.jocar.com.br/"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, "html.parser")

submenus = soup.find_all("ul", class_="submenu3")

links = []

for submenu in submenus:
    for a in submenu.find_all("a", href=True):
        links.append(a["href"])

for link in links:

    response_link = requests.get(link)
    html_link = response_link.text
    soup_link = BeautifulSoup(html_link, "html.parser")

    produtos = soup_link.find_all("div", class_="productDiv")

    for produto in produtos:
        img_tag = produto.find("img", class_="link3")
        nome_tag = produto.find("a", class_="link4")

        # Pegando a URL correta da imagem
        img_src = img_tag.get("data-src") or img_tag.get("src") or img_tag.get("data-original")

        # Verifica se o link da imagem é relativo e converte para absoluto
        img_src = urljoin(url, img_src) if img_src else None

        # Pegando o nome do produto
        nome = nome_tag.text.strip() if nome_tag else "Nome não encontrado"

        # Normalizando o nome do arquivo
        nome_arquivo = re.sub(r'[^a-zA-Z0-9 _-]','',nome)[:150]  
        caminho_imagem = os.path.join(pasta_imagens, f"{nome_arquivo}.jpg")

        if os.path.exists(caminho_imagem):
            print(f"Imagem já existe: {caminho_imagem}")
            continue  # Pula o download e não insere no banco
        
        # Baixar e salvar a imagem
        if img_src:
            try:
                response_img = requests.get(img_src, stream=True)
                if response_img.status_code == 200:
                    with open(caminho_imagem, "wb") as file:
                        for chunk in response_img.iter_content(1024):
                            file.write(chunk)
                    cursor.execute("INSERT INTO produtos (nome_produto, img,categoria) VALUES (%s, %s,%s)", 
                    (nome_arquivo, nome_arquivo+".jpg",extrair_nome_meio(link)))
                    db.commit()

                    print(f"Produto Salvo: {caminho_imagem}")

                else:
                    print(f"Erro ao baixar imagem: {img_src}")
            except Exception as e:
                print(f"Erro ao salvar imagem {img_src}: {e}")




