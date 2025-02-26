from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_usuario = db.Column(db.String(120), unique=True, nullable=False)
    pass_usuario = db.Column(db.String(300), nullable=False)
    verificado = db.Column(db.DateTime, nullable=False)
    tokens = db.relationship('Tokens', backref='usuario', cascade="all, delete-orphan")
    Loja = db.relationship('Loja', backref='usuario', cascade="all, delete-orphan")
    Cliente = db.relationship('Cliente', backref='usuario', cascade="all, delete-orphan")


    def __repr__(self):
        return f'<Usuario {self.email_usuario}>'

class Endereco(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(65), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(8),unique = True, nullable=False)
    complemento = db.Column(db.String(200), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    nmr = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

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
    

class Loja(db.Model):
    __tablename__ = 'lojas'

    id_loja = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nomeFantasia = db.Column(db.String(65), nullable=False)
    razaoSocial = db.Column(db.String(65), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    celular = db.Column(db.String(20), nullable=True)
    abertura = db.Column(db.Date, nullable=False)

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f'<Loja {self.cnpj}>'
    
class Cliente(db.Model):
    __tablename__ = 'clientes'

    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(65), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    dtNascimento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Integer, nullable=False)
    carro = db.Column(db.Integer, nullable=False)
    

    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    def __repr__(self):
        return f'<Loja {self.cnpj}>'
