# /routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
import services.validacoes as validacoes
from controllers.userController import criarUsuario,login,buscar,resetarSenha
from controllers.tokenController import criarToken,validarToken

# Criando o Blueprint de autenticação
auth_bp = Blueprint('auth', __name__)

# Função auxiliar para verificar login
def verificarLog(mensagem=None):
    if mensagem == None:
        mensagem = ""
    if 'user_id' in session:
        return redirect(url_for('menu.principal',mensagem = mensagem))
    return None


def logout():
    session.clear()

@auth_bp.route('/inicio')
def inicio():
    
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""

    verificar = verificarLog(mensagem)
    if verificar:
        return verificar

    
    return render_template('index.html',mensagem=mensagem)

@auth_bp.route('/cadastro')
def cadastro():
    verificar = verificarLog()
    if verificar:
        return verificar
    
    mensagem = request.args.get('mensagem', '')  # Se erro for None, retorna ""
    return render_template('cadastro.html', mensagem=mensagem)

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
            return redirect(url_for('auth.cadastro', mensagem=mensagem))
        
        novo_usuario,mensagem = criarUsuario(email,senha,confirmacao_senha)
        
        if novo_usuario == None:
            return redirect(url_for('auth.cadastro', mensagem=mensagem))
        session['user_id'] = novo_usuario.id_usuario
        session['user_email'] = novo_usuario.email_usuario
        mensagem = criarToken(1, session['user_id'], session['user_email'])

        return redirect(url_for('menu.escolha',mensagem))
            
    except Exception as e:
        return redirect(url_for('auth.cadastro', mensagem=f"Erro ao tentar se cadastrar {e}"))
    

@auth_bp.route('/entrar', methods=['POST'])
def entrar():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        nome = request.form['email']
        senha = request.form['password']

        usuario, token ,mensagem = login(nome,senha)
        
        if usuario == None:
            return redirect(url_for('auth.inicio', mensagem=mensagem))
        
        session['token'] = token
        session['user_id'] = usuario.id_usuario
        session['user_email'] = usuario.email_usuario
        session['user_verificado'] = usuario.verificado
        session['typeUser'] = usuario.typeUser
        return redirect(url_for('menu.principal',mensagem = mensagem))
        
    
    except Exception as e:
        return redirect(url_for('auth.inicio', mensagem=f'Erro ao tentar acessar o sistema{e}'))

@auth_bp.route('/verificarEmail')
def verificarEmail():
    if 'user_verificado' in session and session['user_verificado'] is not None:
        return redirect(url_for('menu.principal'))
    mensagem = request.args.get('mensagem', "")
    return render_template('email.html', mensagem=mensagem)

    
@auth_bp.route('/enviar')
def enviar():
    try:
        if 'user_verificado' in session and session['user_verificado'] is not None:
            return redirect(url_for('menu.principal'))
        from controllers.tokenController import criarToken
        
        criarToken(1,session['user_id'],session['user_email'])
        return redirect(url_for('menu.principal'))
    
    except:
        return redirect(url_for('auth.inicio'))
    
@auth_bp.route('/validar/<id_token>')
def validar(id_token):
    try:
        retorno, mensagem = validarToken(id_token,session['user_id'])
        if retorno == False:
            return redirect(url_for('auth.inicio', mensagem=f"Erro ao processar o token: {mensagem}"))

        session['user_verificado'] = mensagem
        return redirect(url_for('menu.escolha'))

    except Exception as e:
        print(e)
        return redirect(url_for('auth.inicio', mensagem=f"Algo deu errado ao procurar o seu token, repita o processo de recuperação: {e}"))

    
@auth_bp.route('/recuperar')
def recuperar():
    verificar = verificarLog()
    if verificar:
        return verificar
    return render_template('recuperar.html')


@auth_bp.route('/recuperarsenha', methods=['POST'])
def recuperarsenha():
    try:
        verificar = verificarLog()
        if verificar:
            return verificar
        email = request.form['email']

        usuario,mensagem = buscar({'email_usuario': email})
        if usuario == None:
            return redirect(url_for('auth.inicio', mensagem=mensagem))
        mensagem = criarToken(2, usuario.id_usuario, usuario.email_usuario)
        return redirect(url_for('auth.inicio', mensagem='Email de recuperação enviada para sua caixa de mensagens'))
    
    except Exception as e:
            return redirect(url_for('auth.inicio', mensagem=f'Algo deu errado, tente novamente: {e}'))

    


@auth_bp.route('/recuperar/<token>')
def senhas(token):
    try:
        logout()
        mensagem = request.args.get('mensagem', '')

        return render_template('senhas.html',token = token,mensagem = mensagem)
    except Exception as e:
        return redirect(url_for('auth.inicio', mensagem= f'Algo deu errado ao procurar o seu token, repita o processo de recuperação: {e}'))
    
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
        
        alteracao, mensagem = resetarSenha(senha,confirmacao_senha,id_token)
        if(alteracao == False):
            return redirect(url_for('auth.senhas', mensagem=mensagem,token = id_token))

        return redirect(url_for('auth.inicio', mensagem=mensagem))

    except Exception as e:
        return redirect(url_for('auth.senhas',mensagem=f"Erro ao tentar alterar senha: {e}",token = id_token))

    


@auth_bp.route('/sair')
def sair():
    logout()
    return redirect(url_for('auth.inicio'))
