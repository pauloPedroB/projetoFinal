from flask import Blueprint, redirect, url_for, session, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from classes import db

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
        from controllers.tokenController import criarToken
        
        criarToken(1,session['user_id'],session['user_email'])
        return redirect(url_for('menu.principal'))
    
    except:
        return redirect(url_for('auth.inicio'))

def enviar_validacao(email,token):
    
    corpo_email = f"""
    Olá, {email}!
    <br></br>
    Recebemos uma solicitação de cadastro em nosso site usando este email
    <br></br>
    Se você está tentando se cadastrar, clique nest link:
    <br></br>
    http://127.0.0.1:5000/auth/validar/{token}
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
    




    