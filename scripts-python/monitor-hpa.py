import subprocess
import time
import os

def parse_hpa_output(output):
    # Dividir la salida en líneas y crear un DataFrame
    lines = output.splitlines()
    columns = lines[0].split()
    values = lines[1].split()

    aux = values[3]
    del values[3]

    values[2] = values[2] + " " + aux

    printer = "Mostrando HPA actualizado:\n"

    for i in range(len(columns)):
        printer += f"{columns[i]}: {values[i]}\n"
    
    return printer

# Función para ejecutar el comando kubectl y obtener el estado del HPA
def get_hpa():
    result = subprocess.run(['kubectl', 'get', 'hpa', '-n', 'default'], capture_output=True, text=True)
    return result.stdout

# Bucle infinito para mostrar el estado del HPA
while True:
    printer = parse_hpa_output(get_hpa())

    os.system('cls')  # Limpia la pantalla de la consola (en Windows)
    
    print(printer)
    
    time.sleep(5)  # Espera 5 segundos antes de volver a ejecutar el comando
