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
    print("Creando datos de prueba renovados...")

    # Eliminar datos previos (excepto admin)
    Usuario.objects.exclude(username='admin').delete()
    Curso.objects.all().delete()
    Inscripcion.objects.all().delete()
    Calificacion.objects.all().delete()
    Notificacion.objects.all().delete()

    # Profesores nuevos
    profesor1 = Usuario.objects.create_user(
        username='prof_biologia',
        email='biologia@universidad.edu',
        password='Bio12345!',
        first_name='Sofía',
        last_name='Ramírez',
        rol='profesor',
        telefono='555-1001'
    )
    profesor2 = Usuario.objects.create_user(
        username='prof_historia',
        email='historia@universidad.edu',
        password='Hist2025@',
        first_name='Javier',
        last_name='Torres',
        rol='profesor',
        telefono='555-1002'
    )
    profesor3 = Usuario.objects.create_user(
        username='prof_literatura',
        email='literatura@universidad.edu',
        password='Lit#2025A',
        first_name='Lucía',
        last_name='Vega',
        rol='profesor',
        telefono='555-1003'
    )

    # Estudiantes nuevos
    estudiantes = []
    nombres = ['Valentina', 'Mateo', 'Isabella', 'Samuel', 'Camila', 'Sebastián', 'Paula', 'Martín', 'Renata', 'Tomás']
    apellidos = ['Castro', 'Mendoza', 'Ortiz', 'Pérez', 'Salazar', 'Ríos', 'Navarro', 'Cortés', 'Luna', 'Vargas']

    for i, (nombre, apellido) in enumerate(zip(nombres, apellidos)):
        estudiante = Usuario.objects.create_user(
            username=f'estudiante{i+1}',
            email=f'{nombre.lower()}.{apellido.lower()}@estudiante.edu',
            password='Estu2025*',
            first_name=nombre,
            last_name=apellido,
            rol='estudiante',
            telefono=f'555-20{i+10:02d}'
        )
        estudiantes.append(estudiante)

    # Cursos nuevos
    curso_biologia = Curso.objects.create(
        nombre='Biología Molecular',
        codigo='BIO-501',
        descripcion='Estudio avanzado de la biología molecular y genética.',
        creditos=4,
        profesor=profesor1
    )
    curso_historia = Curso.objects.create(
        nombre='Historia Universal',
        codigo='HIS-101',
        descripcion='Recorrido por los principales eventos históricos mundiales.',
        creditos=3,
        profesor=profesor2
    )
    curso_literatura = Curso.objects.create(
        nombre='Literatura Latinoamericana',
        codigo='LIT-301',
        descripcion='Análisis de obras y autores latinoamericanos.',
        creditos=2,
        profesor=profesor3
    )
    curso_quimica = Curso.objects.create(
        nombre='Química Orgánica',
        codigo='QUI-401',
        descripcion='Fundamentos y aplicaciones de la química orgánica.',
        creditos=3,
        profesor=profesor1
    )

    cursos = [curso_biologia, curso_historia, curso_literatura, curso_quimica]

    # Inscribir estudiantes en cursos (2-4 cursos aleatorios)
    import random
    for estudiante in estudiantes:
        cursos_estudiante = random.sample(cursos, random.randint(2, 4))
        for curso in cursos_estudiante:
            Inscripcion.objects.create(
                estudiante=estudiante,
                curso=curso,
                fecha_inscripcion=timezone.now()
            )

    # Calificaciones renovadas
    tipos_evaluacion = ['examen', 'trabajo', 'participacion', 'proyecto', 'quiz', 'laboratorio']
    comentarios = [
        'Excelente desempeño',
        'Buen trabajo, sigue así',
        'Puede mejorar en la próxima',
        'Participación destacada',
        'Entrega puntual',
        'Falta mayor dedicación'
    ]

    for inscripcion in Inscripcion.objects.all():
        num_calificaciones = random.randint(2, 5)
        for i in range(num_calificaciones):
            tipo = random.choice(tipos_evaluacion)
            nota = round(random.uniform(1.0, 5.0), 1)
            observacion = random.choice(comentarios)
            Calificacion.objects.create(
                inscripcion=inscripcion,
                tipo_evaluacion=tipo,
                nota=Decimal(str(nota)),
                fecha_evaluacion=timezone.now().date(),
                observaciones=f'{tipo.capitalize()}: {observacion}',
                profesor=inscripcion.curso.profesor
            )

    # Notificaciones renovadas
    mensajes_estudiantes = [
        'Tienes una nueva calificación en Biología Molecular.',
        'Recuerda entregar tu proyecto de Historia Universal.',
        'Participa en el foro de Literatura Latinoamericana.',
        'Laboratorio de Química Orgánica programado para el viernes.'
    ]
    for estudiante in estudiantes[:6]:
        Notificacion.objects.create(
            usuario=estudiante,
            titulo='Aviso académico',
            mensaje=random.choice(mensajes_estudiantes),
            tipo='info',
            leida=False
        )

    mensajes_profesores = [
        'Hay inscripciones nuevas en tu curso.',
        'Recuerda calificar los trabajos pendientes.',
        'Se ha programado una reunión de profesores.'
    ]
    for profesor in [profesor1, profesor2, profesor3]:
        Notificacion.objects.create(
            usuario=profesor,
            titulo='Notificación administrativa',
            mensaje=random.choice(mensajes_profesores),
            tipo='admin',
            leida=False
        )

    print("Datos de prueba renovados creados exitosamente!")
    print(f"- {Usuario.objects.filter(rol='profesor').count()} profesores")
    print(f"- {Usuario.objects.filter(rol='estudiante').count()} estudiantes")
    print(f"- {Curso.objects.count()} cursos")
    print(f"- {Inscripcion.objects.count()} inscripciones")
    print(f"- {Calificacion.objects.count()} calificaciones")
    print(f"- {Notificacion.objects.count()} notificaciones")

    print("\nCredenciales de acceso:")
    print("Administrador: admin / admin123")
    print("Profesor 1: prof_biologia / Bio12345!")
    print("Profesor 2: prof_historia / Hist2025@")
    print("Profesor 3: prof_literatura / Lit#2025A")
    print("Estudiante 1: estudiante1 / Estu2025*")
    print("Estudiante 2: estudiante2 / Estu2025*")
    print("... (estudiante3 a estudiante10 con la misma contraseña)")

if __name__ == '__main__':
    crear_datos_prueba()