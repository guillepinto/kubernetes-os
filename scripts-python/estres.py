import requests
import time
import os

os.system("cls")

def hacer_solicitud():
    url = "http://localhost:31000/congruencial/lineal"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta una excepción si el estado no es 2xx
        print(f"Respuesta: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")

while True:
    hacer_solicitud()
    time.sleep(15)