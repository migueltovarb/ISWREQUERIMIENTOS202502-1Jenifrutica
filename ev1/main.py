from contactos import (
    cargar_contactos,
    registrar_contacto,
    modificar_contacto,
    eliminar_contacto,
    listar_contactos,
    buscar_contactos_menu
)

def mostrar_menu():
    print("\n ★ CONNECT ME ★ ")
    print("1. Registrar nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Mostrar listado de contactos")
    print("5. Buscar contacto")
    print("6. Salir")

def main():
    contactos = cargar_contactos()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrar_contacto(contactos)
            contactos = cargar_contactos()
        elif opcion == "2":
            modificar_contacto(contactos)
            contactos = cargar_contactos()
        elif opcion == "3":
            eliminar_contacto(contactos)
            contactos = cargar_contactos()
        elif opcion == "4":
            listar_contactos(contactos)
        elif opcion == "5":
            buscar_contactos_menu(contactos)
        elif opcion == "6":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
