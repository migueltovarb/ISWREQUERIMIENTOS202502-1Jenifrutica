from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .models import Usuario, Curso, Inscripcion, Calificacion, Notificacion, HistorialCalificacion
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from types import SimpleNamespace
from django.urls import reverse

# Home: redirige por rol o a login
def home(request):
	# Redirige por rol si está autenticado, si no al login
	if request.user.is_authenticated:
		if getattr(request.user, "rol", None) == "administrador":
			return redirect("admin_dashboard")
		return redirect("dashboard")
	return redirect("login")

# Login básico (placeholder)
def login_view(request):
	# Placeholder simple para permitir el arranque
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			if getattr(user, "rol", None) == "administrador":
				return redirect("admin_dashboard")
			return redirect("dashboard")
		messages.error(request, "Credenciales inválidas")
		return redirect("login")
	return HttpResponse("Página de login (placeholder). Envíe POST con username y password.")

# Logout
def logout_view(request):
	logout(request)
	return redirect("login")

# Registro básico (placeholder)
def registro(request):
	# Placeholder simple para permitir que el servidor arranque
	if request.method == "POST":
		username = request.POST.get("username")
		email = request.POST.get("email", "")
		password = request.POST.get("password")
		if not username or not password:
			messages.error(request, "Usuario y contraseña son obligatorios")
			return redirect("registro")
		from .models import Usuario
		if Usuario.objects.filter(username=username).exists():
			messages.error(request, "El usuario ya existe")
			return redirect("registro")
		u = Usuario(username=username, email=email, rol="estudiante", activo=True)
		u.set_password(password)
		u.save()
		messages.success(request, "Registro exitoso. Inicia sesión.")
		return redirect("login")
	return HttpResponse("Página de registro (placeholder). Envíe POST con username y password.")

# Dashboard para no admin - CORREGIDO
@login_required
def dashboard(request):
    """
    Redirige al dashboard correspondiente según el rol del usuario
    """
    if request.user.rol == 'administrador':
        return redirect('admin_dashboard')
    elif request.user.rol == 'profesor':
        return redirect('dashboard_profesor')
    elif request.user.rol == 'estudiante':
        return redirect('dashboard_estudiante')
    else:
        # Si el rol no está definido, redirigir al login
        messages.warning(request, 'No tienes un rol asignado. Contacta al administrador.')
        return redirect('login')

# Estudiante: ver calificaciones (placeholder)
@login_required
def ver_calificaciones(request):
	return HttpResponse("Ver calificaciones (placeholder).")

# Estudiante: inscribirse a curso (placeholder)
@login_required
def inscribirse_curso(request):
	return HttpResponse("Inscribirse a curso (placeholder).")

# Estudiante: mis cursos (placeholder)
@login_required
def mis_cursos(request):
    """Vista para que el estudiante vea sus cursos inscritos"""
    if request.user.rol != 'estudiante':
        messages.error(request, 'No tienes permisos para acceder')
        return redirect('dashboard')
    
    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user,
        activo=True
    ).select_related('curso', 'curso__profesor')
    
    # Agregar estadísticas a cada curso
    for insc in inscripciones:
        calificaciones = Calificacion.objects.filter(inscripcion=insc)
        insc.total_calificaciones = calificaciones.count()
        insc.promedio = calificaciones.aggregate(Avg('nota'))['nota__avg']
    
    context = {
        'inscripciones': inscripciones,
    }
    return render(request, 'estudiantes/mis_cursos.html', context)

@login_required
def inscribirse_curso(request):
    """Vista para que el estudiante se inscriba a un curso"""
    if request.user.rol != 'estudiante':
        messages.error(request, 'No tienes permisos para acceder')
        return redirect('dashboard')
    
    if request.method == 'POST':
        curso_id = request.POST.get('curso_id')
        curso = get_object_or_404(Curso, id=curso_id, activo=True)
        
        # Verificar si ya está inscrito
        if Inscripcion.objects.filter(estudiante=request.user, curso=curso).exists():
            messages.warning(request, 'Ya estás inscrito en este curso')
        else:
            Inscripcion.objects.create(
                estudiante=request.user,
                curso=curso,
                activo=True
            )
            messages.success(request, f'Te has inscrito exitosamente en {curso.nombre}')
        
        return redirect('mis_cursos')
    
    # Cursos disponibles (no inscritos)
    cursos_inscritos = Inscripcion.objects.filter(
        estudiante=request.user
    ).values_list('curso_id', flat=True)
    
    cursos_disponibles = Curso.objects.filter(
        activo=True
    ).exclude(id__in=cursos_inscritos)
    
    context = {
        'cursos_disponibles': cursos_disponibles,
    }
    return render(request, 'estudiantes/inscribirse_curso.html', context)

# Profesor: cursos asignados (placeholder)
@login_required
def profesor_cursos(request):
	return HttpResponse("Cursos del profesor (placeholder).")

# Profesor: ver estudiantes de un curso (placeholder)
@login_required
def estudiantes_curso(request, curso_id):
	return HttpResponse(f"Estudiantes del curso {curso_id} (placeholder).")

# Profesor: calificar estudiante (placeholder)
@login_required
def calificar_estudiante(request, inscripcion_id):
	return HttpResponse(f"Calificar inscripción {inscripcion_id} (placeholder).")

# Profesor: editar calificación (placeholder)
@login_required
def editar_calificacion(request, calificacion_id):
	return HttpResponse(f"Editar calificación {calificacion_id} (placeholder).")

# Vista principal de inicio de sesión
def login_view(request):
    """
    Vista para el inicio de sesión de usuarios
    Redirige según el rol del usuario autenticado
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.activo:
            login(request, user)
            messages.success(request, f'Bienvenido {user.first_name or user.username}')
            
            # Redirigir según el rol del usuario
            if user.rol == 'estudiante':
                return redirect('dashboard_estudiante')
            elif user.rol == 'profesor':
                return redirect('dashboard_profesor')
            elif user.rol in ['administrador', 'coordinador']:
                return redirect('admin_dashboard')  # CORREGIDO: era 'dashboard_admin'
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'estudiantes/login.html')

# Vista para cerrar sesión
def logout_view(request):
    """
    Cierra la sesión del usuario actual
    """
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login')

# Dashboard para estudiantes
@login_required
def dashboard_estudiante(request):
    """
    Panel principal para estudiantes
    Muestra sus cursos, notas y notificaciones
    """
    if request.user.rol != 'estudiante':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('login')
    
    # Obtener inscripciones activas del estudiante
    inscripciones = Inscripcion.objects.filter(
        estudiante=request.user, 
        activo=True
    ).select_related('curso')
    
    # Obtener calificaciones del estudiante
    calificaciones = Calificacion.objects.filter(
        inscripcion__estudiante=request.user
    ).select_related('inscripcion__curso').order_by('-fecha_registro')
    
    # Calcular promedio general
    promedio_general = calificaciones.aggregate(Avg('nota'))['nota__avg']
    if promedio_general:
        promedio_general = round(promedio_general, 1)
    
    # Obtener notificaciones no leídas
    notificaciones = Notificacion.objects.filter(
        usuario=request.user, 
        leida=False
    ).order_by('-fecha_creacion')[:5]
    
    context = {
        'inscripciones': inscripciones,
        'calificaciones': calificaciones[:10],  # Últimas 10 calificaciones
        'promedio_general': promedio_general,
        'notificaciones': notificaciones,
    }
    
    return render(request, 'estudiantes/dashboard_estudiante.html', context)

# Dashboard para profesores
@login_required
def dashboard_profesor(request):
    """
    Panel principal para profesores
    Muestra sus cursos asignados y opciones de gestión
    """
    if request.user.rol != 'profesor':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('login')
    
    # Obtener cursos asignados al profesor con conteos
    cursos = Curso.objects.filter(profesor=request.user, activo=True)
    
    # Añadir conteos a cada curso
    for curso in cursos:
        curso.estudiantes_count = Inscripcion.objects.filter(
            curso=curso, activo=True
        ).count()
        curso.calificaciones_count = Calificacion.objects.filter(
            inscripcion__curso=curso
        ).count()
    
    # Estadísticas básicas
    total_estudiantes = Inscripcion.objects.filter(
        curso__profesor=request.user, 
        activo=True
    ).count()
    
    total_calificaciones = Calificacion.objects.filter(
        profesor=request.user
    ).count()
    
    # Últimas calificaciones registradas
    ultimas_calificaciones = Calificacion.objects.filter(
        profesor=request.user
    ).select_related(
        'inscripcion__estudiante', 'inscripcion__curso'
    ).order_by('-fecha_registro')[:10]
    
    # Notificaciones
    notificaciones_recientes = Notificacion.objects.filter(
        usuario=request.user, 
        leida=False
    ).order_by('-fecha_creacion')[:5]
    
    context = {
        'cursos': cursos,
        'total_estudiantes': total_estudiantes,
        'total_cursos': cursos.count(),
        'calificaciones_registradas': total_calificaciones,
        'notificaciones_no_leidas': notificaciones_recientes.count(),
        'ultimas_calificaciones': ultimas_calificaciones,
        'notificaciones_recientes': notificaciones_recientes,
    }
    
    return render(request, 'estudiantes/dashboard_profesor.html', context)

# Dashboard para administradores
@login_required
def dashboard_admin(request):
    """
    Panel principal para administradores
    Muestra estadísticas generales del sistema
    """
    if request.user.rol not in ['administrador', 'coordinador']:
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('login')
    
    # Estadísticas generales
    total_usuarios = Usuario.objects.filter(activo=True).count()
    total_estudiantes = Usuario.objects.filter(rol='estudiante', activo=True).count()
    total_profesores = Usuario.objects.filter(rol='profesor', activo=True).count()
    total_cursos = Curso.objects.filter(activo=True).count()
    total_calificaciones = Calificacion.objects.count()
    
    # Usuarios por rol
    usuarios_por_rol = Usuario.objects.filter(activo=True).values('rol').annotate(
        cantidad=Count('id')
    )
    
    context = {
        'total_usuarios': total_usuarios,
        'total_estudiantes': total_estudiantes,
        'total_profesores': total_profesores,
        'total_cursos': total_cursos,
        'total_calificaciones': total_calificaciones,
        'usuarios_por_rol': usuarios_por_rol,
    }
    
    return render(request, 'estudiantes/dashboard_admin.html', context)

# Vista para registrar calificaciones (profesores)
@login_required
def registrar_calificacion(request, curso_id):
    if request.user.rol != 'profesor':
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('login')

    cursos = Curso.objects.filter(profesor=request.user, activo=True)
    curso_actual = get_object_or_404(Curso, id=curso_id, profesor=request.user)
    inscripciones = Inscripcion.objects.filter(curso=curso_actual, activo=True).select_related('estudiante')

    # Prellenado si viene ?editar=<id>
    editar_id = request.GET.get('editar')
    editar_obj = None
    selected_estudiante_id = None
    form_data = SimpleNamespace(curso=str(curso_actual.id), estudiante='', tipo_evaluacion='', nota='', observaciones='')

    if editar_id:
        editar_obj = get_object_or_404(
            Calificacion,
            id=editar_id,
            inscripcion__curso=curso_actual,
            profesor=request.user
        )
        selected_estudiante_id = editar_obj.inscripcion.estudiante_id
        form_data = SimpleNamespace(
            curso=str(curso_actual.id),
            estudiante=str(selected_estudiante_id),
            tipo_evaluacion=editar_obj.tipo_evaluacion,
            nota=str(editar_obj.nota),
            observaciones=editar_obj.observaciones or ''
        )

    if request.method == 'POST':
        # Leer datos del formulario
        curso_post = request.POST.get('curso') or str(curso_actual.id)
        estudiante_post = request.POST.get('estudiante')
        tipo_post = request.POST.get('tipo_evaluacion')
        nota_post = request.POST.get('nota')
        observ_post = request.POST.get('observaciones', '').strip()
        calificacion_id_post = request.POST.get('calificacion_id')

        # Devolver data al template si hay error
        form_data = SimpleNamespace(
            curso=curso_post or '',
            estudiante=estudiante_post or '',
            tipo_evaluacion=tipo_post or '',
            nota=nota_post or '',
            observaciones=observ_post or ''
        )
        selected_estudiante_id = estudiante_post

        # Validaciones mínimas
        if not (curso_post and estudiante_post and tipo_post and nota_post):
            messages.error(request, 'Todos los campos son obligatorios.')
        else:
            try:
                nota_decimal = Decimal(nota_post)
            except (InvalidOperation, TypeError):
                messages.error(request, 'La calificación debe ser un número válido con máximo un decimal.')
                nota_decimal = None

            if nota_decimal is not None and (nota_decimal < Decimal('0.0') or nota_decimal > Decimal('5.0')):
                messages.error(request, 'La calificación debe estar entre 0.0 y 5.0.')

        # Verificar inscripción
        if not messages.get_messages(request):
            insc = Inscripcion.objects.filter(
                curso_id=curso_actual.id,  # Forzamos en el curso actual
                estudiante_id=estudiante_post,
                activo=True
            ).first()
            if not insc:
                messages.error(request, 'El estudiante no está inscrito en este curso.')

        # Crear/actualizar
        if not messages.get_messages(request):
            if calificacion_id_post:
                # Edición
                calif = get_object_or_404(
                    Calificacion,
                    id=calificacion_id_post,
                    inscripcion__curso=curso_actual,
                    profesor=request.user
                )
                nota_anterior = calif.nota
                calif.tipo_evaluacion = tipo_post
                calif.nota = nota_decimal
                calif.observaciones = observ_post
                calif.fecha_evaluacion = calif.fecha_evaluacion or timezone.now().date()
                calif.profesor = request.user
                calif.save()

                # Historial
                HistorialCalificacion.objects.create(
                    calificacion=calif,
                    nota_anterior=nota_anterior,
                    nota_nueva=nota_decimal,
                    usuario_modificacion=request.user,
                    motivo='Actualización de calificación'
                )

                # Notificación al estudiante
                Notificacion.objects.create(
                    usuario=calif.inscripcion.estudiante,
                    tipo='cambio_nota',
                    titulo='Calificación modificada',
                    mensaje=f'Se actualizó tu calificación en {calif.inscripcion.curso.nombre} a {nota_decimal}.'
                )

                messages.success(request, 'Calificación actualizada correctamente.')
                return redirect('registrar_calificacion', curso_id=curso_actual.id)
            else:
                # Creación
                calif = Calificacion.objects.create(
                    inscripcion=insc,
                    tipo_evaluacion=tipo_post,
                    nota=nota_decimal,
                    fecha_evaluacion=timezone.now().date(),
                    observaciones=observ_post,
                    profesor=request.user
                )

                # Notificación al estudiante
                Notificacion.objects.create(
                    usuario=insc.estudiante,
                    tipo='nueva_nota',
                    titulo='Nueva calificación registrada',
                    mensaje=f'Se registró una calificación de {nota_decimal} en {insc.curso.nombre}.'
                )

                messages.success(request, 'Calificación registrada correctamente.')
                return redirect('registrar_calificacion', curso_id=curso_actual.id)

    # Últimas del profesor
    calificaciones_recientes = Calificacion.objects.filter(
        profesor=request.user
    ).select_related('inscripcion__estudiante', 'inscripcion__curso').order_by('-fecha_registro')[:10]

    context = {
        'curso': curso_actual,
        'cursos': cursos,
        'inscripciones': inscripciones,
        'tipos_evaluacion': Calificacion.TIPOS_EVALUACION,
        'calificaciones_recientes': calificaciones_recientes,
        'form_data': form_data,
        'selected_estudiante_id': selected_estudiante_id,
        'editar_obj': editar_obj,
        'selected_curso_id': curso_actual.id,
    }
    return render(request, 'estudiantes/registrar_calificacion.html', context)

# US-009: Editar calificación - MEJORAR
@login_required
def editar_calificacion(request, calificacion_id):
    """Redirige al formulario de registrar con el calificación a editar"""
    calif = get_object_or_404(Calificacion, id=calificacion_id, profesor=request.user)
    return redirect(f"{reverse('registrar_calificacion', kwargs={'curso_id': calif.inscripcion.curso.id})}?editar={calif.id}")

# US-010: NUEVA - Eliminar calificación
@login_required
def eliminar_calificacion(request, calificacion_id):
    """Eliminar una calificación con motivo y registro en historial"""
    if request.user.rol not in ['profesor', 'administrador']:
        messages.error(request, 'No tienes permisos para realizar esta acción')
        return redirect('dashboard')
    
    calif = get_object_or_404(Calificacion, id=calificacion_id)
    
    # Verificar permisos: solo el profesor que la creó o un admin
    if request.user.rol == 'profesor' and calif.profesor != request.user:
        messages.error(request, 'Solo puedes eliminar calificaciones que tú registraste')
        return redirect('dashboard_profesor')
    
    if request.method == 'POST':
        motivo = request.POST.get('motivo', '').strip()
        
        if not motivo:
            messages.error(request, 'Debe proporcionar un motivo para eliminar la calificación')
            return redirect('eliminar_calificacion', calificacion_id=calificacion_id)
        
        # Guardar en historial antes de eliminar
        HistorialCalificacion.objects.create(
            calificacion=calif,
            nota_anterior=calif.nota,
            nota_nueva=None,  # Indica eliminación
            usuario_modificacion=request.user,
            motivo=f"ELIMINACIÓN: {motivo}"
        )
        
        # Notificar al estudiante
        Notificacion.objects.create(
            usuario=calif.inscripcion.estudiante,
            tipo='sistema',
            titulo='Calificación eliminada',
            mensaje=f'Se eliminó una calificación en {calif.inscripcion.curso.nombre}. Motivo: {motivo}'
        )
        
        # Datos para redirección
        curso_id = calif.inscripcion.curso.id
        
        # Eliminar
        calif.delete()
        
        messages.success(request, 'Calificación eliminada correctamente')
        
        if request.user.rol == 'profesor':
            return redirect('registrar_calificacion', curso_id=curso_id)
        else:
            return redirect('admin_calificaciones_lista')
    
    context = {
        'calificacion': calif,
    }
    return render(request, 'estudiantes/eliminar_calificacion.html', context)

# Vista para consultar notas (estudiantes)
@login_required
def mis_notas(request):
    if request.user.rol != 'estudiante':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('login')

    # Filtros
    curso_filter = request.GET.get('curso')
    tipo_filter = request.GET.get('tipo_evaluacion') or ''
    # Mapeo de alias en UI: "trabajo"→"taller"
    tipo_map = {'trabajo': 'taller'}
    tipo_filter = tipo_map.get(tipo_filter, tipo_filter)

    # Base queryset
    qs = Calificacion.objects.filter(
        inscripcion__estudiante=request.user
    ).select_related('inscripcion__curso', 'profesor').order_by('inscripcion__curso__nombre', '-fecha_evaluacion')

    if curso_filter:
        qs = qs.filter(inscripcion__curso_id=curso_filter)
    if tipo_filter:
        qs = qs.filter(tipo_evaluacion=tipo_filter)

    # Cursos disponibles para filtro
    cursos_disponibles = Curso.objects.filter(
        inscripcion__estudiante=request.user
    ).distinct()

    # Armar estructura por curso
    por_curso = {}
    for c in qs:
        curso = c.inscripcion.curso
        if curso.id not in por_curso:
            por_curso[curso.id] = {
                'curso': curso,
                'calificaciones': [],
                'nota_maxima': None,
                'nota_minima': None,
                'promedio': None,
            }
        por_curso[curso.id]['calificaciones'].append(c)

    calificaciones_por_curso = []
    total_calificaciones = qs.count()
    calificaciones_aprobadas = qs.filter(nota__gte=Decimal('3.0')).count()

    for item in por_curso.values():
        notas = [float(x.nota) for x in item['calificaciones']]
        if notas:
            item['nota_maxima'] = max(notas)
            item['nota_minima'] = min(notas)
            item['promedio'] = round(sum(notas) / len(notas), 1)
        calificaciones_por_curso.append(item)

    # Promedio general
    promedio_general = None
    if total_calificaciones:
        promedio_general = round(sum(float(x.nota) for x in qs) / total_calificaciones, 1)

    context = {
        'cursos_disponibles': cursos_disponibles,
        'calificaciones_por_curso': calificaciones_por_curso,
        'promedio_general': promedio_general,
        'total_calificaciones': total_calificaciones,
        'cursos_con_calificaciones': len(calificaciones_por_curso),
        'calificaciones_aprobadas': calificaciones_aprobadas,
    }
    return render(request, 'estudiantes/mis_calificaciones.html', context)

# Vista para mostrar notificaciones del usuario
@login_required
def notificaciones(request):
    estado = request.GET.get('estado', '')
    tipo = request.GET.get('tipo', '')

    notificaciones_query = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')

    # Estado
    if estado == 'leida':
        notificaciones_query = notificaciones_query.filter(leida=True)
    elif estado == 'no_leida':
        notificaciones_query = notificaciones_query.filter(leida=False)

    # Tipo (mapeos de UI a TIPOS_NOTIFICACION)
    if tipo:
        if tipo == 'calificacion':
            notificaciones_query = notificaciones_query.filter(tipo__in=['nueva_nota', 'cambio_nota'])
        elif tipo == 'sistema':
            notificaciones_query = notificaciones_query.filter(tipo='sistema')
        elif tipo == 'academico':
            # No hay tipos académicos específicos aún; dejamos el filtro vacío para futuro
            notificaciones_query = notificaciones_query.none()

    # Paginación
    paginator = Paginator(notificaciones_query, 10)
    page_number = request.GET.get('page')
    notificaciones_paginadas = paginator.get_page(page_number)

    # Estadísticas
    total_notificaciones = Notificacion.objects.filter(usuario=request.user).count()
    notificaciones_no_leidas = Notificacion.objects.filter(usuario=request.user, leida=False).count()
    notificaciones_leidas = total_notificaciones - notificaciones_no_leidas
    notificaciones_hoy = Notificacion.objects.filter(
        usuario=request.user,
        fecha_creacion__date=timezone.now().date()
    ).count()
    
    context = {
        'notificaciones': notificaciones_paginadas,
        'total_notificaciones': total_notificaciones,
        'notificaciones_no_leidas': notificaciones_no_leidas,
        'notificaciones_leidas': notificaciones_leidas,
        'notificaciones_hoy': notificaciones_hoy,
    }
    
    return render(request, 'estudiantes/notificaciones.html', context)

# Vista para mostrar y editar el perfil del usuario
@login_required
def perfil(request):
    user = request.user
    context = {'user': user}

    if user.rol == 'estudiante':
        inscripciones = Inscripcion.objects.filter(estudiante=user)
        calificaciones = Calificacion.objects.filter(inscripcion__estudiante=user)
        
        context.update({
            'total_cursos': inscripciones.count(),
            'total_calificaciones': calificaciones.count(),
            'promedio_general': calificaciones.aggregate(Avg('nota'))['nota__avg'] or 0,
            'cursos_aprobados': inscripciones.filter(
                calificacion__nota__gte=3.0
            ).distinct().count(),
            'porcentaje_aprobacion': (inscripciones.filter(
                calificacion__nota__gte=3.0
            ).distinct().count() / max(inscripciones.count(), 1)) * 100,
        })
        
    elif user.rol == 'profesor':
        cursos = Curso.objects.filter(profesor=user)
        calificaciones = Calificacion.objects.filter(profesor=user)  # CORREGIDO
        context.update({
            'total_cursos': cursos.count(),
            'total_estudiantes': Inscripcion.objects.filter(curso__profesor=user).count(),
            'total_calificaciones': calificaciones.count(),
            'promedio_cursos': cursos.aggregate(
                promedio=Avg('inscripcion__calificacion__nota')
            )['promedio'] or 0,
        })
    else:
        context.update({
            'total_usuarios': Usuario.objects.count(),
            'total_cursos': Curso.objects.count(),
            'total_calificaciones': Calificacion.objects.count(),
            'promedio_sistema': Calificacion.objects.aggregate(Avg('nota'))['nota__avg'] or 0,
        })
    
    # Actividad reciente (simulada)
    actividad_reciente = []
    if user.rol == 'estudiante':
        calificaciones_recientes = Calificacion.objects.filter(
            inscripcion__estudiante=user
        ).order_by('-fecha_registro')[:5]
        
        for cal in calificaciones_recientes:
            actividad_reciente.append({
                'descripcion': f'Nueva calificación en {cal.inscripcion.curso.nombre}: {cal.nota}',
                'fecha': cal.fecha_registro
            })
    
    context['actividad_reciente'] = actividad_reciente
    
    return render(request, 'estudiantes/perfil.html', context)

# Vista AJAX para marcar notificación como leída
@login_required
def marcar_notificacion_leida(request, notificacion_id):
    if request.method == 'POST':
        try:
            notificacion = get_object_or_404(
                Notificacion, 
                id=notificacion_id, 
                usuario=request.user
            )
            notificacion.leida = True
            notificacion.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Vista AJAX para eliminar notificación
@login_required
def eliminar_notificacion(request, notificacion_id):
    if request.method == 'POST':
        try:
            notificacion = get_object_or_404(
                Notificacion, 
                id=notificacion_id, 
                usuario=request.user
            )
            notificacion.delete()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

# Vista AJAX para obtener estudiantes de un curso
@login_required
def obtener_estudiantes_curso(request, curso_id):
    if request.method == 'GET' and request.user.rol == 'profesor':
        try:
            curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)
            inscripciones = Inscripcion.objects.filter(curso=curso).select_related('estudiante')
            
            estudiantes = []
            for inscripcion in inscripciones:
                estudiante = inscripcion.estudiante
                estudiantes.append({
                    'id': estudiante.id,
                    'nombre': f"{estudiante.first_name} {estudiante.last_name}",
                    'email': estudiante.email,
                    'inscripcion_id': inscripcion.id
                })
            
            return JsonResponse({'success': True, 'estudiantes': estudiantes})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'No autorizado'})

# Vista para listar estudiantes de un curso (profesores)
@login_required
def estudiantes_curso(request, curso_id=None):
    """
    Muestra la lista de estudiantes inscritos en un curso
    """
    if request.user.rol != 'profesor':
        messages.error(request, 'No tienes permisos para acceder a esta página')
        return redirect('login')
    
    cursos_disponibles = Curso.objects.filter(profesor=request.user, activo=True)
    # Permitir selección por ruta o por query param
    curso_sel_id = curso_id or request.GET.get('curso')
    curso_seleccionado = None
    estudiantes = []
    total_estudiantes = 0
    total_calificaciones = 0
    promedio_curso = None
    estudiantes_aprobados = 0
    stats = {'excelente': 0, 'sobresaliente': 0, 'bueno': 0, 'aceptable': 0, 'insuficiente': 0, 'nota_maxima': None, 'nota_minima': None, 'tasa_aprobacion': 0}

    if curso_sel_id:
        curso_seleccionado = get_object_or_404(Curso, id=curso_sel_id, profesor=request.user, activo=True)
        inscripciones = Inscripcion.objects.filter(curso=curso_seleccionado, activo=True).select_related('estudiante')
        total_estudiantes = inscripciones.count()

        notas_todas = []
        for insc in inscripciones:
            califs = Calificacion.objects.filter(inscripcion=insc).order_by('-fecha_registro')
            notas = list(califs.values_list('nota', flat=True))
            total_calificaciones += len(notas)
            if notas:
                notas_float = [float(n) for n in notas]
                notas_todas.extend(notas_float)
                promedio = round(sum(notas_float) / len(notas_float), 1)
                if promedio >= 3.0:
                    estudiantes_aprobados += 1
                ultima = califs.first()
            else:
                promedio = None
                ultima = None

            estudiantes.append({
                'estudiante': insc.estudiante,
                'total_calificaciones': len(notas),
                'promedio': promedio,
                'ultima_calificacion': ultima,
            })

        if notas_todas:
            promedio_curso = round(sum(notas_todas) / len(notas_todas), 1)
            stats['nota_maxima'] = max(notas_todas)
            stats['nota_minima'] = min(notas_todas)
            # Distribución
            for n in notas_todas:
                if 4.6 <= n <= 5.0: stats['excelente'] += 1
                elif 4.0 <= n <= 4.5: stats['sobresaliente'] += 1
                elif 3.5 <= n <= 3.9: stats['bueno'] += 1
                elif 3.0 <= n <= 3.4: stats['aceptable'] += 1
                else: stats['insuficiente'] += 1
            stats['tasa_aprobacion'] = (estudiantes_aprobados / max(total_estudiantes, 1)) * 100

    context = {
        'cursos_disponibles': cursos_disponibles,
        'curso_seleccionado': curso_seleccionado,
        'estudiantes': estudiantes,
        'total_estudiantes': total_estudiantes,
        'total_calificaciones': total_calificaciones,
        'promedio_curso': promedio_curso,
        'estudiantes_aprobados': estudiantes_aprobados,
        'stats': stats,
    }
    return render(request, 'estudiantes/estudiantes_curso.html', context)

# US-022: NUEVA - Gestión de periodos (admin_views)
# US-023: MEJORAR - Ver promedios (ya existe en perfil y dashboard)
# US-024: NUEVA - Ver estado académico

@login_required
def ver_estado_academico(request):
    """Ver estado académico del estudiante (Regular/En Riesgo/Reprobado)"""
    if request.user.rol != 'estudiante':
        messages.error(request, 'Esta función es solo para estudiantes')
        return redirect('dashboard')
    
    calificaciones = Calificacion.objects.filter(inscripcion__estudiante=request.user)
    promedio_general = calificaciones.aggregate(Avg('nota'))['nota__avg']
    
    if not promedio_general:
        estado = 'Sin Calificaciones'
        color = 'grey'
        mensaje = 'Aún no tienes calificaciones registradas'
    elif promedio_general >= 3.5:
        estado = 'Regular'
        color = 'green'
        mensaje = '¡Excelente trabajo! Mantén tu buen rendimiento académico'
    elif promedio_general >= 3.0:
        estado = 'En Riesgo'
        color = 'orange'
        mensaje = 'Tu rendimiento está en riesgo. Te recomendamos hablar con tus profesores y reforzar tus estudios'
    else:
        estado = 'Reprobado'
        color = 'red'
        mensaje = 'Tu promedio está por debajo del mínimo. Es urgente que busques apoyo académico'
    
    context = {
        'estado': estado,
        'color': color,
        'mensaje': mensaje,
        'promedio_general': promedio_general,
    }
    return render(request, 'estudiantes/estado_academico.html', context)

# US-026: NUEVA - Buscador global
@login_required
def buscador_global(request):
    """Buscador global según rol del usuario"""
    query = request.GET.get('q', '').strip()
    resultados = []
    
    if query:
        if request.user.rol == 'estudiante':
            # Buscar en cursos inscritos
            cursos = Curso.objects.filter(
                inscripcion__estudiante=request.user,
                nombre__icontains=query
            ) | Curso.objects.filter(
                inscripcion__estudiante=request.user,
                codigo__icontains=query
            )
            for curso in cursos:
                resultados.append({
                    'tipo': 'Curso',
                    'nombre': f'{curso.nombre} ({curso.codigo})',
                    'url': f"{reverse('mis_calificaciones')}?curso={curso.id}"
                })
            
            # Buscar en calificaciones propias
            calificaciones = Calificacion.objects.filter(
                inscripcion__estudiante=request.user,
                inscripcion__curso__nombre__icontains=query
            ).distinct()[:5]
            for cal in calificaciones:
                resultados.append({
                    'tipo': 'Calificación',
                    'nombre': f'{cal.inscripcion.curso.nombre} - {cal.get_tipo_evaluacion_display()}',
                    'url': reverse('mis_calificaciones')
                })
        
        elif request.user.rol == 'profesor':
            # Buscar cursos asignados
            cursos = Curso.objects.filter(
                profesor=request.user,
                nombre__icontains=query
            ) | Curso.objects.filter(
                profesor=request.user,
                codigo__icontains=query
            )
            for curso in cursos:
                resultados.append({
                    'tipo': 'Curso',
                    'nombre': f'{curso.nombre} ({curso.codigo})',
                    'url': reverse('estudiantes_curso', kwargs={'curso_id': curso.id})
                })
            
            # Buscar estudiantes
            estudiantes = Usuario.objects.filter(
                rol='estudiante',
                inscripcion__curso__profesor=request.user
            ).filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)
            ).distinct()[:10]
            for est in estudiantes:
                resultados.append({
                    'tipo': 'Estudiante',
                    'nombre': f'{est.first_name} {est.last_name} ({est.username})',
                    'url': reverse('dashboard_profesor')
                })
        
        elif request.user.rol == 'administrador':
            # Buscar usuarios
            usuarios = Usuario.objects.filter(
                Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)
            )[:10]
            for usr in usuarios:
                resultados.append({
                    'tipo': 'Usuario',
                    'nombre': f'{usr.first_name} {usr.last_name} ({usr.get_rol_display()})',
                    'url': reverse('admin_usuario_editar', kwargs={'usuario_id': usr.id})
                })
            
            # Buscar cursos
            cursos = Curso.objects.filter(
                Q(nombre__icontains=query) | Q(codigo__icontains=query)
            )[:10]
            for curso in cursos:
                resultados.append({
                    'tipo': 'Curso',
                    'nombre': f'{curso.nombre} ({curso.codigo})',
                    'url': reverse('admin_curso_editar', kwargs={'curso_id': curso.id})
                })
    
    context = {
        'query': query,
        'resultados': resultados,
    }
    return render(request, 'estudiantes/buscador.html', context)

# US-027: Ya implementado (accesos rápidos en mis_cursos y dashboard_profesor)
# US-028: Ya implementado (perfil con botones detallados)

# US-012: MEJORAR - Actualizar datos personales
@login_required
def actualizar_perfil(request):
    """Actualizar datos de contacto del usuario"""
    if request.method == 'POST':
        nombre = request.POST.get('first_name', '').strip()
        apellido = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        
        # Validaciones
        if not nombre or len(nombre) < 3:
            messages.error(request, 'El nombre debe tener al menos 3 caracteres')
            return redirect('perfil')
        
        if not apellido or len(apellido) < 3:
            messages.error(request, 'El apellido debe tener al menos 3 caracteres')
            return redirect('perfil')
        
        if not email or '@' not in email:
            messages.error(request, 'Ingrese un correo electrónico válido')
            return redirect('perfil')
        
        # Verificar email único (excluyendo el actual)
        if Usuario.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, 'Ese correo ya está registrado por otro usuario')
            return redirect('perfil')
        
        if telefono and len(telefono) != 10:
            messages.error(request, 'El teléfono debe tener exactamente 10 dígitos')
            return redirect('perfil')
        
        # Actualizar
        request.user.first_name = nombre
        request.user.last_name = apellido
        request.user.email = email
        if telefono:
            request.user.telefono = telefono
        request.user.save()
        
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('perfil')
    
    return redirect('perfil')

# US-013: NUEVA - Descargar comprobante PDF
@login_required
def descargar_comprobante(request):
    """Generar y descargar comprobante de calificaciones en PDF"""
    if request.user.rol != 'estudiante':
        messages.error(request, 'Esta función es solo para estudiantes')
        return redirect('dashboard')
    
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from datetime import datetime
    
    # Obtener calificaciones del estudiante
    calificaciones = Calificacion.objects.filter(
        inscripcion__estudiante=request.user
    ).select_related('inscripcion__curso', 'profesor').order_by('inscripcion__curso__nombre', '-fecha_evaluacion')
    
    if not calificaciones.exists():
        messages.warning(request, 'No tienes calificaciones registradas para generar un comprobante')
        return redirect('mis_calificaciones')
    
    # Crear PDF
    response = HttpResponse(content_type='application/pdf')
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    filename = f'Comprobante_Calificaciones_{request.user.first_name}_{fecha_actual}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1B3C53'),
        spaceAfter=30,
        alignment=1  # Centrado
    )
    elements.append(Paragraph('COMPROBANTE DE CALIFICACIONES', title_style))
    elements.append(Paragraph('Sistema de Gestión de Notas - TROLI', styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Información del estudiante (SIN numero_documento)
    info_data = [
        ['Estudiante:', f'{request.user.first_name} {request.user.last_name}'],
        ['Usuario:', request.user.username],
        ['Email:', request.user.email],
        ['Fecha de emisión:', datetime.now().strftime("%d/%m/%Y %H:%M")],
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F9F3EF')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de calificaciones
    elements.append(Paragraph('CALIFICACIONES POR CURSO', styles['Heading2']))
    elements.append(Spacer(1, 0.2*inch))
    
    # Agrupar por curso
    por_curso = {}
    for c in calificaciones:
        curso = c.inscripcion.curso
        if curso.id not in por_curso:
            por_curso[curso.id] = {'curso': curso, 'calificaciones': []}
        por_curso[curso.id]['calificaciones'].append(c)
    
    # Crear tabla por cada curso
    for item in por_curso.values():
        curso = item['curso']
        elements.append(Paragraph(f'<b>{curso.nombre} ({curso.codigo})</b>', styles['Normal']))
        
        data = [['Tipo', 'Calificación', 'Fecha', 'Profesor']]
        for cal in item['calificaciones']:
            data.append([
                cal.get_tipo_evaluacion_display(),
                str(cal.nota),
                cal.fecha_evaluacion.strftime("%d/%m/%Y") if cal.fecha_evaluacion else 'N/A',
                f'{cal.profesor.first_name} {cal.profesor.last_name}'
            ])
        
        table = Table(data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B3C53')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Promedio general
    promedio_general = calificaciones.aggregate(Avg('nota'))['nota__avg']
    if promedio_general:
        promedio_data = [['PROMEDIO GENERAL:', f'{promedio_general:.1f}']]
        promedio_table = Table(promedio_data, colWidths=[4*inch, 2*inch])
        promedio_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#6B9BD1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(promedio_table)
    
    # Pie de página
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph('<i>Documento generado automáticamente por el Sistema TROLI</i>', styles['Normal']))
    
    doc.build(elements)
    return response

# US-014: NUEVA - Cambiar contraseña
@login_required
def cambiar_contrasena(request):
    """Cambiar contraseña del usuario autenticado"""
    if request.method == 'POST':
        contrasena_actual = request.POST.get('current_password', '').strip()
        nueva_contrasena = request.POST.get('new_password', '').strip()
        confirmar_contrasena = request.POST.get('confirm_password', '').strip()
        
        # Validar contraseña actual
        if not request.user.check_password(contrasena_actual):
            messages.error(request, 'La contraseña actual es incorrecta')
            return redirect('perfil')
        
        # Validar que las nuevas contraseñas coincidan
        if nueva_contrasena != confirmar_contrasena:
            messages.error(request, 'Las contraseñas nuevas no coinciden')
            return redirect('perfil')
        
        # Validar longitud mínima
        if len(nueva_contrasena) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
            return redirect('perfil')
        
        # Validar que tenga mayúscula, número y carácter especial
        import re
        if not re.search(r'[A-Z]', nueva_contrasena):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula')
            return redirect('perfil')
        
        if not re.search(r'[0-9]', nueva_contrasena):
            messages.error(request, 'La contraseña debe contener al menos un número')
            return redirect('perfil')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', nueva_contrasena):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial (!@#$%^&*)')
            return redirect('perfil')
        
        # Cambiar la contraseña
        request.user.set_password(nueva_contrasena)
        request.user.save()
        
        # Crear notificación
        Notificacion.objects.create(
            usuario=request.user,
            tipo='sistema',
            titulo='Contraseña cambiada',
            mensaje='Tu contraseña ha sido cambiada exitosamente'
        )
        
        # Mantener la sesión activa después del cambio
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, 'Contraseña cambiada correctamente')
        return redirect('perfil')
    
    return redirect('perfil')
