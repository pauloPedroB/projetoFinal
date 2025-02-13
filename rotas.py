from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import requests
from geopy.geocoders import Nominatim, OpenCage
from geopy.exc import GeocoderTimedOut
from geopy.distance import geodesic

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://aluno:toor@localhost:3306/projetoAutomoveis'
app.config['SECRET_KEY'] = 'Chave()1243123'

db = SQLAlchemy(app)

class Endereco(db.Model):
    __tablename__ = 'enderecos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rua = db.Column(db.String(50), nullable=False)
    nmr = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f'<Endereco {self.rua}>'


def logout():
    session.clear()

def consultar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if "erro" not in dados:
            return True, dados
        else:
            return False, "Cep Não encontrado"
    else:
        return False,"Erro na requisição."




def obter_lat_long(endereco):
    # Primeiro, tente usar o Nominatim
    geolocator_nominatim = Nominatim(user_agent="myGeocoder")
    
    try:
        localizacao = geolocator_nominatim.geocode(endereco, timeout=10)
        if localizacao:
            return {"latitude": localizacao.latitude, "longitude": localizacao.longitude}
    except GeocoderTimedOut:
        print("Erro de timeout com Nominatim.")
    
    # Se o Nominatim não funcionar, tente o OpenCage
    chave_api_opencage = '25fc62d0f13d40448e3f206d06bc89bd'
    geolocator_opencage = OpenCage(api_key=chave_api_opencage)
    
    try:
        localizacao = geolocator_opencage.geocode(endereco)
        if localizacao:
            return {"latitude": localizacao.latitude, "longitude": localizacao.longitude}
    except Exception as e:
        print(f"Erro ao tentar o OpenCage: {e}")
    
    partes_endereco = endereco.split(',')
    
    bairro = partes_endereco[1] if len(partes_endereco) > 1 else None
    cidade = partes_endereco[2] if len(partes_endereco) > 2 else partes_endereco[1]

    if bairro and cidade:
        endereco_bairro_cidade = f"{bairro.strip()}, {cidade.strip()}"
        try:
            localizacao_bairro_cidade = geolocator_opencage.geocode(endereco_bairro_cidade)
            if localizacao_bairro_cidade:
                return {"latitude": localizacao_bairro_cidade.latitude, "longitude": localizacao_bairro_cidade.longitude}
        except Exception as e:
            print(f"Erro ao tentar buscar o bairro e cidade com OpenCage: {e}")
    
    return None

    
@app.route('/buscar_cep', methods=['GET'])
def buscar_cep():
    cep = request.args.get('cep')

    if not cep or len(cep) != 8 or not cep.isdigit():
        return render_template('index.html', erro="Cep Inválido", dados=None)
    
    sucesso, endereco = consultar_cep(cep)
    endereco_completo = endereco
    if sucesso:
        endereco_formatado = f'{endereco["logradouro"]}, {endereco["bairro"]}, {endereco["localidade"]}, {endereco["uf"]}, Brasil'
        
        latLong = obter_lat_long(endereco_formatado)
        
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

@app.route('/')
def inicio():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
