from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Modelo personalizado de Usuario que extiende el usuario de Django
class Usuario(AbstractUser):
    """
    Modelo personalizado de usuario que incluye roles para el sistema
    Permite diferenciar entre estudiantes, profesores y administradores
    """
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('administrador', 'Administrador'),
        ('coordinador', 'Coordinador'),
    ]
    
    rol = models.CharField(max_length=15, choices=ROLES, default='estudiante')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    # Solucionar conflicto con auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='usuario_set',
        related_query_name='usuario',
    )
    
    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"

# Modelo para representar un curso o materia
class Curso(models.Model):
    """
    Representa una materia o curso en el sistema
    Cada curso tiene un nombre, código y profesor asignado
    """
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    creditos = models.IntegerField(default=3)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

# Modelo para la inscripción de estudiantes en cursos
class Inscripcion(models.Model):
    """
    Relaciona estudiantes con cursos
    Permite que un estudiante esté inscrito en múltiples cursos
    """
    estudiante = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'estudiante'})
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.nombre}"
    
    class Meta:
        unique_together = ['estudiante', 'curso']
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

# Modelo para las calificaciones
class Calificacion(models.Model):
    """
    Almacena las notas de los estudiantes
    Incluye validación para notas entre 0.0 y 5.0
    """
    TIPOS_EVALUACION = [
        ('parcial', 'Parcial'),
        ('final', 'Final'),
        ('taller', 'Taller'),
        ('participacion', 'Participación'),
        ('proyecto', 'Proyecto'),
        ('quiz', 'Quiz'),
    ]
    
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    tipo_evaluacion = models.CharField(max_length=15, choices=TIPOS_EVALUACION)
    nota = models.DecimalField(
        max_digits=3, 
        decimal_places=1,
        validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))]
    )
    fecha_evaluacion = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    profesor = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'rol': 'profesor'})
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.inscripcion.estudiante.username} - {self.inscripcion.curso.nombre} - {self.nota}"
    
    class Meta:
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"

# Modelo para el historial de cambios en calificaciones
class HistorialCalificacion(models.Model):
    """
    Registra todos los cambios realizados en las calificaciones
    Permite auditoría y seguimiento de modificaciones
    """
    calificacion = models.ForeignKey(Calificacion, on_delete=models.CASCADE)
    nota_anterior = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    nota_nueva = models.DecimalField(max_digits=3, decimal_places=1)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    motivo = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Cambio en {self.calificacion} por {self.usuario_modificacion.username}"
    
    class Meta:
        verbose_name = "Historial de Calificación"
        verbose_name_plural = "Historiales de Calificaciones"

# Modelo para notificaciones del sistema
class Notificacion(models.Model):
    """
    Sistema básico de notificaciones para usuarios
    Informa sobre nuevas notas, cambios, etc.
    """
    TIPOS_NOTIFICACION = [
        ('nueva_nota', 'Nueva Nota'),
        ('cambio_nota', 'Cambio de Nota'),
        ('recordatorio', 'Recordatorio'),
        ('sistema', 'Sistema'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPOS_NOTIFICACION)
    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
    
    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ['-fecha_creacion']

# Modelo para reportes académicos guardados
class ReporteAcademico(models.Model):
    """
    Almacena configuraciones de reportes guardados que pueden ser reutilizados
    """
    TIPOS_REPORTE = [
        ('notas_estudiante', 'Notas por Estudiante'),
        ('notas_asignatura', 'Notas por Asignatura'),
        ('resumen_general', 'Resumen General'),
        ('estudiantes_riesgo', 'Estudiantes en Riesgo'),
    ]
    
    ESTADOS_ACADEMICOS = [
        ('aprobado', 'Aprobado'),
        ('reprobado', 'Reprobado'),
        ('suspendido', 'Suspendido'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(max_length=500, blank=True, null=True)
    tipo_reporte = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    
    # Filtros del reporte
    semestre = models.CharField(max_length=10, blank=True, null=True)
    grupo = models.CharField(max_length=50, blank=True, null=True)
    asignatura = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_desde = models.DateField(null=True, blank=True)
    fecha_hasta = models.DateField(null=True, blank=True)
    estado_academico = models.CharField(max_length=15, choices=ESTADOS_ACADEMICOS, blank=True, null=True)
    
    # Metadatos
    activo = models.BooleanField(default=True)
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_reporte_display()}"
    
    class Meta:
        verbose_name = "Reporte Académico"
        verbose_name_plural = "Reportes Académicos"
        ordering = ['-fecha_creacion']

# Modelo para el historial de generación de reportes
class HistorialReporte(models.Model):
    """
    Registra cada vez que se genera un reporte
    """
    FORMATOS = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
    ]
    
    reporte = models.ForeignKey(ReporteAcademico, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo_reporte = models.CharField(max_length=20)
    filtros_aplicados = models.TextField()  # JSON con los filtros usados
    formato_exportacion = models.CharField(max_length=10, choices=FORMATOS)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reporte generado por {self.usuario.username} - {self.fecha_generacion}"
    
    class Meta:
        verbose_name = "Historial de Reporte"
        verbose_name_plural = "Historial de Reportes"
        ordering = ['-fecha_generacion']
