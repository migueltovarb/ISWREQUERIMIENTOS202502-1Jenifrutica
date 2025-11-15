from django.core.management.base import BaseCommand
from estudiantes.models import Usuario, Curso, Inscripcion, Calificacion, Notificacion
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos de prueba en el sistema TROLI'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando carga de datos de prueba...'))

        # Crear Administrador
        admin, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'email': 'admin@troli.edu.co',
                'rol': 'administrador',
                'activo': True,
            }
        )
        if created:
            admin.set_password('Admin123@')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Administrador creado: admin / Admin123@'))
        else:
            self.stdout.write(self.style.WARNING('Administrador ya existe'))

        # Crear Profesor
        profesor, created = Usuario.objects.get_or_create(
            username='profesor1',
            defaults={
                'first_name': 'María',
                'last_name': 'García',
                'email': 'maria.garcia@troli.edu.co',
                'rol': 'profesor',
                'activo': True,
            }
        )
        if created:
            profesor.set_password('Profesor123@')
            profesor.save()
            self.stdout.write(self.style.SUCCESS('Profesor creado: profesor1 / Profesor123@'))
        else:
            self.stdout.write(self.style.WARNING('Profesor ya existe'))

        # Crear Estudiantes
        estudiante1, created = Usuario.objects.get_or_create(
            username='estudiante1',
            defaults={
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'email': 'juan.perez@estudiante.troli.edu.co',
                'rol': 'estudiante',
                'activo': True,
            }
        )
        if created:
            estudiante1.set_password('Estudiante123@')
            estudiante1.save()
            self.stdout.write(self.style.SUCCESS('Estudiante 1 creado: estudiante1 / Estudiante123@'))
        else:
            self.stdout.write(self.style.WARNING('Estudiante 1 ya existe'))

        estudiante2, created = Usuario.objects.get_or_create(
            username='estudiante2',
            defaults={
                'first_name': 'Ana',
                'last_name': 'López',
                'email': 'ana.lopez@estudiante.troli.edu.co',
                'rol': 'estudiante',
                'activo': True,
            }
        )
        if created:
            estudiante2.set_password('Estudiante123@')
            estudiante2.save()
            self.stdout.write(self.style.SUCCESS('Estudiante 2 creado: estudiante2 / Estudiante123@'))
        else:
            self.stdout.write(self.style.WARNING('Estudiante 2 ya existe'))

        # Crear Cursos
        curso1, created = Curso.objects.get_or_create(
            codigo='MAT101',
            defaults={
                'nombre': 'Matemáticas I',
                'descripcion': 'Introducción al cálculo diferencial e integral',
                'creditos': 4,
                'profesor': profesor,
                'activo': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Curso creado: Matemáticas I (MAT101)'))
        else:
            self.stdout.write(self.style.WARNING('Curso Matemáticas I ya existe'))

        curso2, created = Curso.objects.get_or_create(
            codigo='FIS101',
            defaults={
                'nombre': 'Física I',
                'descripcion': 'Principios fundamentales de la mecánica clásica',
                'creditos': 4,
                'profesor': profesor,
                'activo': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Curso creado: Física I (FIS101)'))
        else:
            self.stdout.write(self.style.WARNING('Curso Física I ya existe'))

        curso3, created = Curso.objects.get_or_create(
            codigo='PROG101',
            defaults={
                'nombre': 'Programación I',
                'descripcion': 'Introducción a la programación con Python',
                'creditos': 3,
                'profesor': profesor,
                'activo': True,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Curso creado: Programación I (PROG101)'))
        else:
            self.stdout.write(self.style.WARNING('Curso Programación I ya existe'))

        # Crear Inscripciones
        insc1, created = Inscripcion.objects.get_or_create(
            estudiante=estudiante1,
            curso=curso1,
            defaults={'activo': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Inscripción creada: Juan en Matemáticas I'))

        inscripcion2, created = Inscripcion.objects.get_or_create(
            estudiante=estudiante1,
            curso=curso2,
            defaults={'estado': 'activo'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Inscripción creada: Juan en Física I'))

        inscripcion3, created = Inscripcion.objects.get_or_create(
            estudiante=estudiante2,
            curso=curso1,
            defaults={'estado': 'activo'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Inscripción creada: Ana en Matemáticas I'))

        # Crear Calificaciones
        calif1, created = Calificacion.objects.get_or_create(
            inscripcion=insc1,
            tipo_evaluacion='parcial',
            defaults={
                'nota': Decimal('4.5'),
                'fecha_evaluacion': timezone.now().date(),
                'observaciones': 'Excelente trabajo en el primer parcial',
                'profesor': profesor,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Calificación creada: Juan - Matemáticas I - Parcial: 4.5'))

        calif2, created = Calificacion.objects.get_or_create(
            inscripcion=insc1,
            tipo_evaluacion='taller',
            defaults={
                'nota': Decimal('4.8'),
                'fecha_evaluacion': timezone.now().date(),
                'observaciones': 'Buen desempeño en el taller de derivadas',
                'profesor': profesor,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Calificación creada: Juan - Matemáticas I - Taller: 4.8'))

        calif3, created = Calificacion.objects.get_or_create(
            inscripcion=insc2,
            tipo_evaluacion='quiz',
            defaults={
                'nota': Decimal('3.8'),
                'fecha_evaluacion': timezone.now().date(),
                'observaciones': 'Buen dominio de cinemática',
                'profesor': profesor,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Calificación creada: Juan - Física I - Quiz: 3.8'))

        calif4, created = Calificacion.objects.get_or_create(
            inscripcion=insc3,
            tipo_evaluacion='parcial',
            defaults={
                'nota': Decimal('4.2'),
                'fecha_evaluacion': timezone.now().date(),
                'observaciones': 'Muy buen trabajo',
                'profesor': profesor,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Calificación creada: Ana - Matemáticas I - Parcial: 4.2'))

        # Crear Notificaciones
        notif1, created = Notificacion.objects.get_or_create(
            usuario=estudiante1,
            tipo='nueva_nota',
            titulo='Nueva calificación registrada',
            defaults={
                'mensaje': 'Se registró una calificación de 4.5 en Matemáticas I.',
                'leida': False,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Notificación creada para Juan'))

        notif2, created = Notificacion.objects.get_or_create(
            usuario=estudiante2,
            tipo='nueva_nota',
            titulo='Nueva calificación registrada',
            defaults={
                'mensaje': 'Se registró una calificación de 4.2 en Matemáticas I.',
                'leida': False,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Notificación creada para Ana'))

        self.stdout.write(self.style.SUCCESS('\nCarga de datos completada exitosamente!'))
        self.stdout.write(self.style.SUCCESS('\nResumen:'))
        self.stdout.write(f'   - Usuarios: {Usuario.objects.count()}')
        self.stdout.write(f'   - Cursos: {Curso.objects.count()}')
        self.stdout.write(f'   - Inscripciones: {Inscripcion.objects.count()}')
        self.stdout.write(f'   - Calificaciones: {Calificacion.objects.count()}')
        self.stdout.write(f'   - Notificaciones: {Notificacion.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nCredenciales de acceso:'))
        self.stdout.write('   Admin:       admin / Admin123@')
        self.stdout.write('   Profesor:    profesor1 / Profesor123@')
        self.stdout.write('   Estudiante1: estudiante1 / Estudiante123@')
        self.stdout.write('   Estudiante2: estudiante2 / Estudiante123@')
        self.stdout.write(self.style.SUCCESS('\nInicia el servidor con: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('   Accede a: http://localhost:8000/'))
