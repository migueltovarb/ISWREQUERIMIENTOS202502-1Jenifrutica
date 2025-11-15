from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils import timezone
from .decorators import admin_required
from .models import Usuario, Curso, Inscripcion, Calificacion, HistorialCalificacion, Notificacion
from .forms import UsuarioAdminForm, CursoAdminForm, InscripcionAdminForm

@login_required
@admin_required
def admin_dashboard(request):
    """Dashboard principal del administrador"""
    context = {
        'total_estudiantes': Usuario.objects.filter(rol='estudiante', activo=True).count(),
        'total_profesores': Usuario.objects.filter(rol='profesor', activo=True).count(),
        'total_cursos': Curso.objects.filter(activo=True).count(),
        'total_inscripciones': Inscripcion.objects.filter(activo=True).count(),
        'total_calificaciones': Calificacion.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

# ============= GESTIÓN DE USUARIOS =============

@login_required
@admin_required
def admin_usuarios_lista(request):
    """Lista de todos los usuarios"""
    rol_filter = request.GET.get('rol', '')
    search = request.GET.get('search', '')
    
    usuarios = Usuario.objects.all().order_by('-date_joined')
    
    if rol_filter:
        usuarios = usuarios.filter(rol=rol_filter)
    if search:
        usuarios = usuarios.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    context = {
        'usuarios': usuarios,
        'rol_filter': rol_filter,
        'search': search,
    }
    return render(request, 'admin/usuarios_lista.html', context)

@login_required
@admin_required
def admin_usuario_crear(request):
    """Crear nuevo usuario con validaciones y acciones de guardado"""
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST)
        if form.is_valid():
            usuario = form.save()

            # Registrar auditoría como notificación de sistema
            Notificacion.objects.create(
                usuario=request.user,
                tipo='sistema',
                titulo='Creación de usuario',
                mensaje=f"Se creó el usuario '{usuario.username}' el {timezone.now().strftime('%d/%m/%Y %H:%M')} por {request.user.username}."
            )

            # Enviar correo con credenciales (usuario + contraseña ingresada)
            try:
                tmp_pwd = form.cleaned_data.get('password') or 'Contraseña establecida por el administrador'
                send_mail(
                    subject='Credenciales de acceso - Sistema de Gestión de Notas',
                    message=(
                        f"Hola {usuario.first_name or usuario.username},\n\n"
                        f"Tu cuenta ha sido creada en el Sistema de Gestión de Notas.\n"
                        f"Usuario: {usuario.username}\n"
                        f"Contraseña temporal: {tmp_pwd}\n\n"
                        "Por seguridad, cambia la contraseña en tu primer inicio de sesión."
                    ),
                    from_email=None,  # DEFAULT_FROM_EMAIL
                    recipient_list=[usuario.email],
                    fail_silently=True
                )
                # Notificación al usuario creado
                Notificacion.objects.create(
                    usuario=usuario,
                    tipo='sistema',
                    titulo='Tu cuenta ha sido creada',
                    mensaje='Tu cuenta fue creada por el administrador. Revisa tu correo para credenciales.'
                )
            except Exception:
                # Si el envío falla, continuar pero informar al admin
                messages.warning(request, 'Usuario creado, pero no fue posible enviar el correo de credenciales.')

            messages.success(request, f'Usuario {usuario.username} creado exitosamente.')

            # Acciones: Guardar, Guardar y añadir otro, Guardar y seguir editando
            action = (
                request.POST.get('btn_action') or
                request.POST.get('action') or
                request.POST.get('submit')
            )
            if request.POST.get('save_add_another') or action == 'save_add_another':
                return redirect('admin_usuario_crear')
            if request.POST.get('save_continue') or action == 'save_continue':
                return redirect('admin_usuario_editar', usuario_id=usuario.id)
            return redirect('admin_usuarios_lista')
    else:
        form = UsuarioAdminForm()
    
    return render(request, 'admin/usuario_form.html', {'form': form, 'action': 'Crear'})

@login_required
@admin_required
def admin_usuario_editar(request, usuario_id):
    """Editar usuario existente con soporte de botones de guardado"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente')

            # Auditoría mínima: notificación para el admin responsable
            Notificacion.objects.create(
                usuario=request.user,
                tipo='sistema',
                titulo='Actualización de usuario',
                mensaje=f"Se actualizó el usuario '{usuario.username}' el {timezone.now().strftime('%d/%m/%Y %H:%M')} por {request.user.username}."
            )

            action = (
                request.POST.get('btn_action') or
                request.POST.get('action') or
                request.POST.get('submit')
            )
            if request.POST.get('save_add_another') or action == 'save_add_another':
                return redirect('admin_usuario_crear')
            if request.POST.get('save_continue') or action == 'save_continue':
                return redirect('admin_usuario_editar', usuario_id=usuario.id)
            return redirect('admin_usuarios_lista')
    else:
        form = UsuarioAdminForm(instance=usuario)
    
    return render(request, 'admin/usuario_form.html', {'form': form, 'action': 'Editar', 'usuario': usuario})

@login_required
def admin_usuario_eliminar(request, usuario_id):
    """
    US-019: Eliminar (desactivar) usuario del sistema (SOFT DELETE)
    Solo administradores pueden acceder
    """
    if request.user.rol not in ['administrador', 'coordinador']:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard')
    
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Validación 1: No puede eliminarse a sí mismo
    if usuario.id == request.user.id:
        messages.error(request, 'No puedes eliminar tu propia cuenta')
        return redirect('admin_usuarios_lista')
    
    # Validación 2: Verificar si es el último administrador activo
    if usuario.rol == 'administrador' and usuario.activo:
        admins_activos = Usuario.objects.filter(rol='administrador', activo=True).count()
        if admins_activos <= 1:
            messages.error(request, 'No se puede eliminar el último administrador activo del sistema')
            return redirect('admin_usuarios_lista')
    
    # Obtener estadísticas del usuario
    if usuario.rol == 'estudiante':
        inscripciones_activas = Inscripcion.objects.filter(estudiante=usuario, activo=True).count()
        calificaciones_count = Calificacion.objects.filter(inscripcion__estudiante=usuario).count()
    elif usuario.rol == 'profesor':
        cursos_asignados = Curso.objects.filter(profesor=usuario, activo=True).count()
        calificaciones_registradas = Calificacion.objects.filter(profesor=usuario).count()
    else:
        inscripciones_activas = 0
        calificaciones_count = 0
        cursos_asignados = 0
        calificaciones_registradas = 0
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        
        # Validar motivo
        if not motivo or len(motivo) < 10:
            messages.error(request, 'Debe proporcionar un motivo de al menos 10 caracteres para eliminar el usuario')
            return redirect('admin_usuario_eliminar', usuario_id=usuario_id)
        
        # Si es profesor con cursos activos, advertencia adicional
        if usuario.rol == 'profesor' and cursos_asignados > 0:
            confirmacion = request.POST.get('confirmacion_profesor')
            if confirmacion != 'confirmo':
                messages.warning(request, 'Debe confirmar que desea eliminar al profesor con cursos activos')
                return redirect('admin_usuario_eliminar', usuario_id=usuario_id)
        
        # Realizar la desactivación (soft delete)
        usuario.activo = False
        usuario.save()
        
        # Si es estudiante: desactivar inscripciones
        if usuario.rol == 'estudiante':
            Inscripcion.objects.filter(estudiante=usuario, activo=True).update(activo=False)
        
        # Si es profesor: desasignar cursos
        if usuario.rol == 'profesor':
            Curso.objects.filter(profesor=usuario).update(profesor=None)
        
        # Registrar en historial (si existe un modelo HistorialSistema)
        # HistorialSistema.objects.create(
        #     accion='Eliminación de usuario',
        #     usuario_afectado=usuario,
        #     usuario_ejecutor=request.user,
        #     motivo=motivo
        # )
        
        # Notificación al usuario eliminado (opcional)
        Notificacion.objects.create(
            usuario=usuario,
            tipo='sistema',
            titulo='Cuenta desactivada',
            mensaje=f'Su cuenta ha sido desactivada por un administrador. Motivo: {motivo}'
        )
        
        messages.success(request, f'El usuario {usuario.first_name} {usuario.last_name} ha sido desactivado correctamente')
        return redirect('admin_usuarios_lista')
    
    context = {
        'usuario': usuario,
        'inscripciones_activas': inscripciones_activas if usuario.rol == 'estudiante' else 0,
        'calificaciones_count': calificaciones_count if usuario.rol == 'estudiante' else 0,
        'cursos_asignados': cursos_asignados if usuario.rol == 'profesor' else 0,
        'calificaciones_registradas': calificaciones_registradas if usuario.rol == 'profesor' else 0,
    }
    
    return render(request, 'estudiantes/admin/eliminar_usuario.html', context)

# ============= GESTIÓN DE CURSOS =============

@login_required
@admin_required
def admin_cursos_lista(request):
    """Lista de todos los cursos"""
    search = request.GET.get('search', '')
    
    cursos = Curso.objects.all().select_related('profesor').order_by('codigo')
    
    if search:
        cursos = cursos.filter(
            Q(codigo__icontains=search) |
            Q(nombre__icontains=search) |
            Q(profesor__username__icontains=search)
        )
    
    # Agregar estadísticas a cada curso
    for curso in cursos:
        curso.num_estudiantes = Inscripcion.objects.filter(curso=curso, activo=True).count()
    
    context = {
        'cursos': cursos,
        'search': search,
    }
    return render(request, 'admin/cursos_lista.html', context)

@login_required
@admin_required
def admin_curso_crear(request):
    """Crear nuevo curso"""
    if request.method == 'POST':
        form = CursoAdminForm(request.POST)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f'Curso {curso.nombre} creado exitosamente')
            return redirect('admin_cursos_lista')
    else:
        form = CursoAdminForm()
    
    return render(request, 'admin/curso_form.html', {'form': form, 'action': 'Crear'})

@login_required
@admin_required
def admin_curso_editar(request, curso_id):
    """Editar curso existente"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        form = CursoAdminForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, f'Curso {curso.nombre} actualizado exitosamente')
            return redirect('admin_cursos_lista')
    else:
        form = CursoAdminForm(instance=curso)
    
    return render(request, 'admin/curso_form.html', {'form': form, 'action': 'Editar', 'curso': curso})

@login_required
@admin_required
def admin_curso_eliminar(request, curso_id):
    """Desactivar curso"""
    curso = get_object_or_404(Curso, id=curso_id)
    
    if request.method == 'POST':
        curso.activo = False
        curso.save()
        messages.success(request, f'Curso {curso.nombre} desactivado exitosamente')
        return redirect('admin_cursos_lista')
    
    return render(request, 'admin/curso_confirmar_eliminar.html', {'curso': curso})

# ============= GESTIÓN DE INSCRIPCIONES =============

@login_required
@admin_required
def admin_inscripciones_lista(request):
    """Lista de inscripciones"""
    curso_id = request.GET.get('curso', '')
    estudiante_id = request.GET.get('estudiante', '')
    
    inscripciones = (Inscripcion.objects
        .select_related('estudiante', 'curso')
        .annotate(
            total_calificaciones=Count('calificacion', distinct=True),
            promedio=Avg('calificacion__nota'),
        )
        .order_by('-fecha_inscripcion')
    )
    
    if curso_id:
        inscripciones = inscripciones.filter(curso_id=curso_id)
    if estudiante_id:
        inscripciones = inscripciones.filter(estudiante_id=estudiante_id)
    
    cursos = Curso.objects.filter(activo=True)
    estudiantes = Usuario.objects.filter(rol='estudiante', activo=True)
    
    context = {
        'inscripciones': inscripciones,
        'cursos': cursos,
        'estudiantes': estudiantes,
        'curso_id': curso_id,
        'estudiante_id': estudiante_id,
    }
    return render(request, 'admin/inscripciones_lista.html', context)

@login_required
@admin_required
def admin_inscripcion_crear(request):
    """Crear nueva inscripción"""
    if request.method == 'POST':
        form = InscripcionAdminForm(request.POST)
        if form.is_valid():
            inscripcion = form.save()
            messages.success(request, f'Inscripción creada exitosamente')
            return redirect('admin_inscripciones_lista')
    else:
        form = InscripcionAdminForm()
    
    return render(request, 'admin/inscripcion_form.html', {'form': form, 'action': 'Crear'})

@login_required
@admin_required
def admin_inscripcion_eliminar(request, inscripcion_id):
    """Desactivar inscripción"""
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id)
    
    if request.method == 'POST':
        inscripcion.activo = False
        inscripcion.save()
        messages.success(request, 'Inscripción desactivada exitosamente')
        return redirect('admin_inscripciones_lista')
    
    return render(request, 'admin/inscripcion_confirmar_eliminar.html', {'inscripcion': inscripcion})

# ============= GESTIÓN DE CALIFICACIONES =============

@login_required
@admin_required
def admin_calificaciones_lista(request):
    """Lista de calificaciones"""
    curso_id = request.GET.get('curso', '')
    estudiante_id = request.GET.get('estudiante', '')
    
    calificaciones = Calificacion.objects.all().select_related(
        'inscripcion__estudiante', 
        'inscripcion__curso', 
        'profesor'
    ).order_by('-fecha_evaluacion')
    
    if curso_id:
        calificaciones = calificaciones.filter(inscripcion__curso_id=curso_id)
    if estudiante_id:
        calificaciones = calificaciones.filter(inscripcion__estudiante_id=estudiante_id)
    
    cursos = Curso.objects.filter(activo=True)
    estudiantes = Usuario.objects.filter(rol='estudiante', activo=True)
    
    context = {
        'calificaciones': calificaciones,
        'cursos': cursos,
        'estudiantes': estudiantes,
        'curso_id': curso_id,
        'estudiante_id': estudiante_id,
    }
    return render(request, 'admin/calificaciones_lista.html', context)

@login_required
@admin_required
def admin_historial_lista(request):
    """Lista del historial de cambios en calificaciones"""
    historial = HistorialCalificacion.objects.all().select_related(
        'calificacion__inscripcion__estudiante',
        'calificacion__inscripcion__curso',
        'usuario_modificacion'
    ).order_by('-fecha_cambio')
    
    context = {
        'historial': historial,
    }
    return render(request, 'admin/historial_lista.html', context)

# ============= REPORTES Y ESTADÍSTICAS =============

@login_required
@admin_required
def admin_reportes(request):
    """Reportes y estadísticas"""
    # Estadísticas por curso
    cursos_stats = Curso.objects.filter(activo=True).annotate(
        num_estudiantes=Count('inscripcion', filter=Q(inscripcion__activo=True)),
        promedio=Avg('inscripcion__calificacion__nota')
    ).order_by('-num_estudiantes')
    
    # Estudiantes con mejor rendimiento
    estudiantes_top = Usuario.objects.filter(
        rol='estudiante', 
        activo=True
    ).annotate(
        promedio=Avg('inscripcion__calificacion__nota')
    ).order_by('-promedio')[:10]
    
    # Estadísticas generales
    total_calificaciones = Calificacion.objects.count()
    promedio_general = Calificacion.objects.aggregate(Avg('nota'))['nota__avg']
    
    context = {
        'cursos_stats': cursos_stats,
        'estudiantes_top': estudiantes_top,
        'total_calificaciones': total_calificaciones,
        'promedio_general': promedio_general,
    }
    return render(request, 'admin/reportes.html', context)

# ============= GENERACIÓN DE REPORTES ACADÉMICOS =============

from django.http import HttpResponse, JsonResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfgen import canvas
import json
from datetime import datetime
from .models import ReporteAcademico, HistorialReporte
from .forms import ReporteAcademicoForm

@login_required
@admin_required
def admin_generar_reporte(request):
    """Página para generar nuevo reporte con filtros avanzados"""
    # Obtener datos para los filtros
    semestres = ['2024-1', '2024-2', '2025-1', '2025-2']  # Esto podría venir de la BD
    grupos = ['Grupo A', 'Grupo B', 'Grupo C', 'Grupo D']  # Ejemplo de grupos
    asignaturas = Curso.objects.filter(activo=True).order_by('nombre')
    
    # Obtener reportes guardados del usuario actual
    reportes_guardados = ReporteAcademico.objects.filter(
        usuario_creador=request.user
    ).select_related('asignatura').order_by('-fecha_creacion')
    
    # Obtener historial de reportes generados
    historial = HistorialReporte.objects.all().select_related('usuario').order_by('-fecha_generacion')[:10]
    
    # Variables para la vista previa
    datos_reporte = None
    filtros_aplicados = {}
    
    # Si se solicita generar vista previa
    if request.method == 'GET' and request.GET.get('preview'):
        # Validar campos obligatorios
        semestre = request.GET.get('semestre', '').strip()
        tipo_reporte = request.GET.get('tipo_reporte', '').strip()
        
        if not semestre or not tipo_reporte:
            messages.error(request, 'Por favor, complete los campos obligatorios: Semestre y Tipo de Reporte')
        else:
            # Obtener filtros opcionales
            grupo = request.GET.get('grupo', '').strip()
            asignatura_id = request.GET.get('asignatura', '').strip()
            fecha_desde = request.GET.get('fecha_desde', '').strip()
            fecha_hasta = request.GET.get('fecha_hasta', '').strip()
            estado_academico = request.GET.get('estado_academico', '').strip()
            
            # Construir filtros
            filtros_aplicados = {
                'semestre': semestre,
                'tipo_reporte': tipo_reporte,
                'grupo': grupo,
                'asignatura_id': asignatura_id,
                'fecha_desde': fecha_desde,
                'fecha_hasta': fecha_hasta,
                'estado_academico': estado_academico,
            }
            
            # Generar datos según tipo de reporte
            datos_reporte = _generar_datos_reporte(tipo_reporte, filtros_aplicados)
    
    context = {
        'semestres': semestres,
        'grupos': grupos,
        'asignaturas': asignaturas,
        'reportes_guardados': reportes_guardados,
        'historial': historial,
        'datos_reporte': datos_reporte,
        'filtros_aplicados': filtros_aplicados,
    }
    
    return render(request, 'admin/generar_reporte.html', context)

def _generar_datos_reporte(tipo_reporte, filtros):
    """Función auxiliar para generar los datos del reporte según tipo y filtros"""
    # Construir query base de calificaciones
    query = Calificacion.objects.select_related(
        'inscripcion__estudiante',
        'inscripcion__curso',
        'profesor'
    )
    
    # Aplicar filtros opcionales
    if filtros.get('asignatura_id'):
        query = query.filter(inscripcion__curso_id=filtros['asignatura_id'])
    
    if filtros.get('fecha_desde'):
        query = query.filter(fecha_evaluacion__gte=filtros['fecha_desde'])
    
    if filtros.get('fecha_hasta'):
        query = query.filter(fecha_evaluacion__lte=filtros['fecha_hasta'])
    
    # Generar datos según tipo de reporte
    if tipo_reporte == 'notas_estudiante':
        # Agrupar por estudiante
        datos = []
        estudiantes = Usuario.objects.filter(rol='estudiante', activo=True)
        
        for estudiante in estudiantes:
            calificaciones = query.filter(inscripcion__estudiante=estudiante)
            if calificaciones.exists():
                promedio = calificaciones.aggregate(Avg('nota'))['nota__avg']
                datos.append({
                    'matricula': estudiante.username,
                    'nombre': estudiante.get_full_name(),
                    'total_notas': calificaciones.count(),
                    'promedio': round(promedio, 2) if promedio else 0,
                    'estado': 'Aprobado' if promedio and promedio >= 3.0 else 'Reprobado'
                })
        
        return datos
    
    elif tipo_reporte == 'notas_asignatura':
        # Agrupar por asignatura
        datos = []
        cursos = Curso.objects.filter(activo=True)
        
        for curso in cursos:
            calificaciones = query.filter(inscripcion__curso=curso)
            if calificaciones.exists():
                promedio = calificaciones.aggregate(Avg('nota'))['nota__avg']
                datos.append({
                    'codigo': curso.codigo,
                    'nombre': curso.nombre,
                    'profesor': curso.profesor.get_full_name(),
                    'estudiantes': calificaciones.values('inscripcion__estudiante').distinct().count(),
                    'promedio': round(promedio, 2) if promedio else 0
                })
        
        return datos
    
    elif tipo_reporte == 'resumen_general':
        # Resumen general del sistema
        total_estudiantes = Usuario.objects.filter(rol='estudiante', activo=True).count()
        total_cursos = Curso.objects.filter(activo=True).count()
        total_calificaciones = query.count()
        promedio_general = query.aggregate(Avg('nota'))['nota__avg']
        
        return [{
            'total_estudiantes': total_estudiantes,
            'total_cursos': total_cursos,
            'total_calificaciones': total_calificaciones,
            'promedio_general': round(promedio_general, 2) if promedio_general else 0
        }]
    
    elif tipo_reporte == 'estudiantes_riesgo':
        # Estudiantes con promedio < 3.0
        datos = []
        estudiantes = Usuario.objects.filter(rol='estudiante', activo=True)
        
        for estudiante in estudiantes:
            calificaciones = query.filter(inscripcion__estudiante=estudiante)
            if calificaciones.exists():
                promedio = calificaciones.aggregate(Avg('nota'))['nota__avg']
                if promedio and promedio < 3.0:
                    datos.append({
                        'matricula': estudiante.username,
                        'nombre': estudiante.get_full_name(),
                        'promedio': round(promedio, 2),
                        'cursos_reprobados': calificaciones.filter(nota__lt=3.0).count(),
                        'estado': 'En Riesgo'
                    })
        
        return datos
    
    return []

@login_required
@admin_required
def admin_exportar_reporte_pdf(request):
    """Exportar reporte a PDF"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    # Obtener filtros del request
    semestre = request.POST.get('semestre', '').strip()
    tipo_reporte = request.POST.get('tipo_reporte', '').strip()
    
    # Validar campos obligatorios
    if not semestre or not tipo_reporte:
        return JsonResponse({'error': 'Campos obligatorios faltantes'}, status=400)
    
    # Construir filtros
    filtros = {
        'semestre': semestre,
        'tipo_reporte': tipo_reporte,
        'grupo': request.POST.get('grupo', ''),
        'asignatura_id': request.POST.get('asignatura', ''),
        'fecha_desde': request.POST.get('fecha_desde', ''),
        'fecha_hasta': request.POST.get('fecha_hasta', ''),
        'estado_academico': request.POST.get('estado_academico', ''),
    }
    
    # Generar datos
    datos = _generar_datos_reporte(tipo_reporte, filtros)
    
    if not datos:
        return JsonResponse({'error': 'No hay datos para exportar'}, status=400)
    
    # Obtener nombre personalizado si existe
    nombre_pdf = request.POST.get('nombre_pdf', '').strip()
    if nombre_pdf:
        # Limpiar nombre para usar como filename (solo alfanuméricos, espacios, guiones)
        import re
        nombre_archivo = re.sub(r'[^\w\s\-]', '', nombre_pdf)
        nombre_archivo = nombre_archivo.replace(' ', '_')
    else:
        nombre_archivo = f"reporte_{tipo_reporte}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Registrar en historial
    HistorialReporte.objects.create(
        usuario=request.user,
        tipo_reporte=tipo_reporte,
        filtros_aplicados=json.dumps(filtros),
        formato_exportacion='pdf'
    )
    
    # Crear PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}.pdf"'
    
    # Generar PDF con ReportLab
    doc = SimpleDocTemplate(response, pagesize=letter)
    elementos = []
    styles = getSampleStyleSheet()
    
    # Título
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1B3C53'),
        spaceAfter=30,
        alignment=1  # Centrado
    )
    
    # Usar nombre personalizado si existe, sino usar el nombre por defecto
    if nombre_pdf:
        titulo_reporte = nombre_pdf
    else:
        tipo_nombre = dict([
            ('notas_estudiante', 'Notas por Estudiante'),
            ('notas_asignatura', 'Notas por Asignatura'),
            ('resumen_general', 'Resumen General'),
            ('estudiantes_riesgo', 'Estudiantes en Riesgo'),
        ]).get(tipo_reporte, 'Reporte Académico')
        titulo_reporte = f"Reporte Académico: {tipo_nombre}"
    
    elementos.append(Paragraph(titulo_reporte, titulo_style))
    elementos.append(Paragraph(f"Semestre: {semestre}", styles['Normal']))
    elementos.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Construir tabla según tipo de reporte
    if tipo_reporte == 'notas_estudiante':
        data = [['Matrícula', 'Nombre', 'Total Notas', 'Promedio', 'Estado']]
        for item in datos:
            data.append([
                item['matricula'],
                item['nombre'],
                str(item['total_notas']),
                str(item['promedio']),
                item['estado']
            ])
    
    elif tipo_reporte == 'notas_asignatura':
        data = [['Código', 'Asignatura', 'Profesor', 'Estudiantes', 'Promedio']]
        for item in datos:
            data.append([
                item['codigo'],
                item['nombre'],
                item['profesor'],
                str(item['estudiantes']),
                str(item['promedio'])
            ])
    
    elif tipo_reporte == 'resumen_general':
        data = [['Indicador', 'Valor']]
        item = datos[0]
        data.append(['Total Estudiantes', str(item['total_estudiantes'])])
        data.append(['Total Cursos', str(item['total_cursos'])])
        data.append(['Total Calificaciones', str(item['total_calificaciones'])])
        data.append(['Promedio General', str(item['promedio_general'])])
    
    elif tipo_reporte == 'estudiantes_riesgo':
        data = [['Matrícula', 'Nombre', 'Promedio', 'Cursos Reprobados', 'Estado']]
        for item in datos:
            data.append([
                item['matricula'],
                item['nombre'],
                str(item['promedio']),
                str(item['cursos_reprobados']),
                item['estado']
            ])
    
    # Crear tabla
    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B3C53')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elementos.append(tabla)
    elementos.append(Spacer(1, 0.3*inch))
    elementos.append(Paragraph("Sistema de Gestión de Notas - TROLI", styles['Normal']))
    
    doc.build(elementos)
    
    return response

@login_required
@admin_required
def admin_guardar_reporte(request):
    """Guardar configuración de reporte para reutilización"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    # Validar campos obligatorios de filtros
    semestre = request.POST.get('semestre', '').strip()
    tipo_reporte = request.POST.get('tipo_reporte', '').strip()
    
    if not semestre or not tipo_reporte:
        return JsonResponse({
            'error': 'Por favor, complete todos los campos obligatorios'
        }, status=400)
    
    # Crear formulario con datos del modal
    form_data = {
        'nombre': request.POST.get('nombre_reporte', '').strip(),
        'descripcion': request.POST.get('descripcion', '').strip(),
        'activo': request.POST.get('estado_reporte', 'True') == 'True',
    }
    
    form = ReporteAcademicoForm(form_data)
    
    if not form.is_valid():
        return JsonResponse({
            'error': 'Datos inválidos',
            'errores': form.errors
        }, status=400)
    
    # Guardar reporte
    reporte = form.save(commit=False)
    reporte.tipo_reporte = tipo_reporte
    reporte.semestre = semestre
    reporte.grupo = request.POST.get('grupo', '').strip()
    
    asignatura_id = request.POST.get('asignatura', '').strip()
    if asignatura_id:
        reporte.asignatura_id = asignatura_id
    
    fecha_desde = request.POST.get('fecha_desde', '').strip()
    if fecha_desde:
        reporte.fecha_desde = fecha_desde
    
    fecha_hasta = request.POST.get('fecha_hasta', '').strip()
    if fecha_hasta:
        reporte.fecha_hasta = fecha_hasta
    
    reporte.estado_academico = request.POST.get('estado_academico', '').strip()
    reporte.usuario_creador = request.user
    reporte.save()
    
    return JsonResponse({
        'success': True,
        'mensaje': f'Reporte "{reporte.nombre}" guardado exitosamente',
        'reporte_id': reporte.id
    })

@login_required
@admin_required
def admin_cargar_reporte_guardado(request, reporte_id):
    """Cargar configuración de un reporte guardado"""
    reporte = get_object_or_404(ReporteAcademico, id=reporte_id)
    
    datos = {
        'nombre': reporte.nombre,
        'descripcion': reporte.descripcion,
        'tipo_reporte': reporte.tipo_reporte,
        'semestre': reporte.semestre,
        'grupo': reporte.grupo or '',
        'asignatura_id': reporte.asignatura_id or '',
        'fecha_desde': reporte.fecha_desde.strftime('%Y-%m-%d') if reporte.fecha_desde else '',
        'fecha_hasta': reporte.fecha_hasta.strftime('%Y-%m-%d') if reporte.fecha_hasta else '',
        'estado_academico': reporte.estado_academico or '',
    }
    
    return JsonResponse(datos)

@login_required
@admin_required
def admin_editar_reporte(request, reporte_id):
    """Editar un reporte guardado"""
    reporte = get_object_or_404(ReporteAcademico, id=reporte_id, usuario_creador=request.user)
    
    # Obtener datos para los selectores
    semestres = ['2024-1', '2024-2', '2025-1', '2025-2']
    grupos = ['Grupo A', 'Grupo B', 'Grupo C', 'Grupo D']
    asignaturas = Curso.objects.filter(activo=True).order_by('nombre')
    
    if request.method == 'POST':
        form = ReporteAcademicoForm(request.POST, instance=reporte)
        if form.is_valid():
            reporte_actualizado = form.save(commit=False)
            
            # Actualizar campos adicionales
            reporte_actualizado.semestre = request.POST.get('semestre')
            reporte_actualizado.grupo = request.POST.get('grupo', '').strip()
            asignatura_id = request.POST.get('asignatura')
            if asignatura_id:
                reporte_actualizado.asignatura_id = asignatura_id
            else:
                reporte_actualizado.asignatura = None
            
            fecha_desde = request.POST.get('fecha_desde', '').strip()
            if fecha_desde:
                reporte_actualizado.fecha_desde = fecha_desde
            else:
                reporte_actualizado.fecha_desde = None
            
            fecha_hasta = request.POST.get('fecha_hasta', '').strip()
            if fecha_hasta:
                reporte_actualizado.fecha_hasta = fecha_hasta
            else:
                reporte_actualizado.fecha_hasta = None
            
            reporte_actualizado.estado_academico = request.POST.get('estado_academico', '').strip()
            reporte_actualizado.save()
            
            messages.success(request, 'El reporte ha sido actualizado correctamente')
            return redirect('admin_generar_reporte')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario')
    else:
        form = ReporteAcademicoForm(instance=reporte)
    
    context = {
        'form': form,
        'reporte': reporte,
        'semestres': semestres,
        'grupos': grupos,
        'asignaturas': asignaturas,
        'editar': True,
    }
    
    return render(request, 'admin/reporte_form.html', context)

@login_required
@admin_required
def admin_eliminar_reporte(request, reporte_id):
    """Eliminar un reporte guardado"""
    reporte = get_object_or_404(ReporteAcademico, id=reporte_id)
    
    # Verificar que el usuario actual sea el creador
    if reporte.usuario_creador != request.user:
        messages.error(request, 'No tienes permisos para eliminar este reporte.')
        return redirect('admin_generar_reporte')
    
    if request.method == 'POST':
        nombre_reporte = reporte.nombre
        reporte.delete()
        messages.success(request, f'El reporte "{nombre_reporte}" ha sido eliminado correctamente')
        return redirect('admin_generar_reporte')
    
    context = {
        'reporte': reporte,
    }
    
    return render(request, 'admin/reporte_confirmar_eliminar.html', context)
