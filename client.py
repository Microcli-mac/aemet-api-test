from dotenv import load_dotenv
from fastapi import FastAPI
import os
import requests
import json

# Load .env
load_dotenv()
# Load fastAPI
app = FastAPI()
# Load params
base_url = "https://opendata.aemet.es"
api_key = os.getenv("API_KEY")
headers = {
    "Content-Type": "application/json,text/plain",
    # "Content-Type": "application/json",
    'cache-control': "no-cache",
    'api_key': api_key
}

@app.get("/seasons")
def get_all_seasons():
    print("getting all seasons")
    url = base_url + "/opendata/api/valores/climatologicos/inventarioestaciones/todasestaciones/"
    return __get_request(url)


@app.get("/seasons_by_dates/{init_date}/{end_date}")
def get_all_seasons_by_dates(init_date: str, end_date: str):
    print("getting all seasons by dates")
    url = base_url + f"/opendata/api/valores/climatologicos/diarios/datos/fechaini/{init_date}/fechafin/{end_date}/todasestaciones"
    return __get_request(url)


@app.get("/prediction_by_hourly_municipalities/{municipality_code}")
def get_prediction_by_hourly_municipalities(municipality_code: str):
    print("getting prediction by hourly municipalities")
    url = base_url + f"/opendata/api/prediccion/especifica/municipio/horaria/{municipality_code}"
    return __get_request(url)

@app.get("/municipalities/")
def get_all_municipalities():
    print("getting municipalities")
    url = base_url + "/opendata/api/maestro/municipios"
    return __get_request(url)

@app.get("/forecast_by_code/{code}")
def get_forecast_by_code(code: str):
    print("getting forecast by code")
    url = base_url + f"/opendata/api/prediccion/ccaa/hoy/{code}"
    return __get_request(url, False)

def __get_request(url: str, is_json:bool=True):
    try:
        response = requests.get(
            url,
            headers=headers)
        response.raise_for_status()
        return __get_response(response, is_json)
    except requests.exceptions.RequestException as e:
        print(f"Error al leer los datos: {e}")

def __get_response(value, is_json:bool=True):
    data_json = json.loads(value.text)
    try:
        print(is_json)
        response = requests.get(data_json["datos"])
        response.raise_for_status()
        if is_json:
            return response.json()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error al leer los datos: {e}")