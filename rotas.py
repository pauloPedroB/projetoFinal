from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from geopy.distance import geodesic
import validacoes
from classes import db, Usuarios, Endereco, Tokens
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Victor%4012@localhost:3306/projetoAutomoveis'
app.config['SECRET_KEY'] = 'Chave()1243123'

db.init_app(app)



def logout():
    session.clear()

def verificarCadastro():
    if 'user_id' not in session:
        return redirect('/inicio')
    if not 'user_verificado' in session or session['user_verificado'] is None:
        return redirect('/VerifiqueseuEmail')

    return None

def verificarLog():
    if 'user_id' in session:
        return redirect('/menu')
    return None
    
@app.route('/')
def index():
    return redirect('/inicio')


@app.route('/inicio')
def inicio():
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""

    verificar = verificarLog()
    if verificar:
        return verificar

    
    return render_template('index.html',erro=erro)
    

@app.route('/cadastro')
def cadastro():
    
    verificar = verificarLog()
    if verificar:
        return verificar
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""

    return render_template('cadastro.html',erro = erro)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        
        verificar = verificarLog()
        if verificar:
            return verificar
        email = request.form['email']
        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']

        validacao,mensagem = validacoes.validar_cadastro(email,senha,confirmacao_senha)
        

        if(validacao == False):
            return redirect(url_for('cadastro',erro = mensagem))
        elif(Usuarios.query.filter_by(email_usuario=email).first()):
            return redirect(url_for('cadastro',erro = "Email já cadastrado!"))
        
        hashed_password = generate_password_hash(senha)
        
        novo_usuario = Usuarios(email_usuario=email, pass_usuario=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        session['user_id'] = novo_usuario.id_usuario
        session['user_email'] = novo_usuario.email_usuario

        validacoes.enviarEmail(1,session['user_id'],session['user_email'])
        
        return redirect(url_for('menu'))

    except:
        return redirect(url_for('cadastro',erro = "Erro ao tentar se cadastrar"))

    

@app.route('/enviar')
def enviar():
    try:
        validacoes.enviarEmail(1,session['user_id'],session['user_email'])
        return redirect(url_for('menu'))
    
    except:
        return redirect(url_for('inicio'))



    
@app.route('/validar/<token>')
def validar(token):
    try:
      
        token = Tokens.query.filter(Tokens.id_token == token, Tokens.usado == False).first()

        if not token or validacoes.verificar_expiracao_token(token)==True:
            return redirect(url_for('VerificarEmail', mensagem="Token inválido ou já utilizado."))
        usuario = Usuarios.query.filter(Usuarios.id_usuario == token.id_user).first()

        if not usuario:
            return redirect(url_for('VerificarEmail', mensagem="Usuário não encontrado"))
        
        if usuario.id_usuario != session.get('user_id'):
            return redirect(url_for('VerificarEmail', mensagem="Usuario vinculado ao token não é o mesmo usuário que está acessando o Sistema"))


        
        usuario.verificado = validacoes.horario_br()
        token.usado = True
        db.session.commit()

        session['user_verificado'] = usuario.verificado

        return redirect(url_for('menu'))
    except:
        return redirect(url_for('inicio', erro='Algo deu errado ao procurar o seu token, repita o processo de recuperação'))

@app.route('/entrar', methods=['POST'])
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

                return redirect(url_for('menu'))

            return redirect(url_for('inicio', erro='Senha incorreta'))
        return redirect(url_for('inicio', erro='Usuário não encontrado'))
        
   except:
        return redirect(url_for('inicio', erro='Erro ao tentar acessar o sistema'))
   
@app.route('/recuperar')
def recuperar():
    verificar = verificarLog()
    if verificar:
        return verificar
    return render_template('recuperar.html')


@app.route('/recuperarsenha', methods=['POST'])
def recuperarsenha():
        verificar = verificarLog()
        if verificar:
            return verificar
        email = request.form['email']
        usuario = Usuarios.query.filter((Usuarios.email_usuario == email)).first()
        if(usuario):
            validacoes.enviarEmail(2, usuario.id_usuario, usuario.email_usuario)
            return redirect(url_for('inicio', erro='Email de recuperação enviada para sua caixa de mensagens'))
        else:
            return redirect(url_for('inicio', erro='Usuário não encontado'))
        
@app.route('/recuperar/<token>')
def senhas(token):
    try:
        logout()

        return render_template('senhas.html',token = token)
    except:
        return redirect(url_for('inicio', erro='Algo deu errado ao procurar o seu token, repita o processo de recuperação'))
    

@app.route('/alterarsenha', methods=['POST'])
def alterarsenha():
    try:
        logout()

        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']
        id_token = request.form['token']

        verificar_senha, mensagem = validacoes.validar_senha(senha, confirmacao_senha)

        if not verificar_senha:
            return render_template('senhas.html', mensagem=mensagem,token = id_token)

        token = Tokens.query.filter(Tokens.id_token == id_token, Tokens.usado == False).first()

        if not token or validacoes.verificar_expiracao_token(token)==True:
            return render_template('senhas.html', mensagem="Token inválido ou já utilizado.",token = id_token)

        usuario = Usuarios.query.filter(Usuarios.id_usuario == token.id_user).first()

        if not usuario:
            return render_template('senhas.html', mensagem="Usuário não encontrado.",token = id_token)

        hashed_password = generate_password_hash(senha)
        usuario.pass_usuario = hashed_password

        token.usado = True
        db.session.commit()
        
        return redirect(url_for('inicio', erro="Senha alterada com sucesso."))
    except:
        return render_template('senhas.html', mensagem="Erro ao tentar alterar senha",token = id_token)

@app.route('/menu')
def menu():
    verificar = verificarCadastro()
    if verificar:  
        return verificar
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""
 
    return render_template('menu.html', mensagem = "Validado")

@app.route('/cadastroLoja')
def cadastroLoja():
    
    verificar = verificarCadastro()
    if verificar:
        return verificar
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""
    return render_template('cadastroLoja.html',erro = erro)




@app.route('/consultar_cnpj', methods=['GET'])
def consultar_cnpj():
    cnpj = request.args.get('cnpj')
    if cnpj:
        url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'CNPJ não encontrado'}), 404
    return jsonify({'error': 'CNPJ inválido'}), 400

@app.route('/cadastrarLoja',methods=['POST'])
def cadastrarLoja():
    cnpj = request.form['CNPJ']
    nomeFantasia = request.form['nomeFantasia']
    razaoSocial = request.form['razaoSocial']
    telefone = request.form['telefone']
    celular = request.form['celular']
    abertura = request.form['abertura']

    cadastro,mensagem = validacoes.validar_cadastroLoja(cnpj,nomeFantasia,razaoSocial,telefone,celular,abertura)
    if cadastro:
        return redirect(url_for('menu'))
    return redirect(url_for('cadastroLoja',erro = mensagem))

@app.route('/buscar_cep', methods=['GET'])
def buscar_cep():
    cep = request.args.get('cep')

    if not cep or len(cep) != 8 or not cep.isdigit():
        return render_template('index.html', erro="Cep Inválido", dados=None)
    
    sucesso, endereco = validacoes.consultar_cep(cep)
    endereco_completo = endereco
    if sucesso:
        endereco_formatado = f'{endereco["logradouro"]}, {endereco["bairro"]}, {endereco["localidade"]}, {endereco["uf"]}, Brasil'
        
        latLong = validacoes.obter_lat_long(endereco_formatado)
        
        if latLong:
            novo_endereco = Endereco(rua = endereco["logradouro"],nmr = 2, latitude = latLong["latitude"], longitude = latLong["longitude"])
            db.session.add(novo_endereco)
            db.session.commit()

            enderecos = Endereco.query.all()
            enderecos_ordenados = []
            for endereco in enderecos:
                distancia = geodesic((float(novo_endereco.latitude), float(novo_endereco.longitude)),
                                    (float(endereco.latitude), float(endereco.longitude))).km
                enderecos_ordenados.append({
                    "rua": endereco.rua,
                    "distancia": round(distancia, 2)
                })

            enderecos_ordenados.sort(key=lambda x: x["distancia"])


            return render_template('index.html', erro="", dados=endereco_completo, latLong=latLong,enderecos_ordenados = enderecos_ordenados)
        else:
            return render_template('index.html', erro="Coordenadas não encontradas.", dados=endereco)
    else:
        return render_template('index.html', erro="Cep não encontrado", dados=None)
    
@app.route('/VerifiqueseuEmail')
def VerificarEmail():
    
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""
    return render_template('email.html',mensagem = mensagem)

@app.route('/sair')
def sair():
    logout()
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
