from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from geopy.distance import geodesic
import validacoes

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Victor%4012@localhost:3306/projetoAutomoveis'
app.config['SECRET_KEY'] = 'Chave()1243123'

db = SQLAlchemy(app)

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_usuario = db.Column(db.String(120), unique=True, nullable=False)
    pass_usuario = db.Column(db.String(300), nullable=False)
    verificado = db.Column(db.DateTime, nullable=False)
    tokens = db.relationship('Tokens', backref='usuario', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'

class Endereco(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(50), nullable=False)
    nmr = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Endereco {self.rua}>'
    
class Tokens(db.Model):
    __tablename__ = 'tokens'

    id_token = db.Column(db.String(300), primary_key=True, nullable=False) 
    dt_cr = db.Column(db.DateTime, nullable=False) 
    usado = db.Column(db.Boolean, default=False, nullable=False)

    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f'<Token {self.id_token}>'

def logout():
    session.clear()


def enviarEmail():
    id_token = validacoes.gerar_token()
    horario = validacoes.horario_br()
    novo_token = Tokens(id_token=id_token, id_user=session['user_id'], dt_cr=horario,usado = False)
    db.session.add(novo_token)
    db.session.commit()
    enviar = validacoes.enviar_email(session['user_email'],novo_token.id_token)


def verificarCadastro():
    if 'user_id' not in session:
        return redirect('/inicio')
    if not 'user_verificado' in session or session['user_verificado'] is None:
        return redirect('/VerifiqueseuEmail')

    return None
    
@app.route('/')
def index():
    return redirect('/inicio')


@app.route('/inicio')
def inicio():
    
    erro = request.args.get('erro')
    if erro == None:
        erro = ""

    if 'user_id' in session:
        return redirect('/menu')
    
    return render_template('index.html',erro=erro)
    

@app.route('/cadastro')
def cadastro():
    logout()

    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        logout()
        email = request.form['email']
        senha = request.form['password']
        confirmacao_senha = request.form['confirm_password']

        validacao,mensagem = validacoes.validar_cadastro(email,senha,confirmacao_senha)
        

        if(validacao == False):
            return render_template("cadastro.html", erro=mensagem)
        elif(Usuarios.query.filter_by(email_usuario=email).first()):
            return render_template("cadastro.html", erro="Email já cadastrado!")
        
        hashed_password = generate_password_hash(senha)
        
        novo_usuario = Usuarios(email_usuario=email, pass_usuario=hashed_password)
        db.session.add(novo_usuario)
        db.session.commit()

        session['user_id'] = novo_usuario.id_usuario
        session['user_email'] = novo_usuario.email_usuario

        enviarEmail()
        
        return redirect(url_for('menu'))

    except:
        return render_template("cadastro.html", erro="Erro ao tentar se cadastrar")
    

@app.route('/enviar')
def enviar():
    try:
        verificar = verificarCadastro()
        enviarEmail()
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
        logout()
        nome = request.form['login']
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
   

@app.route('/menu')
def menu():
    verificar = verificarCadastro()
    if verificar:  
        return verificar
    mensagem = request.args.get('mensagem')
    if mensagem == None:
        mensagem = ""
 
    return render_template('menu.html', mensagem = "Validado")


  
    
    
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
