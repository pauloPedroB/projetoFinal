from flask import Blueprint, redirect, url_for, session, request, render_template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import secrets
import smtplib
from datetime import datetime, timedelta
import validacoes
from classes import db,Tokens,Usuarios



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


@email_service.route('/validar/<token>')
def validar(token):
    try:
        token = Tokens.query.filter(Tokens.id_token == token, Tokens.usado == False).first()

        if not token or verificar_expiracao_token(token):
            return redirect(url_for('email.verificarEmail', mensagem="Token inválido ou já utilizado."))

        usuario = Usuarios.query.filter(Usuarios.id_usuario == token.id_user).first()

        if not usuario:
            return redirect(url_for('email.verificarEmail', mensagem="Usuário não encontrado"))
        
        if usuario.id_usuario != session.get('user_id'):
            return redirect(url_for('email.verificarEmail', mensagem="Usuário vinculado ao token não é o mesmo usuário que está acessando o sistema"))

        usuario.verificado = validacoes.horario_br()
        token.usado = True
        db.session.commit()

        session['user_verificado'] = usuario.verificado

        return redirect(url_for('menu.escolha'))
    except:
        return redirect(url_for('auth.inicio', erro="Algo deu errado ao procurar o seu token, repita o processo de recuperação"))


def enviarEmail(metodo, id, email):
    id_token = gerar_token()
    horario = validacoes.horario_br()
    novo_token = Tokens(id_token=id_token, id_user=id, dt_cr=horario, usado=False)
    if metodo == 1:
        # Verifica se o usuário já foi verificado; somente retorna se o valor for diferente de None
        if session.get('user_verificado') is not None:
            return None
        enviar_validacao(email, novo_token.id_token)
    elif metodo == 2:
        enviar_email_recuperacao(email, novo_token.id_token)
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
    
def gerar_token(comprimento=32):
    return secrets.token_hex(comprimento)


def verificar_expiracao_token(token):
    agora = datetime.now()
    
    tempo_criacao = token.dt_cr
    
    limite = tempo_criacao + timedelta(hours=2)
    
    if agora > limite:
        return True 
    else:
        return False
    