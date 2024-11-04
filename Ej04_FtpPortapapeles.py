import subprocess
import pyperclip
import time


def ftp_download():
    # Creamos un proceso utilizando subprocess.Popen para ejecutar el comando 'ftp'
    p1 = subprocess.Popen('ftp', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Lista de comandos que se enviarán al programa FTP
    comandos = [
        b"verbose\n",  # Activa el modo detallado para mostrar más información
        b"open ftp.dlptest.com\n",  # Abre una conexión FTP al servidor 'ftp.dlptest.com'
        b"dlpuser\n",  # Usuario de prueba para la autenticación
        b"rNf50#7\n",  # Contraseña de prueba para la autenticación
        b"ls\n",  # Lista los archivos y directorios en el servidor remoto
        b"get readme.txt\n",  # Descarga el archivo 'readme.txt' desde el servidor
        b"bye\n"  # Cierra la conexión FTP
    ]

    # Iteramos sobre cada comando en la lista y lo enviamos al proceso FTP
    for cmd in comandos:
        p1.stdin.write(cmd)

    # Esperamos hasta 5 segundos a que el proceso termine y capturamos la salida
    respuesta = p1.communicate(timeout=10)


    # Imprimimos la respuesta del servidor FTP
    print("Respuesta del servidor FTP:")
    print(respuesta[0].decode("cp850", "ignore"))
    print(respuesta[1].decode("cp850", "ignore"))

    # Verificamos si el archivo ha sido descargado
    try:
        with open("readme.txt", "r") as file:
            contenido = file.read()
            pyperclip.copy(contenido)  # Copiamos el contenido al portapapeles
            print("Contenido copiado al portapapeles.")
    except FileNotFoundError:
        print("Error: El archivo no se ha encontrado tras la descarga.")


def verificar_portapapeles():
    contenido_anterior = pyperclip.paste()  # Contenido inicial del portapapeles
    print("Comenzando la verificación del portapapeles...")

    while True:
        time.sleep(2)  # Esperamos 2 segundos antes de comprobar nuevamente
        contenido_actual = pyperclip.paste()  # Obtenemos el contenido actual del portapapeles
        if contenido_actual != contenido_anterior:
            print("¡El contenido del portapapeles ha cambiado!")
            contenido_anterior = contenido_actual


if __name__ == "__main__":
    ftp_download()
    verificar_portapapeles()
