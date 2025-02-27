# /routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from classes import db, Usuarios, Tokens
import services.validacoes as validacoes
from services.email_service import enviarEmail,verificar_expiracao_token
from werkzeug.security import generate_password_hash, check_password_hash


# Criando o Blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Função auxiliar para verificar login
def verificarLog():
    if 'user_id' in session:
        return redirect(url_for('menu.principal'))
    return None


def logout():
    session.clear()

@auth_bp.route('/inicio')
def inicio():
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""

    verificar = verificarLog()
    if verificar:
        return verificar

    
    return render_template('index.html',erro=erro)

@auth_bp.route('/cadastro')
def cadastro():
    verificar = verificarLog()
    if verificar:
        return verificar
    
    erro = request.args.get('erro', '')  # Se erro for None, retorna ""
    return render_template('cadastro.html', erro=erro)

@auth_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        
        email = request.form['email']
        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']

        validacao, mensagem = validacoes.validar_cadastro(email, senha, confirmacao_senha)

        if not validacao:
            return redirect(url_for('auth.cadastro', erro=mensagem))
        elif Usuarios.query.filter_by(email_usuario=email).first():
            return redirect(url_for('auth.cadastro', erro="Email já cadastrado!"))
        
        hashed_password = generate_password_hash(senha)
        
        novo_usuario = Usuarios(email_usuario=email, pass_usuario=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        session['user_id'] = novo_usuario.id_usuario
        session['user_email'] = novo_usuario.email_usuario

        enviarEmail(1, session['user_id'], session['user_email'])
        
        return redirect(url_for('menu.escolha'))

    except:
        return redirect(url_for('auth.cadastro', erro="Erro ao tentar se cadastrar"))
    
@auth_bp.route('/entrar', methods=['POST'])
def entrar():
   try:
        verificar = verificarLog()
        if verificar:
            return verificar
        nome = request.form['email']
        senha = request.form['password']

        usuario = Usuarios.query.filter(Usuarios.email_usuario == nome).first()
        if(usuario):
            if(check_password_hash(usuario.pass_usuario,senha)):
                session['user_id'] = usuario.id_usuario
                session['user_email'] = usuario.email_usuario
                session['user_verificado'] = usuario.verificado
                session['typeUser'] = usuario.typeUser


                return redirect(url_for('menu.principal'))

            return redirect(url_for('auth.inicio', erro='Senha incorreta'))
        return redirect(url_for('auth.inicio', erro='Usuário não encontrado'))
        
   except:
        return redirect(url_for('auth.inicio', erro='Erro ao tentar acessar o sistema'))
    
@auth_bp.route('/recuperar')
def recuperar():
    verificar = verificarLog()
    if verificar:
        return verificar
    return render_template('recuperar.html')


@auth_bp.route('/recuperarsenha', methods=['POST'])
def recuperarsenha():
        verificar = verificarLog()
        if verificar:
            return verificar
        email = request.form['email']
        usuario = Usuarios.query.filter((Usuarios.email_usuario == email)).first()
        if(usuario):
            enviarEmail(2, usuario.id_usuario, usuario.email_usuario)
            return redirect(url_for('auth.inicio', erro='Email de recuperação enviada para sua caixa de mensagens'))
        else:
            return redirect(url_for('auth.inicio', erro='Usuário não encontado'))


@auth_bp.route('/recuperar/<token>')
def senhas(token):
    try:
        logout()
        mensagem = request.args.get('mensagem', '')

        return render_template('senhas.html',token = token,mensagem = mensagem)
    except:
        return redirect(url_for('auth.inicio', erro='Algo deu errado ao procurar o seu token, repita o processo de recuperação'))
    
@auth_bp.route('/alterarsenha', methods=['POST'])
def alterarsenha():
    try:
        logout()

        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']
        id_token = request.form['token']

        verificar_senha, mensagem = validacoes.validar_senha(senha, confirmacao_senha)

        if not verificar_senha:
            return redirect(url_for('auth.senhas',mensagem=mensagem,token = id_token))


        token = Tokens.query.filter(Tokens.id_token == id_token, Tokens.usado == False).first()

        if not token or verificar_expiracao_token(token)==True:
            return redirect(url_for('auth.senhas',mensagem="Token inválido ou já utilizado.",token = id_token))

        usuario = Usuarios.query.filter(Usuarios.id_usuario == token.id_user).first()

        if not usuario:
            return redirect(url_for('auth.senhas',mensagem="Usuário não encontrado",token = id_token))


        hashed_password = generate_password_hash(senha)
        usuario.pass_usuario = hashed_password

        token.usado = True
        db.session.commit()
        
        return redirect(url_for('auth.inicio', erro="Senha alterada com sucesso."))
    except:
        return redirect(url_for('auth.senhas',mensagem="Erro ao tentar alterar senha",token = id_token))

    


@auth_bp.route('/sair')
def sair():
    logout()
    return redirect(url_for('auth.inicio'))
