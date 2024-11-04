import os
import sys

#Ejecutar en https://www.online-python.com/


def main():
    # Creamos dos pipes para comunicación bidireccional
    fd_padre_a_hijo = os.pipe()  # Pipe para que el padre envíe al hijo
    fd_hijo_a_padre = os.pipe()  # Pipe para que el hijo envíe al padre

    # Mensaje que el padre enviará al hijo
    saludo_padre = "Buenos días, hijo.\n"

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

        # Leer mensaje del padre
        buffer = os.read(fd_padre_a_hijo[0], 80).decode("utf-8")
        print(f"El hijo recibe del padre: {buffer}")

        # Modificar el mensaje a mayúsculas
        mensaje_modificado = buffer.upper()

        # Enviar el mensaje modificado de vuelta al padre
        os.write(fd_hijo_a_padre[1], mensaje_modificado.encode("utf-8"))
        print("El hijo envía el mensaje modificado al padre...")

        # Cerrar descriptores de lectura y escritura en el hijo
        os.close(fd_padre_a_hijo[0])
        os.close(fd_hijo_a_padre[1])

    else:
        # Código del proceso padre
        # Cerrar las partes del pipe que no se usan en el padre
        os.close(fd_padre_a_hijo[0])  # Cerrar lectura del pipe padre->hijo
        os.close(fd_hijo_a_padre[1])  # Cerrar escritura del pipe hijo->padre

        # Enviar el mensaje al hijo
        os.write(fd_padre_a_hijo[1], saludo_padre.encode("utf-8"))
        print("El padre envía un mensaje al hijo...")

        # Esperar la respuesta del hijo
        mensaje_recibido = os.read(fd_hijo_a_padre[0], 80).decode("utf-8")
        print(f"El padre recibe del hijo: {mensaje_recibido}")

        # Cerrar descriptores de lectura y escritura en el padre
        os.close(fd_padre_a_hijo[1])
        os.close(fd_hijo_a_padre[0])

        # Esperar a que el proceso hijo termine
        os.wait()

# Ejecutar el programa
if __name__ == "__main__":
    main()
