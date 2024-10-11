# controller/import_scripts/api_totvs.py

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter a raiz da URL a partir da variável de ambiente
base_url = os.getenv('API_URL')

# Verificar se a variável de ambiente foi definida
if not base_url:
    raise ValueError("A variável de ambiente 'API_URL' não está definida.")

# Definir os endpoints concatenando a base_url com os caminhos específicos
endpoint_departments = f"{base_url}/api/framework/v1/consultaSQLServer/RealizaConsulta/APP.ENF1/1/S"
endpoint_employees = f"{base_url}/api/framework/v1/consultaSQLServer/RealizaConsulta/APP.ENF2/1/S"
endpoint_students = f"{base_url}/api/framework/v1/consultaSQLServer/RealizaConsulta/APP.ENF3/1/S"
endpoint_class = f"{base_url}/api/framework/v1/consultaSQLServer/RealizaConsulta/APP.ENF4/1/S"

# Cabeçalhos 
headers = {
    "Content-Type": "application/json",    
}

# Credenciais da API
api_login = os.getenv('API_LOGIN')
api_password = os.getenv('API_PASSWORD')    

def get_data(endpoint):
    try:
        response = requests.get(endpoint, headers=headers, auth=HTTPBasicAuth(api_login, api_password))
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro: {err}")
    return None


