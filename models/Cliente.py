from datetime import datetime
from models.Usuario import Usuario

class Cliente():
    id_cliente = int
    cpf = str(11)
    nome = str(65)
    telefone = str(20)
    dtNascimento = datetime
    genero = int
    carro = int
    usuario = Usuario

    def __init__(self, id_cliente, cpf, nome, telefone, dtNascimento, genero, carro, usuario):
        self.id_cliente = id_cliente
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.dtNascimento = dtNascimento
        self.genero = genero
        self.carro = carro
        self.usuario = usuario
    