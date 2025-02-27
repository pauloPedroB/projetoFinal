from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Endereco
import requests
import re
from geopy.geocoders import Nominatim, OpenCage
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic


endereco_bp = Blueprint('endereco', __name__)

import validacoes

@endereco_bp.route('/cadastro')
def cadastro():
    verificar = validacoes.verificarCadastro()
    if verificar:
        return verificar
    verificarLojaCliente = validacoes.verificarLojaCliente()
    if verificarLojaCliente:
        return verificarLojaCliente
    if Endereco.query.filter_by(id_usuario=session['user_id']).first():
        return redirect(url_for('menu.principal'))
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroEnd.html',erro = erro)


@endereco_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        
        verificarLojaCliente = validacoes.verificarLojaCliente()
        if verificarLojaCliente:
            return verificarLojaCliente
        
        if Endereco.query.filter_by(id_usuario=session['user_id']).first():
            return redirect(url_for('menu.principal'))
        
        cep = request.form['CEP']
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        uf = request.form['uf']
        cidade = request.form['cidade']
        complemento = request.form['complemento']
        
        
        if(Endereco.query.filter_by(id_usuario = session['user_id']).first()):
            return redirect(url_for('endereco.cadastro',erro = "Já existe um endereço vinculado à esse usuário, se precisa atualizar esse endereço, atualize-o na página de perfil"))
        
        validacao,mensagem = validar_endereco(cep, numero, complemento, rua, cidade, uf,bairro)
        if validacao == False:
            return redirect(url_for('endereco.cadastro', erro = mensagem))
        novo_Endereco = Endereco(cep=mensagem[0], nmr = mensagem[1], complemento = mensagem[2], rua = mensagem[3], cidade = mensagem[4], uf = mensagem[5],bairro = mensagem[6],latitude = mensagem[7],longitude = mensagem[8], id_usuario = session['user_id'])
        db.session.add(novo_Endereco)
        db.session.commit()
        return redirect(url_for('menu.principal'))
    except:
        return redirect(url_for('endereco.cadastro', erro = "Algo deu errado, tente novamente"))


       

    



def validar_endereco(cep, numero, complemento, rua, cidade, uf,bairro):
    MAX_RUA_LENGTH = 65
    MAX_CIDADE_LENGTH = 40
    MAX_COMPLEMENTO_LENGTH = 200
    MAX_UF_LENGTH = 2
    
    # Validação do CEP
    if not re.fullmatch(r"\d{8}", cep):
        return False,"CEP inválido. Deve conter exatamente 8 dígitos numéricos."
    else:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
        if response.status_code == 200:
            cep_data = response.json()
            if "erro" in cep_data:
                return False,"CEP NÃO ENCONTRADO"
            else:
                rua = cep_data.get("logradouro", "")[:MAX_RUA_LENGTH]
                cidade = cep_data.get("localidade", "")[:MAX_CIDADE_LENGTH]
                uf = cep_data.get("uf", "")[:MAX_UF_LENGTH]
                bairro = cep_data.get("bairro", "")
        else:
            return False, "Erro ao consultar o CEP."
    
    # Validação do número
    if not numero:
        return False, "Número é obrigatório."
    
    # Validação da rua
    if not rua:
        return False, "Rua é obrigatória."
    elif len(rua) > MAX_RUA_LENGTH:
        return False, f"Rua não pode ter mais que {MAX_RUA_LENGTH} caracteres."
    
    # Validação da cidade
    if not cidade:
        return False, "Cidade é obrigatória."
    elif len(cidade) > MAX_CIDADE_LENGTH:
        return False, f"Cidade não pode ter mais que {MAX_CIDADE_LENGTH} caracteres."
    
    # Validação da UF
    if not uf:
        return False, "UF é obrigatória."
    elif len(uf) != MAX_UF_LENGTH:
        return False, f"UF deve ter exatamente {MAX_UF_LENGTH} caracteres."
    
    # Validação do complemento
    if len(complemento) > MAX_COMPLEMENTO_LENGTH:
        return False,f"Complemento não pode ter mais que {MAX_COMPLEMENTO_LENGTH} caracteres."
    
    endereco_formatado = f'{rua}, {numero}, {bairro}, {bairro}, {uf}, Brasil'
    latLong = obter_lat_long(endereco_formatado)
    
    return True, [re.sub(r"\D", "", cep),numero, complemento, rua, cidade, uf,bairro, latLong["latitude"], latLong["longitude"]]


def obter_lat_long(endereco):
    # Primeiro, tente usar o Nominatim
    geolocator_nominatim = Nominatim(user_agent="myGeocoder")
    
    try:
        localizacao = geolocator_nominatim.geocode(endereco, timeout=10)
        if localizacao:
            return {"latitude": localizacao.latitude, "longitude": localizacao.longitude}
    except GeocoderTimedOut:
        print("Erro de timeout com Nominatim.")
    
    # Se o Nominatim não funcionar, tente o OpenCage
    chave_api_opencage = '25fc62d0f13d40448e3f206d06bc89bd'
    geolocator_opencage = OpenCage(api_key=chave_api_opencage)
    
    try:
        localizacao = geolocator_opencage.geocode(endereco)
        if localizacao:
            return {"latitude": localizacao.latitude, "longitude": localizacao.longitude}
    except Exception as e:
        print(f"Erro ao tentar o OpenCage: {e}")
    
    partes_endereco = endereco.split(',')
    
    bairro = partes_endereco[1] if len(partes_endereco) > 1 else None
    cidade = partes_endereco[2] if len(partes_endereco) > 2 else partes_endereco[1]

    if bairro and cidade:
        endereco_bairro_cidade = f"{bairro.strip()}, {cidade.strip()}"
        try:
            localizacao_bairro_cidade = geolocator_opencage.geocode(endereco_bairro_cidade)
            if localizacao_bairro_cidade:
                return {"latitude": localizacao_bairro_cidade.latitude, "longitude": localizacao_bairro_cidade.longitude}
        except Exception as e:
            print(f"Erro ao tentar buscar o bairro e cidade com OpenCage: {e}")
    
    return None