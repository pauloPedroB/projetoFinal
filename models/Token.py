from datetime import datetime
from models.Usuario import Usuario


class Token():
    id_token = int
    dt_cr = datetime
    usado = bool
    usuario = Usuario

    def __init__(self, id_token, dt_cr, usado, usuario):
        self.id_token = id_token
        self.dt_cr = dt_cr
        self.usado = usado
        self.usuario = usuario
