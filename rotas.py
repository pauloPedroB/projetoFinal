from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from geopy.distance import geodesic
import services.validacoes as validacoes
from classes import db, Endereco

from routes.auth import auth_bp
from routes.cliente import cliente_bp
from routes.loja import loja_bp
from routes.endereco import endereco_bp
from routes.menu import menu_bp
from routes.produto import produto_bp


from services.email_service import email_service
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
app.register_blueprint(email_service,url_prefix='/email')
app.register_blueprint(apis_bp,url_prefix='/apis')
app.register_blueprint(endereco_bp,url_prefix='/endereco')
app.register_blueprint(menu_bp,url_prefix='/menu')
app.register_blueprint(produto_bp,url_prefix='/produto')

@app.route('/')
def index():
    try:
        return redirect(url_for('auth.inicio'))
    except:
        session.clear()
        return redirect(url_for('auth.inicio',erro = "Algo deu errado, acesse o sistema novamente"))
        
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
    



if __name__ == '__main__':
    app.run(debug=True)
