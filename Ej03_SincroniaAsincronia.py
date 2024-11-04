import subprocess
import time


def ejecutar_sincrono():
    print("Ejecutando Notepad de manera síncrona (bloqueante)...")
    inicio = time.time()

    # Ejecutar de manera síncrona, el programa espera a que Notepad se cierre
    subprocess.run("notepad.exe")

    fin = time.time()
    duracion = fin - inicio
    print(f"Tiempo de ejecución síncrona: {duracion:.2f} segundos"
)

def ejecutar_asincrono():
    print("Ejecutando Notepad de manera asíncrona (no bloqueante)...")
    inicio = time.time()

    # Ejecutar de manera asíncrona, el programa no espera a que Notepad se cierre
    proceso = subprocess.Popen("notepad.exe")

    # El tiempo se mide justo después de iniciar Notepad, sin esperar a que se cierre
    fin = time.time()
    duracion = fin - inicio
    print(f"Tiempo de ejecución asíncrona: {duracion:.2f} segundos")


def main():
    opcion = input("¿Deseas ejecutar Notepad de manera síncrona (s) o asíncrona (a)? ").strip().lower()

    if opcion == 's':
        ejecutar_sincrono()
    elif opcion == 'a':
        ejecutar_asincrono()
    else:
        print("Opción no válida. Por favor, elige 's' para síncrona o 'a' para asíncrona.")


# Ejecutar el programa principal
if __name__ == "__main__":
    main()
