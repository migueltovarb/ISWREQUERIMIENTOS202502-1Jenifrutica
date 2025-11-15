import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_notas.settings')
django.setup()

from estudiantes.models import ReporteAcademico, Usuario

# Obtener el primer usuario administrador
admin = Usuario.objects.filter(rol='administrador').first()

if admin:
    print(f"Usuario encontrado: {admin.username}")
    
    # Crear reporte de prueba
    reporte = ReporteAcademico.objects.create(
        nombre="Reporte de Prueba",
        descripcion="Este es un reporte de prueba",
        tipo_reporte="resumen_general",
        semestre="2025-2",
        activo=True,
        usuario_creador=admin
    )
    
    print(f"Reporte creado con ID: {reporte.id}")
    print(f"Total reportes en BD: {ReporteAcademico.objects.count()}")
    
    # Listar todos los reportes
    print("\nReportes guardados:")
    for r in ReporteAcademico.objects.all():
        print(f"- ID: {r.id}, Nombre: {r.nombre}, Usuario: {r.usuario_creador.username}")
else:
    print("No se encontró ningún usuario administrador")
