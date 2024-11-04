import psutil


def listar_procesos_activos():
    # Solicita al usuario una lista de nombres de procesos a verificar
    nombres_procesos = input("Introduce una lista de nombres de procesos separados por comas: ").split(",")
    nombres_procesos = [nombre.strip().lower() for nombre in nombres_procesos]

    # Solicita la palabra clave para filtrar los procesos
    palabra_clave = input("Introduce la palabra clave para filtrar los procesos: ").strip().lower()

    print(f"\n{'Nombre':<25} {'PID':<10} {'Memoria (MB)':<15}")
    print("-" * 50)
    procesos_encontrados = False

    # Filtrar y mostrar procesos que contienen la palabra clave y están en la lista de nombres especificados
    for proceso in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            nombre = proceso.info['name'].lower() if proceso.info['name'] else ""
            if any(nombre_proceso in nombre for nombre_proceso in nombres_procesos) and palabra_clave in nombre:
                pid = proceso.info['pid']
                memoria_uso = proceso.info['memory_info'].rss / (1024 * 1024)  # Convertir a MB
                print(f"{nombre:<25} {pid:<10} {memoria_uso:<15.2f}")
                procesos_encontrados = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if not procesos_encontrados:
        print(f"No se encontraron procesos que coincidan con los criterios especificados.")
        quit()


def finalizar_proceso(nombre_proceso):
    procesos_finalizados = False

    for proceso in psutil.process_iter(['pid', 'name']):
        try:
            if nombre_proceso.lower() == proceso.info['name'].lower():
                proceso.terminate()
                proceso.wait()  # Espera a que el proceso se finalice
                print(f"Proceso '{nombre_proceso}' con PID {proceso.info['pid']} finalizado correctamente.")
                procesos_finalizados = True
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            procesos_finalizados = True
            print(f"No se pudo finalizar el proceso '{nombre_proceso}': {e}")

    if not procesos_finalizados:
        print(f"No se encontraron procesos llamados '{nombre_proceso}'.")


if __name__ == "__main__":
    listar_procesos_activos()

    opcion = input("\n¿Desea finalizar un proceso por su nombre? (s/n): ").strip().lower()
    if opcion == 's':
        nombre_proceso = input("Ingrese el nombre exacto del proceso que desea finalizar: ").strip()
        finalizar_proceso(nombre_proceso)

    print("\n---\n")
