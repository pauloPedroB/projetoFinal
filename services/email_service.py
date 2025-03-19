from flask import Blueprint, redirect, url_for, session, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from classes import db
import requests

API_URL = "http://localhost:3001/tokens/"



email_service = Blueprint('email', __name__)

@email_service.route('/verificarEmail')
def verificarEmail():
    if 'user_verificado' in session and session['user_verificado'] is not None:
        return redirect(url_for('menu.principal'))
    mensagem = request.args.get('mensagem', "")
    return render_template('email.html', mensagem=mensagem)


@email_service.route('/enviar')
def enviar():
    try:
        if 'user_verificado' in session and session['user_verificado'] is not None:
            return redirect(url_for('menu.principal'))
        enviarEmail(1,session['user_id'],session['user_email'])
        return redirect(url_for('menu.principal'))
    
    except:
        return redirect(url_for('auth.inicio'))


@email_service.route('/validar/<id_token>')
def validar(id_token):
    try:
    
        response = requests.get(API_URL + f"validar/{id_token}/{session.get('user_id')}")
        if response.status_code == 200:
            try:
                resposta_json = response.json()
                print(resposta_json)


                verificado = resposta_json.get('verificado')

                session['user_verificado'] = verificado
                return redirect(url_for('menu.escolha'))
            
            except ValueError as e:
                # Caso a resposta não seja um JSON válido
                print(f"Resposta não é JSON válido{e}")
                return redirect(url_for('auth.inicio', mensagem= f"Resposta do servidor não é válida: {e}"))
        else:
            resposta_json = response.json()
            mensagem = resposta_json.get('message')

            print(f"Erro no servidor: {mensagem}")
            return redirect(url_for('auth.inicio', mensagem=f"Erro ao processar o token: {mensagem}"))

    except Exception as e:
        print(e)
        return redirect(url_for('auth.inicio', mensagem=f"Algo deu errado ao procurar o seu token, repita o processo de recuperação: {e}"))




def enviarEmail(metodo, id, email):
    dados_usuario = {
            "id_user": id,
        }
    response = requests.post(API_URL + "criar/", json=dados_usuario)
    resposta_json = response.json()

    if response.status_code == 201:
        novo_token = resposta_json.get('novo_token')
        print(novo_token['id_token'],"\n",email,"\n",metodo)

        if metodo == 1:
            if session.get('user_verificado') is not None:
                return None
            email = enviar_validacao(email, novo_token['id_token'])
            print(email)
        elif metodo == 2:
            email = enviar_email_recuperacao(email, novo_token['id_token'])
            print(email)

    else:
        print(response.status_code)





def enviar_validacao(email,token):
    
    corpo_email = f"""
    Olá, {email}!
    <br></br>
    Recebemos uma solicitação de cadastro em nosso site usando este email
    <br></br>
    Se você está tentando se cadastrar, clique nest link:
    <br></br>
    http://127.0.0.1:5000/email/validar/{token}
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
    http://127.0.0.1:5000/auth/recuperar/{token}
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
    




    