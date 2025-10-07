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

    @staticmethod
    def from_dict(data):
        return Contacto(
            data["nombre"],
            data["telefono"],
            data["correo"],
            data["cargo"]
        )



def cargar_contactos():
    if not os.path.exists(ARCHIVO_CONTACTOS):
        # Crear el archivo vacío si no existe
        with open(ARCHIVO_CONTACTOS, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []
    try:
        with open(ARCHIVO_CONTACTOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Contacto.from_dict(c) for c in datos]
    except (json.JSONDecodeError, ValueError):
        return []



def guardar_contactos(contactos):
    try:
        with open(ARCHIVO_CONTACTOS, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in contactos], f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error al guardar contactos: {e}")



def buscar_contacto(contactos, criterio):
    return [c for c in contactos if criterio.lower() in c.nombre.lower() or criterio.lower() in c.correo.lower()]



def existe_correo(contactos, correo):
    return any(c.correo.lower() == correo.lower() for c in contactos)



def existe_nombre(contactos, nombre):
    return any(c.nombre.lower() == nombre.lower() for c in contactos)



def existe_telefono(contactos, telefono):
    return any(c.telefono.lower() == telefono.lower() for c in contactos)



def registrar_contacto(contactos):
    print("\n ★ Registrar nuevo contacto  ★")
    nombre = input("Nombre: ").strip()
    telefono = input("Número de teléfono: ").strip()
    if len(telefono) > 20:
        print("Error: el número de teléfono no puede superar los 20 caracteres.")
        return
    correo = input("Correo electrónico: ").strip()
    cargo = input("Cargo en la empresa: ").strip()
    if existe_correo(contactos, correo):
        print("Error: ya existe un contacto con ese correo electrónico.")
        return
    if existe_nombre(contactos, nombre) and existe_telefono(contactos, telefono):
        print("Error: ya existe un contacto con ese nombre y número de teléfono.")
        return
    contacto = Contacto(nombre, telefono, correo, cargo)
    contactos.append(contacto)
    guardar_contactos(contactos)
    print("Contacto registrado exitosamente.")



def eliminar_contacto(contactos):
    print("\n ★ Eliminar contacto ★ ")
    criterio = input("Ingrese el nombre, correo electrónico o número de teléfono del contacto a eliminar: ").strip().lower()
    encontrados = [
        c for c in contactos
        if criterio == c.correo.lower()
        or criterio == c.nombre.lower()
        or criterio == c.telefono.lower()
    ]
    if not encontrados:
        print("Error: este contacto no existe.")
        return
    print(f"Se encontraron {len(encontrados)} contacto(s):")
    for idx, c in enumerate(encontrados, 1):
        print(f"{idx}. Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")
    if len(encontrados) > 1:
        seleccion = input("Ingrese el número del contacto que desea eliminar: ").strip()
        if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(encontrados):
            print("Selección inválida.")
            return
        contacto_a_eliminar = encontrados[int(seleccion) - 1]
    else:
        contacto_a_eliminar = encontrados[0]
    print(f"¿Está seguro que desea eliminar el contacto '{contacto_a_eliminar.nombre}'? (s/n)")
    confirm = input().strip().lower()
    if confirm == "s":
        contactos.remove(contacto_a_eliminar)
        guardar_contactos(contactos)
        print("Contacto eliminado exitosamente.")
    else:
        print("Acción cancelada.")



def modificar_contacto(contactos):
    print("\n ★ Modificar información de contacto ★ ")
    criterio = input("Ingrese el nombre o correo electrónico del contacto a modificar: ").strip().lower()
    encontrados = [
        c for c in contactos
        if criterio == c.correo.lower() or criterio == c.nombre.lower()
    ]
    if not encontrados:
        print("Error: este contacto no existe.")
        return
    if len(encontrados) > 1:
        print(f"Se encontraron {len(encontrados)} contacto(s):")
        for idx, c in enumerate(encontrados, 1):
            print(f"{idx}. Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")
        seleccion = input("Ingrese el número del contacto que desea modificar: ").strip()
        if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(encontrados):
            print("Selección inválida.")
            return
        contacto = encontrados[int(seleccion) - 1]
    else:
        contacto = encontrados[0]
    print(f"Contacto actual: Nombre: {contacto.nombre}, Teléfono: {contacto.telefono}, Correo: {contacto.correo}, Cargo: {contacto.cargo}")
    print("¿Está seguro que desea modificar la información de este contacto? (si/no)")
    confirm = input().strip().lower()
    if confirm != "si":
        print("Acción cancelada.")
        return
    nombre = input(f"Nuevo nombre [{contacto.nombre}]: ").strip() or contacto.nombre
    telefono = input(f"Nuevo teléfono [{contacto.telefono}]: ").strip() or contacto.telefono
    if len(telefono) > 20:
        print("Error: el número de teléfono no puede superar los 20 caracteres.")
        return
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
    print("\n ★ Lista de contactos  ★")
    if not contactos:
        print("No hay contactos registrados.")
        return
    for idx, c in enumerate(contactos, 1):
        print(f"{idx}. Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")



def buscar_contactos_menu(contactos):
    print("\n ★ Buscar contacto  ★")
    criterio = input("Ingrese nombre o correo a buscar: ").strip()
    resultados = buscar_contacto(contactos, criterio)
    if not resultados:
        print("Error: este contacto no existe.")
        return
    for c in resultados:
        print(f"Nombre: {c.nombre}, Teléfono: {c.telefono}, Correo: {c.correo}, Cargo: {c.cargo}")