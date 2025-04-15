from models.Loja import Loja
from models.Produto import Produto
from models.Endereco import Endereco




class Produto_Loja():

    produto: Produto
    loja: Loja
    endereco: Endereco
    distancia: float
    id_produto_loja: int

    def __init__(self, produto, loja,endereco = None,distancia = None,id_produto_loja = None):
            self.produto = produto
            self.loja = loja
            self.distancia = distancia
            self.endereco = endereco
            self.id_produto_loja = id_produto_loja

          
