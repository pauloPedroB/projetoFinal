import re
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz
import requests
from geopy.geocoders import Nominatim, OpenCage
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic

from classes import db, Usuarios, Endereco, Tokens
from flask import session


def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if len(email) > 254:
        return False
    
    if not re.match(regex, email):  # Corrigido aqui
        return False
   
    return True


def validar_senha(senha,confirmacao_senha):
    if (len(senha) >= 8 and
        re.search(r'[A-Z]', senha) and
        re.search(r'[a-z]', senha) and
        re.search(r'[0-9]', senha) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', senha)):
        if(senha != confirmacao_senha):
            return False, "Senha e Confirmação de Senha devem ser iguais"
        else:
            return True,"Senha alterada com Sucesso"

    return False, "Senha deve ter pelo menos oito caracteres, uma letra maiúscula, uma letra minuscula, um número e um caracter"
  


def validar_usuario(nome_usuario):
    if (3 <= len(nome_usuario) <= 20 and
        re.match(r'^[a-zA-Z0-9_]+$', nome_usuario) and
        not nome_usuario.startswith('_') and
        not nome_usuario.endswith('_')):
        return True
    return False

def validar_cadastro(email,password,password_confirm):

    if validar_email(email) == False:
        return False,"Email inválido"
    
    senha, mensagem = validar_senha(password,password_confirm)
    if senha == False:
        return False,mensagem
    
    return True, "Cadastrado com sucesso!"

def enviarEmail(metodo,id,email):

    id_token = gerar_token()
    horario = horario_br()
    novo_token = Tokens(id_token=id_token, id_user=id, dt_cr=horario,usado = False)
    if metodo == 1:
        if 'user_verificado' in session:
            return None
        enviar_validacao(email,novo_token.id_token)
    elif metodo == 2:
        enviar_email_recuperacao(email,novo_token.id_token)
    db.session.add(novo_token)
    db.session.commit()

def enviar_validacao(email,token):
    
    corpo_email = f"""
    Olá, {email}!
    <br></br>
    Recebemos uma solicitação de cadastro em nosso site usando este email
    <br></br>
    Se você está tentando se cadastrar, clique nest link:
    <br></br>
    http://127.0.0.1:5000/validar/{token}
    <br></br>
    Este link é válido por 2 horas.
    """

    msg = MIMEMultipart()
    msg['Subject'] = "Assunto"
    msg['From'] = 'siqueirapedropaulo93@gmail.com'
    msg['To'] = email
    senha = 'gelmtdnmupufjiqd'  # Senha de app gerada

    msg.attach(MIMEText(corpo_email, 'html', 'utf-8'))
    try:
       
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], senha)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

        return True
    except Exception as e:

        return False
    
def enviar_email_recuperacao(email,token):
    
    corpo_email = f"""
    Olá, {email}!
    <br></br>
    Recebemos uma solicitação para redefinir sua senha. Se você não solicitou a redefinição, ignore este email.
    <br></br>
    Para redefinir sua senha, clique no link abaixo:
    <br></br>
    http://127.0.0.1:5000/recuperar/{token}
    <br></br>
    Este link é válido por 2 horas.
    """

    msg = MIMEMultipart()
    msg['Subject'] = "Assunto"
    msg['From'] = 'siqueirapedropaulo93@gmail.com'
    msg['To'] = email
    senha = 'gelmtdnmupufjiqd'  # Senha de app gerada

    msg.attach(MIMEText(corpo_email, 'html', 'utf-8'))


    try:
       
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(msg['From'], senha)
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()

        return True
    except Exception as e:

        return False

def gerar_token(comprimento=32):
    return secrets.token_hex(comprimento)

def horario_br():
    fuso_horario_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_horario_brasilia)

def verificar_expiracao_token(token):
    agora = datetime.now()
    
    tempo_criacao = token.dt_cr
    
    limite = tempo_criacao + timedelta(hours=2)
    
    if agora > limite:
        return True 
    else:
        return False
    

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if "erro" not in dados:
            return True, dados
        else:
            return False, "Cep Não encontrado"
    else:
        return False,"Erro na requisição."




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

# ------------------------------- VALIDAR CADASTRO LOJA --------------------------------------------
def validar_cadastroLoja(cnpj,nome,razao,tell,cell,data):
    if validar_cnpj(cnpj) == False:
        return False, "CNPJ INVÁLIDO"
    if validar_nome(nome)  == False:
        return False,"Nome Fantásia Inválido"
    if validar_nome(razao)  == False:
        return False,"Razão Social Inválida"
    if validar_telefone(tell)  == False:
        return False,"Telefone Inválido"
    if validar_data_abertura(data)  == False:
        return False,"Data inválida"
    if(cell != None):
        if validar_telefone(cell)  == False:
            return False,"Número de Telefone Inválido"
 
    return True,"Sucesso"



def validar_cnpj(cnpj):
    """Valida um CNPJ verificando o formato e os dígitos verificadores."""
    cnpj = re.sub(r'\D', '', cnpj)

    if len(cnpj) != 14:
        return False 

    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6] + pesos_1

    def calcular_digito(cnpj_parcial, pesos):
        soma = sum(int(a) * b for a, b in zip(cnpj_parcial, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    digito1 = calcular_digito(cnpj[:12], pesos_1)
    digito2 = calcular_digito(cnpj[:12] + digito1, pesos_2)

    return cnpj.endswith(digito1 + digito2)



def validar_data_abertura(data_str):
    try:
        # Converte a string da data para um objeto datetime
        data_abertura = datetime.strptime(data_str, "%Y-%m-%d")
        
        # Obtém a data atual (sem horas, minutos e segundos)
        data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Verifica se a data de abertura é no futuro
        if data_abertura > data_atual:
            return False  # Se for no futuro, retorna False (inválido)
        
        # Se passar, a data é válida (ou no passado ou no presente)
        return True 
    
    except ValueError:
        return False  # Se a data não for válida no formato "%Y-%m-%d", retorna False
    


# ---------------------------------------------------------------------------------------------------


# ------------------------------- VALIDAR CADASTRO CLIENTE --------------------------------------------

def validar_cadastroCliente(cpf,nome,tell,data,genero, carro):
    if validar_cpf(cpf) == False:
        return False, "CPF INVÁLIDO"
    if validar_nome(nome)  == False:
        return False,"Nome Inválido"
    if validar_telefone(tell)  == False:
        return False,"Telefone Inválido"
    if validar_data_nascimento(data)  == False:
        return False,"Data inválida"
    if validar_genero(genero) == False:
        return False, "opção de Gênero não disponível"
    if validar_carro(carro) == False:
        return False, "opção de Carro não disponível"

    return True,"Sucesso"

def validar_genero(genero):
    """Valida a escolha do gênero (valores entre 1 e 4)."""
    return genero in {"1", "2", "3", "4"}

def validar_carro(carro):
    """Valida a escolha sobre possuir carro (valores entre 1 e 3)."""
    return carro in {"1", "2", "3"}

def validar_cpf(cpf):
    """Valida um CPF verificando o formato e os dígitos verificadores."""
    cpf = re.sub(r'\D', '', cpf)  # Remove caracteres não numéricos

    if len(cpf) != 11 or cpf in (str(i) * 11 for i in range(10)):
        return False

    def calcular_digito(cpf_parcial, pesos):
        soma = sum(int(d) * p for d, p in zip(cpf_parcial, pesos))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos_1 = list(range(10, 1, -1))
    pesos_2 = list(range(11, 1, -1))

    digito1 = calcular_digito(cpf[:9], pesos_1)
    digito2 = calcular_digito(cpf[:9] + digito1, pesos_2)

    return cpf.endswith(digito1 + digito2)


def validar_data_nascimento(data_str):
    """Verifica se a data de nascimento está no passado e se a idade é válida."""
    try:
        data_nascimento = datetime.strptime(data_str, "%Y-%m-%d")
        data_atual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if data_nascimento >= data_atual:
            return False  

        idade = (data_atual - data_nascimento).days // 365
        return idade >= 18

    except ValueError:
        return False  
    
#-----------------------------------------------------------
def validar_telefone(telefone):
    """Valida telefone e celular: apenas números e tamanho entre 10 e 11 dígitos"""
    telefone_limpo = re.sub(r'\D', '', telefone)  # Remove caracteres não numéricos
    return bool(re.fullmatch(r'\d{10,11}', telefone_limpo))


def validar_nome(nome):
    # Verifica se o nome tem entre 3 e 65 caracteres
    if len(nome) < 3 or len(nome) > 65:
        return False
    
    # Verifica se o nome contém apenas letras e espaços
    if not re.match(r'^[a-zA-Záéíóúãõâêîôûàèìòùãẽĩõũ ]+$', nome):
        return False
    
    # Verifica se o nome não começa nem termina com espaços
    if nome.startswith(' ') or nome.endswith(' '):
        return False
    
    return True