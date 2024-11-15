import subprocess
import time
import os

def parse_pods_output(output):
    printer = "Mostrando pods actualizados:\n"

    # Dividir la salida en líneas
    lines = output.splitlines()
    values = lines[1:]
    line1 = "POD     "  
    line2 = "CPU     "
    line3 = "MEM     "

    for i in range(len(values)):
        values[i] = values[i].split()
        line1 += ("POD"+str(i+1)).ljust(7)
        line2 += values[i][1].ljust(7)
        line3 += values[i][2].ljust(7)

    printer += line1 + "\n" + line2 + "\n" + line3  

    return printer

# Función para ejecutar el comando kubectl y obtener el estado de los pods
def get_pods():
    result = subprocess.run(['kubectl', 'top', 'pods', '-n', 'default'], capture_output=True, text=True)
    return result.stdout

# Bucle infinito para mostrar el estado de los pods
while True:

    printer = parse_pods_output(get_pods())

    os.system('cls')  # Limpia la pantalla de la consola (en Windows)
    
    print(printer)
    
    time.sleep(5)  # Espera 5 segundos antes de volver a ejecutar el comando