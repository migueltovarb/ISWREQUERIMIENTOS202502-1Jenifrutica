from django.urls import path
from . import views, admin_views

urlpatterns = [
    # Autenticación
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Dashboards específicos por rol
    path('dashboard/estudiante/', views.dashboard_estudiante, name='dashboard_estudiante'),
    path('dashboard/profesor/', views.dashboard_profesor, name='dashboard_profesor'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    # Estudiantes
    path('estudiante/calificaciones/', views.ver_calificaciones, name='ver_calificaciones'),
    path('estudiante/mis-calificaciones/', views.mis_notas, name='mis_calificaciones'),
    path('estudiante/inscribirse/', views.inscribirse_curso, name='inscribirse_curso'),
    path('estudiante/mis-cursos/', views.mis_cursos, name='mis_cursos'),
    
    # Profesores
    path('profesor/cursos/', views.profesor_cursos, name='profesor_cursos'),
    path('profesor/curso/<int:curso_id>/estudiantes/', views.estudiantes_curso, name='estudiantes_curso'),
    path('profesor/calificar/<int:curso_id>/', views.registrar_calificacion, name='registrar_calificacion'),
    path('profesor/calificar/<int:inscripcion_id>/', views.calificar_estudiante, name='calificar_estudiante'),
    path('profesor/editar-calificacion/<int:calificacion_id>/', views.editar_calificacion, name='editar_calificacion'),
    path('profesor/eliminar-calificacion/<int:calificacion_id>/', views.eliminar_calificacion, name='eliminar_calificacion'),
    
    # Notificaciones y perfil
    path('notificaciones/', views.notificaciones, name='notificaciones'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/cambiar-contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    
    # US-013: Descargar comprobante PDF
    path('estudiante/descargar-comprobante/', views.descargar_comprobante, name='descargar_comprobante'),
    
    # US-024: Ver estado académico
    path('estudiante/estado-academico/', views.ver_estado_academico, name='estado_academico'),
    
    # US-026: Buscador global
    path('buscar/', views.buscador_global, name='buscador_global'),
    
    # ============= PANEL DE ADMINISTRACIÓN PERSONALIZADO =============
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Gestión de usuarios
    path('admin-panel/usuarios/', admin_views.admin_usuarios_lista, name='admin_usuarios_lista'),
    path('admin-panel/usuarios/crear/', admin_views.admin_usuario_crear, name='admin_usuario_crear'),
    path('admin-panel/usuarios/<int:usuario_id>/editar/', admin_views.admin_usuario_editar, name='admin_usuario_editar'),
    path('admin-panel/usuarios/<int:usuario_id>/eliminar/', admin_views.admin_usuario_eliminar, name='admin_usuario_eliminar'),
    
    # Gestión de cursos
    path('admin-panel/cursos/', admin_views.admin_cursos_lista, name='admin_cursos_lista'),
    path('admin-panel/cursos/crear/', admin_views.admin_curso_crear, name='admin_curso_crear'),
    path('admin-panel/cursos/<int:curso_id>/editar/', admin_views.admin_curso_editar, name='admin_curso_editar'),
    path('admin-panel/cursos/<int:curso_id>/eliminar/', admin_views.admin_curso_eliminar, name='admin_curso_eliminar'),
    
    # Gestión de inscripciones
    path('admin-panel/inscripciones/', admin_views.admin_inscripciones_lista, name='admin_inscripciones_lista'),
    path('admin-panel/inscripciones/crear/', admin_views.admin_inscripcion_crear, name='admin_inscripcion_crear'),
    path('admin-panel/inscripciones/<int:inscripcion_id>/eliminar/', admin_views.admin_inscripcion_eliminar, name='admin_inscripcion_eliminar'),
    
    # Gestión de calificaciones
    path('admin-panel/calificaciones/', admin_views.admin_calificaciones_lista, name='admin_calificaciones_lista'),
    path('admin-panel/historial/', admin_views.admin_historial_lista, name='admin_historial_lista'),
    
    # Reportes
    path('admin-panel/reportes/', admin_views.admin_reportes, name='admin_reportes'),
    
    # Generación de Reportes Académicos
    path('admin-panel/generar-reporte/', admin_views.admin_generar_reporte, name='admin_generar_reporte'),
    path('admin-panel/exportar-reporte-pdf/', admin_views.admin_exportar_reporte_pdf, name='admin_exportar_reporte_pdf'),
    path('admin-panel/guardar-reporte/', admin_views.admin_guardar_reporte, name='admin_guardar_reporte'),
    path('admin-panel/cargar-reporte/<int:reporte_id>/', admin_views.admin_cargar_reporte_guardado, name='admin_cargar_reporte_guardado'),
    path('admin-panel/editar-reporte/<int:reporte_id>/', admin_views.admin_editar_reporte, name='admin_editar_reporte'),
    path('admin-panel/eliminar-reporte/<int:reporte_id>/', admin_views.admin_eliminar_reporte, name='admin_eliminar_reporte'),
]