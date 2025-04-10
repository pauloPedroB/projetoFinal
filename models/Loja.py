from datetime import datetime
from models.Usuario import Usuario

class Loja():
    id_loja: int
    cnpj: str
    nomeFantasia: str
    razaoSocial: str
    telefone: str
    celular: str
    abertura: datetime
    usuario: Usuario
    def __init__(self, id_loja, cnpj, nomeFantasia, razaoSocial, telefone, celular, abertura, usuario):
        self.id_loja = id_loja
        self.cnpj = cnpj
        self.nomeFantasia = nomeFantasia
        self.razaoSocial = razaoSocial
        self.telefone = telefone
        self.celular = celular
        self.abertura = abertura
        self.usuario = usuario

    
    
