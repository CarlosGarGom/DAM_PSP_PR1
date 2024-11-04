import os
import sys

#Ejecutar en https://www.online-python.com/
#Subir tambien ejercicio2.txt

def main():
    # Nombre del archivo que el padre va a enviar al hijo
    archivo_nombre = "ejercicio2.txt"

    # Creamos dos pipes para la comunicación bidireccional
    fd_padre_a_hijo = os.pipe()  # Pipe para que el padre envíe al hijo
    fd_hijo_a_padre = os.pipe()  # Pipe para que el hijo envíe al padre

    # Crear un proceso hijo con fork()
    pid = os.fork()

    if pid < 0:
        # Error en la creación del proceso hijo
        print("No se ha podido crear el proceso hijo...")
        sys.exit(1)

    elif pid == 0:
        # Código del proceso hijo
        # Cerrar las partes del pipe que no se usan en el hijo
        os.close(fd_padre_a_hijo[1])  # Cerrar escritura del pipe padre->hijo
        os.close(fd_hijo_a_padre[0])  # Cerrar lectura del pipe hijo->padre

        # Leer contenido del archivo enviado por el padre
        contenido = os.read(fd_padre_a_hijo[0], 1024).decode("utf-8")

        # Calcular el número de líneas y palabras
        lineas = contenido.strip().splitlines()
        num_lineas = len(lineas)
        num_palabras = sum(len(linea.split()) for linea in lineas)

        # Enviar el resultado al padre
        resultado = f"Líneas: {num_lineas}, Palabras: {num_palabras}"
        os.write(fd_hijo_a_padre[1], resultado.encode("utf-8"))
        print("El hijo envía el conteo de líneas y palabras al padre...")

        # Cerrar descriptores de lectura y escritura en el hijo
        os.close(fd_padre_a_hijo[0])
        os.close(fd_hijo_a_padre[1])

    else:
        # Código del proceso padre
        # Cerrar las partes del pipe que no se usan en el padre
        os.close(fd_padre_a_hijo[0])  # Cerrar lectura del pipe padre->hijo
        os.close(fd_hijo_a_padre[1])  # Cerrar escritura del pipe hijo->padre

        # Leer el contenido del archivo y enviarlo al hijo
        try:
            with open(archivo_nombre, "r") as archivo:
                contenido = archivo.read()
            os.write(fd_padre_a_hijo[1], contenido.encode("utf-8"))
            print(f"El padre envía el contenido del archivo '{archivo_nombre}' al hijo...")
        except FileNotFoundError:
            print(f"El archivo '{archivo_nombre}' no se encuentra.")
            sys.exit(1)

        # Esperar la respuesta del hijo
        mensaje_recibido = os.read(fd_hijo_a_padre[0], 1024).decode("utf-8")
        print(f"El padre recibe del hijo: {mensaje_recibido}")

        # Cerrar descriptores de lectura y escritura en el padre
        os.close(fd_padre_a_hijo[1])
        os.close(fd_hijo_a_padre[0])

        # Esperar a que el proceso hijo termine
        os.wait()


# Ejecutar el programa
if __name__ == "__main__":
    main()
