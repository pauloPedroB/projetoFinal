from flask import Blueprint, request, jsonify
import requests

apis_bp = Blueprint('apis', __name__)


@apis_bp.route('/consultar_cnpj', methods=['GET'])
def consultar_cnpj():
    cnpj = request.args.get('cnpj')
    if cnpj:
        url = f'https://www.receitaws.com.br/v1/cnpj/{cnpj}'
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'CNPJ não encontrado'}), 404
    return jsonify({'error': 'CNPJ inválido'}), 400

