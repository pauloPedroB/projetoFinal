from datetime import datetime

class Usuario(object):
    id_usuario = int
    email_usuario = str(120)
    pass_usuario = str(300)
    verificado = datetime
    typeUser = int

    def __init__(self, id_usuario, email_usuario, pass_usuario, verificado, typeUser):
        self.id_usuario = id_usuario
        self.email_usuario = email_usuario
        self.pass_usuario = pass_usuario
        self.verificado = verificado
        self.typeUser = typeUser

