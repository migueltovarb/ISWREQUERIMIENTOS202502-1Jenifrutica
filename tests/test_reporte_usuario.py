import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_notas.settings')
django.setup()

from estudiantes.models import ReporteAcademico, Usuario

print("Usuarios disponibles:")
for u in Usuario.objects.all():
    print(f"- {u.username} ({u.rol})")

username = input("\n¿Con qué usuario estás logueado? ")

usuario = Usuario.objects.filter(username=username).first()

if usuario:
    print(f"\nUsuario encontrado: {usuario.username}")
    
    # Crear reporte de prueba
    reporte = ReporteAcademico.objects.create(
        nombre=f"Reporte de {usuario.username}",
        descripcion="Este es un reporte de prueba",
        tipo_reporte="resumen_general",
        semestre="2025-2",
        activo=True,
        usuario_creador=usuario
    )
    
    print(f"Reporte creado con ID: {reporte.id}")
    print(f"\nReportes de {usuario.username}:")
    for r in ReporteAcademico.objects.filter(usuario_creador=usuario):
        print(f"- ID: {r.id}, Nombre: {r.nombre}")
else:
    print(f"No se encontró el usuario: {username}")
