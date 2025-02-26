from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db,Endereco
import requests
import re

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
     
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroEnd.html',erro = erro)

@endereco_bp.route('/cadastrar',methods=['POST'])
def cadastrar():
    try:
        if(Endereco.query.filter_by(id_usuario = session['user_id']).first()):
            return redirect(url_for('endereco.cadastro',erro = "Já existe um endereço vinculado à esse usuário, se precisa atualizar esse endereço, atualize-o na página de perfil"))
        verificar = validacoes.verificarCadastro()
        if verificar:
            return verificar
        
        verificarLojaCliente = validacoes.verificarLojaCliente()
        if verificarLojaCliente:
            return verificarLojaCliente
        
        erro = request.args.get('erro')
        if erro == None:
            erro = ""
    except:
        return render_template('cadastroEnd.html',erro = "Algo deu errado, tente novamente")
    
def validarCadastroEndereco(cep,rua, numero, bairro, complemento, uf):
    print('/Tem que fazer')





def validar_formulario(cep, numero, complemento, rua, cidade, uf):
    MAX_RUA_LENGTH = 65
    MAX_CIDADE_LENGTH = 40
    MAX_CEP_LENGTH = 8
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
    
    return True, [re.sub(r"\D", "", cep),rua,numero,complemento,uf,cidade]
