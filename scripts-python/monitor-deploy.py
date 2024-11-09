import subprocess
import time
import os

def parse_deployments_output(output):
    lines = output.splitlines()
    values = lines[1].split()

    printer = "Mostrando deployments actualizados:\n"
    line1 = "ETATUS            " + values[1]
    line2 = "UPDATE            " + values[2]
    line3 = "AVAILABLE         " + values[3]
    line4 = "AGE               " + values[4]

    printer += line1 + "\n" + line2 + "\n" + line3 + "\n" + line4

    return printer


def get_deployments():
    result = subprocess.run(['kubectl', 'get', 'deployments', '-n', 'default'], capture_output=True, text=True)
    return result.stdout

while True:
    printer = parse_deployments_output(get_deployments())

    os.system('cls')

    print(printer)

    time.sleep(5)