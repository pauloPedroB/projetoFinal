from models.Usuario import Usuario

class Endereco():
    id: int
    rua: str
    bairro: str
    cidade: str
    cep: str
    complemento: str
    uf: str
    nmr: int
    latitude: str
    longitude: str
    usuario: Usuario
    def __init__(self, id, rua, bairro, cidade, cep, complemento, uf, nmr,latitude,longitude,usuario):
        self.id = id
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.complemento = complemento
        self.uf = uf
        self.nmr = nmr
        self.latitude = latitude
        self.longitude = longitude
        self.usuario = usuario

