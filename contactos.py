import os
import json

ARCHIVO_CONTACTOS = "contactos.json"

class Contacto:
    def __init__(self, nombre, telefono, correo, cargo):
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.cargo = cargo

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "correo": self.correo,
            "cargo": self.cargo
        }

    def from_dict(data):
        return Contacto(
            data["nombre"],
            data["telefono"],
            data["correo"],
            data["cargo"]
        )



def cargar_contactos():
    if not os.path.exists(ARCHIVO_CONTACTOS):
        return []
    try:
        with open(ARCHIVO_CONTACTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Contacto.from_dict(c) for c in datos]
    except (json.JSONDecodeError, ValueError):
        return []



def guardar_contactos(contactos):
    with open(ARCHIVO_CONTACTOS, "w", encoding="utf-8") as f:
        json.dump([c.to_dict() for c in contactos], f, ensure_ascii=False, indent=2)



def buscar_contacto(contactos, criterio):
    return [c for c in contactos if criterio.lower() in c.nombre.lower() or criterio.lower() in c.correo.lower()]



def existe_correo(contactos, correo):
    return any(c.correo.lower() == correo.lower() for c in contactos)



def registrar_contacto(contactos):
    print("\n--- Registrar nuevo contacto ---")
    nombre = input("Nombre: ").strip()
    telefono = input("Número de teléfono: ").strip()
    correo = input("Correo electrónico: ").strip()
    cargo = input("Cargo en la empresa: ").strip()
    if existe_correo(contactos, correo):
        print("Error: ya existe un contacto con ese correo electrónico.")
        return
    contacto = Contacto(nombre, telefono, correo, cargo)
    contactos.append(contacto)
    guardar_contactos(contactos)
    print("Contacto registrado exitosamente.")



def eliminar_contacto(contactos):
    print("\n--- Eliminar contacto ---")
    correo = input("Ingrese el correo electrónico del contacto a eliminar: ").strip()
    encontrados = [c for c in contactos if c.correo.lower() == correo.lower()]
    if not encontrados:
        print("Error: este contacto no existe.")
        return
    print(f"¿Está seguro que desea eliminar el contacto '{encontrados[0].nombre}'? (s/n)")
    confirm = input().strip().lower()
    if confirm == "s":
        contactos.remove(encontrados[0])
        guardar_contactos(contactos)
        print("Contacto eliminado exitosamente.")
    else:
        print("Acción cancelada.")



def modificar_contacto(contactos):
    print("\n--- Modificar información de contacto ---")
    correo = input("Ingrese el correo electrónico del contacto a modificar: ").strip()
    encontrados = [c for c in contactos if c.correo.lower() == correo.lower()]
    if not encontrados:
        print("Error: este contacto no existe.")
        return
    contacto = encontrados[0]
    print(f"Contacto actual: Nombre: {contacto.nombre}, Teléfono: {contacto.telefono}, Correo: {contacto.correo}, Cargo: {contacto.cargo}")
    print("¿Está seguro que desea modificar este contacto? (s/n)")
    confirm = input().strip().lower()
    if confirm != "s":
        print("Acción cancelada.")
        return
    nombre = input(f"Nuevo nombre [{contacto.nombre}]: ").strip() or contacto.nombre
    telefono = input(f"Nuevo teléfono [{contacto.telefono}]: ").strip() or contacto.telefono
    nuevo_correo = input(f"Nuevo correo [{contacto.correo}]: ").strip() or contacto.correo
    cargo = input(f"Nuevo cargo [{contacto.cargo}]: ").strip() or contacto.cargo
    if nuevo_correo != contacto.correo and existe_correo(contactos, nuevo_correo):
        print("Error: ya existe un contacto con ese correo electrónico.")
        return
    contacto.nombre = nombre
    contacto.telefono = telefono
    contacto.correo = nuevo_correo
    contacto.cargo = cargo
    guardar_contactos(contactos)
    print("Contacto modificado exitosamente.")



def listar_contactos(contactos):
    print("\n--- Lista de contactos ---")
    if not contactos:
        print("No hay contactos registrados.")
        return
    for idx, c in enumerate(contactos, 1):
        print(f"{idx}. Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")



def buscar_contactos_menu(contactos):
    print("\n--- Buscar contacto ---")
    criterio = input("Ingrese nombre o correo a buscar: ").strip()
    resultados = buscar_contacto(contactos, criterio)
    if not resultados:
        print("Error: este contacto no existe.")
        return
    for c in resultados:
        print(f"Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")