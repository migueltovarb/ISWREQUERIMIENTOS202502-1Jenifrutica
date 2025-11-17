#!/usr/bin/env python
"""
Script para crear datos de prueba para el sistema de gestión de notas
"""
import os
import sys
import django
from django.utils import timezone
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_notas.settings')
django.setup()

from estudiantes.models import Usuario, Curso, Inscripcion, Calificacion, Notificacion


def crear_datos_prueba():
    print("Creando datos de prueba...")
    
    # Verificar si ya existen datos
    if Usuario.objects.filter(rol='profesor').exists():
        print("Ya existen datos de prueba. Eliminando datos existentes...")
        # Eliminar datos existentes (excepto el admin)
        Usuario.objects.exclude(username='admin').delete()
        Curso.objects.all().delete()
        Inscripcion.objects.all().delete()
        Calificacion.objects.all().delete()
        Notificacion.objects.all().delete()
    
    # Crear profesores
    profesor1 = Usuario.objects.create_user(
        username='prof_matematicas',
        email='matematicas@universidad.edu',
        password='prof123',
        first_name='María',
        last_name='González',
        rol='profesor',
        telefono='555-0101'
    )
    
    profesor2 = Usuario.objects.create_user(
        username='prof_fisica',
        email='fisica@universidad.edu',
        password='prof123',
        first_name='Carlos',
        last_name='Rodríguez',
        rol='profesor',
        telefono='555-0102'
    )
    
    # Crear estudiantes
    estudiantes = []
    nombres = ['Ana', 'Luis', 'Carmen', 'Diego', 'Elena', 'Fernando', 'Gabriela', 'Hugo']
    apellidos = ['Martín', 'López', 'García', 'Hernández', 'Jiménez', 'Ruiz', 'Díaz', 'Moreno']
    
    for i, (nombre, apellido) in enumerate(zip(nombres, apellidos)):
        estudiante = Usuario.objects.create_user(
            username=f'estudiante{i+1}',
            email=f'{nombre.lower()}.{apellido.lower()}@estudiante.edu',
            password='est123',
            first_name=nombre,
            last_name=apellido,
            rol='estudiante',
            telefono=f'555-02{i+10:02d}'
        )
        estudiantes.append(estudiante)
    
    # Crear cursos
    curso_matematicas = Curso.objects.create(
        nombre='Matemáticas Avanzadas',
        codigo='MAT-301',
        descripcion='Curso de matemáticas para estudiantes de tercer año',
        creditos=4,
        profesor=profesor1
    )
    
    curso_fisica = Curso.objects.create(
        nombre='Física Cuántica',
        codigo='FIS-401',
        descripcion='Introducción a los principios de la física cuántica',
        creditos=3,
        profesor=profesor2
    )
    
    curso_algebra = Curso.objects.create(
        nombre='Álgebra Linear',
        codigo='MAT-201',
        descripcion='Fundamentos del álgebra linear y matrices',
        creditos=3,
        profesor=profesor1
    )
    
    # Inscribir estudiantes en cursos
    cursos = [curso_matematicas, curso_fisica, curso_algebra]
    
    for estudiante in estudiantes:
        # Cada estudiante se inscribe en 2-3 cursos aleatoriamente
        import random
        cursos_estudiante = random.sample(cursos, random.randint(2, 3))
        
        for curso in cursos_estudiante:
            Inscripcion.objects.create(
                estudiante=estudiante,
                curso=curso,
                fecha_inscripcion=timezone.now()
            )
    
    # Crear calificaciones
    tipos_evaluacion = ['parcial', 'final', 'taller', 'participacion', 'proyecto', 'quiz']
    
    for inscripcion in Inscripcion.objects.all():
        # Crear 3-5 calificaciones por inscripción
        import random
        num_calificaciones = random.randint(3, 5)
        
        for i in range(num_calificaciones):
            tipo = random.choice(tipos_evaluacion)
            nota = round(random.uniform(2.0, 5.0), 1)
            
            calificacion = Calificacion.objects.create(
                inscripcion=inscripcion,
                tipo_evaluacion=tipo,
                nota=Decimal(str(nota)),
                fecha_evaluacion=timezone.now().date(),
                observaciones=f'Evaluación {tipo} - Buen desempeño' if nota >= 3.5 else f'Evaluación {tipo} - Necesita mejorar',
                profesor=inscripcion.curso.profesor
            )
    
    # Crear notificaciones
    for estudiante in estudiantes[:4]:  # Solo para algunos estudiantes
        Notificacion.objects.create(
            usuario=estudiante,
            titulo='Nueva calificación registrada',
            mensaje='Se ha registrado una nueva calificación en uno de tus cursos.',
            tipo='nueva_nota',
            leida=False
        )
    
    # Notificaciones para profesores
    for profesor in [profesor1, profesor2]:
        Notificacion.objects.create(
            usuario=profesor,
            titulo='Recordatorio de evaluación',
            mensaje='Recuerda registrar las calificaciones pendientes.',
            tipo='recordatorio',
            leida=False
        )
    
    print("Datos de prueba creados exitosamente!")
    print(f"- {Usuario.objects.filter(rol='profesor').count()} profesores")
    print(f"- {Usuario.objects.filter(rol='estudiante').count()} estudiantes")
    print(f"- {Curso.objects.count()} cursos")
    print(f"- {Inscripcion.objects.count()} inscripciones")
    print(f"- {Calificacion.objects.count()} calificaciones")
    print(f"- {Notificacion.objects.count()} notificaciones")
    
    print("\nCredenciales de acceso:")
    print("Administrador: admin / admin123")
    print("Profesor 1: prof_matematicas / prof123")
    print("Profesor 2: prof_fisica / prof123")
    print("Estudiante 1: estudiante1 / est123")
    print("Estudiante 2: estudiante2 / est123")
    print("... (estudiante3 a estudiante8 con la misma contraseña)")

if __name__ == '__main__':
    crear_datos_prueba()