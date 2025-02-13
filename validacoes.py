import re
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import pytz

def validar_email(email):

    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if len(email) > 254:
        return False
    
    if re.match(regex, email) == False:
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

def validar_cadastro(email,user,password,password_confirm):

    if validar_email(email) == False:
        return False,"Email inválido"
    
    if validar_usuario(user) == False:
        return False,"Nome de usuário deve ter entre 3 e 20 caracteres; Conter apenas letras, números e/ou sublinhados (_); Não começar ou terminar com um sublinhado; Não conter espaços."
    
    senha, mensagem = validar_senha(password,password_confirm)
    if senha == False:
        return False,mensagem
    
    return True, "Cadastrado com sucesso!"


    
def enviar_email(email,token):
    
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


def enviar_convite(email,token):
    
    corpo_email = f"""
    Olá, {email}!
    <br></br>
    Entre na nossa equipe, adorariamos tê-lo em nosso time
    <br></br>
    http://127.0.0.1:5000/convite/{token}
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
