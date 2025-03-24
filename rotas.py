from flask import Flask, session, redirect, url_for
from classes import db

from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.loja import loja_bp
from routes.endereco import endereco_bp
from routes.menu import menu_bp
from routes.produto import produto_bp


from services.apis import apis_bp



app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Victor%4012@localhost:3306/projetoAutomoveis'
app.config['SECRET_KEY'] = 'Chave()1243123'

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.register_blueprint(loja_bp, url_prefix='/loja')
app.register_blueprint(apis_bp,url_prefix='/apis')
app.register_blueprint(endereco_bp,url_prefix='/endereco')
app.register_blueprint(menu_bp,url_prefix='/menu')
app.register_blueprint(produto_bp,url_prefix='/produto')

@app.route('/')
def index():
    try:
        return redirect(url_for('auth.inicio'))
    except Exception as e:
        session.clear()
        return redirect(url_for('auth.inicio',erro = f"Algo deu errado, acesse o sistema novamente: {e}"))
        
if __name__ == '__main__':
    app.run(debug=True)
