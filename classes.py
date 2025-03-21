from flask_sqlalchemy import SQLAlchemy
from models import Usuario
from controllers.userController import buscarPorId
db = SQLAlchemy()

class Endereco(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(65), nullable=False)
    bairro = db.Column(db.String(40), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(8),unique = True, nullable=False)
    complemento = db.Column(db.String(200), nullable=False)
    uf = db.Column(db.String(2), nullable=False)
    nmr = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    id_usuario = db.Column(db.Integer, unique=True, nullable=False)

    _usuario_obj = None  # Cache para armazenar o usuário

    @property
    def usuario(self):
        """Busca os dados do usuário na API apenas na primeira vez."""
        if self._usuario_obj is None:
            self._usuario_obj, _ = buscarPorId(self.id_usuario)  # Busca usuário na API
        return self._usuario_obj

    def __repr__(self):
        return f'<Endereco {self.rua}>'

class Loja(db.Model):
    __tablename__ = 'lojas'

    id_loja = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cnpj = db.Column(db.String(14), unique=True, nullable=False)
    nomeFantasia = db.Column(db.String(65), nullable=False)
    razaoSocial = db.Column(db.String(65), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    celular = db.Column(db.String(20), nullable=True)
    abertura = db.Column(db.Date, nullable=False)

    id_usuario = db.Column(db.Integer, unique=True, nullable=False)

    _usuario_obj = None  # Cache para armazenar o usuário

    @property
    def usuario(self):
        """Busca os dados do usuário na API apenas na primeira vez."""
        if self._usuario_obj is None:
            self._usuario_obj, _ = buscarPorId(self.id_usuario)  # Busca usuário na API
        return self._usuario_obj

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

    id_usuario = db.Column(db.Integer, unique=True, nullable=False)

    _usuario_obj = None  # Cache para armazenar o usuário

    @property
    def usuario(self):
        """Busca os dados do usuário na API apenas na primeira vez."""
        if self._usuario_obj is None:
            self._usuario_obj, _ = buscarPorId(self.id_usuario)  # Busca usuário na API
        return self._usuario_obj

    def __repr__(self):
        return f'<Cliente {self.nome} (Usuário: {self.usuario.email_usuario if self.usuario else "Não encontrado"})>'

class Administrador(db.Model):
    __tablename__ = 'administradores'

    id_adm = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(65), nullable=False)

    id_usuario = db.Column(db.Integer, unique=True, nullable=False)

    _usuario_obj = None  # Cache para armazenar o usuário

    @property
    def usuario(self):
        """Busca os dados do usuário na API apenas na primeira vez."""
        if self._usuario_obj is None:
            self._usuario_obj, _ = buscarPorId(self.id_usuario)  # Busca usuário na API
        return self._usuario_obj

    def __repr__(self):
        return f'<Administrador {self.id_adm}>'

class Produto(db.Model):
    __tablename__ = 'produtos'

    id_produto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    img = db.Column(db.String(300), nullable=False)


    def __repr__(self):
        return f'<Produto {self.id_produto}>'

class Produto_Loja(db.Model):
    __tablename__ = 'produto_loja'

    id_produto_loja = db.Column(db.Integer, primary_key=True, autoincrement=True)

    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    id_loja = db.Column(db.Integer, db.ForeignKey('lojas.id_loja'), nullable=False)

    def __repr__(self):
        return f'<Produto Loja {self.id_produto_loja}>'

