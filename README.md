# Sistema de Gestión de Notas - Django

## Descripción
Sistema completo de gestión académica desarrollado en Django que permite la administración de estudiantes, profesores, cursos, calificaciones y notificaciones con diferentes roles de usuario.

## Características Principales

### Roles de Usuario
- **Administrador**: Gestión completa del sistema
- **Profesor**: Registro de calificaciones y gestión de cursos
- **Estudiante**: Consulta de calificaciones y notificaciones

### Funcionalidades por Rol

#### Administrador
- Dashboard con estadísticas del sistema
- Gestión de usuarios, cursos y calificaciones
- Acceso al panel de administración de Django
- Visualización de actividad del sistema
- Gestión de notificaciones

#### Profesor
- Dashboard personalizado con estadísticas de cursos
- Registro y modificación de calificaciones
- Visualización de estudiantes por curso
- Gestión de notificaciones
- Historial de calificaciones registradas

#### Estudiante
- Dashboard con resumen académico
- Consulta detallada de calificaciones por curso
- Sistema de notificaciones
- Perfil personal editable
- Estadísticas de rendimiento académico

### Interfaz de Usuario
- Diseño moderno y responsivo
- Paleta de colores profesional
- Navegación intuitiva
- Mensajes de confirmación y validación
- Animaciones suaves

## Instalación y Configuración

### Requisitos
- Python 3.8+
- Django 5.2.7
- SQLite (incluido por defecto)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**
```bash
cd TROLI_GESTION_NOTAS
```

2. **Instalar dependencias**
```bash
pip install django
```

3. **Aplicar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear datos de prueba**
```bash
python tests/crear_datos_prueba.py
```

5. **Ejecutar el servidor**
```bash
python manage.py runserver
```

6. **Acceder al sistema**
Abrir navegador en: http://127.0.0.1:8000/

## Credenciales de Acceso

### Administrador
- **Usuario**: admin
- **Contraseña**: admin123
- **Acceso**: Panel completo de administración

### Profesores
- **Usuario**: prof_matematicas
- **Contraseña**: prof123
- **Cursos**: Matemáticas Avanzadas, Álgebra Linear

- **Usuario**: prof_fisica
- **Contraseña**: prof123
- **Cursos**: Física Cuántica

### Estudiantes
- **Usuario**: estudiante1 a estudiante8
- **Contraseña**: est123
- **Acceso**: Dashboard estudiantil y consulta de notas

## Estructura del Proyecto

```
TROLI_GESTION_NOTAS/
├── db.sqlite3              # Base de datos SQLite
├── manage.py               # Comando Django
├── README.md               # Documentación principal
├── requirements.txt        # Dependencias del proyecto
├── docs/                   # Documentación
│   └── scripts/
│       └── cargar_datos.ps1  # Script de carga de datos
├── estudiantes/            # Aplicación principal
│   ├── models.py           # Modelos de datos
│   ├── views.py            # Vistas estudiantes
│   ├── admin_views.py      # Vistas administrador
│   ├── urls.py             # URLs de la aplicación
│   ├── admin.py            # Configuración admin
│   ├── forms.py            # Formularios Django
│   ├── decorators.py       # Decoradores personalizados
│   ├── management/         # Comandos personalizados
│   │   └── commands/
│   │       └── cargar_datos.py
│   ├── migrations/         # Migraciones de base de datos
│   ├── templates/          # Plantillas HTML
│   │   ├── admin/          # Templates administrador
│   │   ├── estudiantes/    # Templates estudiantes
│   │   └── registration/   # Templates autenticación
│   └── static/             # Archivos estáticos
│       └── style.css       # Estilos CSS
├── gestion_notas/          # Configuración principal
│   ├── settings.py         # Configuraciones Django
│   ├── urls.py             # URLs principales
│   └── wsgi.py             # Configuración WSGI
├── static/                 # Archivos estáticos globales
│   └── style.css           # Estilos CSS globales
├── tests/                  # Pruebas del proyecto
│   ├── crear_datos_prueba.py   # Script de datos de prueba
│   ├── test_reporte.py         # Tests de reportes
│   └── test_reporte_usuario.py # Tests de reportes por usuario
└── venv/                   # Entorno virtual (no incluir en git)
```

## Modelos de Datos

### Usuario (AbstractUser)
- Roles: estudiante, profesor, administrador, coordinador
- Información personal y de contacto
- Sistema de autenticación integrado

### Curso
- Información del curso (nombre, código, descripción)
- Asignación de profesor
- Gestión de créditos y estado

### Inscripción
- Relación estudiante-curso
- Control de fechas y estado activo

### Calificación
- Notas con validación (0.0 - 5.0)
- Tipos de evaluación (parcial, final, taller, etc.)
- Historial de cambios
- Observaciones del profesor

### Notificación
- Sistema de mensajería interna
- Tipos: nueva_nota, cambio_nota, recordatorio, sistema
- Estado de lectura

## Funcionalidades Técnicas

### Validaciones
- Notas entre 0.0 y 5.0
- Campos obligatorios en formularios
- Validación de roles y permisos

### Seguridad
- Autenticación requerida para todas las vistas
- Decoradores de login_required
- Validación de roles por vista

### Base de Datos
- Migraciones automáticas
- Relaciones ForeignKey optimizadas
- Índices para consultas eficientes

### Interfaz
- Templates responsivos
- JavaScript para interactividad
- CSS moderno con variables
- Mensajes de Django integrados

## Datos de Prueba Incluidos

El sistema incluye:
- 1 Administrador
- 2 Profesores con cursos asignados
- 8 Estudiantes inscritos en múltiples cursos
- 3 Cursos académicos
- 84 Calificaciones distribuidas
- 6 Notificaciones de ejemplo

## URLs Principales

- `/` - Página de login
- `/dashboard/estudiante/` - Dashboard del estudiante
- `/dashboard/profesor/` - Dashboard del profesor  
- `/dashboard/admin/` - Dashboard del administrador
- `/mis-calificaciones/` - Consulta de notas (estudiantes)
- `/registrar-calificacion/` - Registro de notas (profesores)
- `/notificaciones/` - Gestión de notificaciones
- `/perfil/` - Perfil de usuario
- `/admin/` - Panel de administración Django

## Soporte y Desarrollo

### Tecnologías Utilizadas
- **Backend**: Django 5.2.7
- **Frontend**: HTML5, CSS3, JavaScript
- **Base de Datos**: SQLite
- **Autenticación**: Django Auth System

### Características Avanzadas
- Sistema de notificaciones en tiempo real
- Historial de cambios en calificaciones
- Filtros y búsquedas avanzadas
- Exportación de datos
- Responsive design

## Próximas Mejoras Sugeridas
- Integración con email para notificaciones
- Reportes en PDF
- Gráficos de rendimiento
- API REST
- Sistema de backup automático

---

**Desarrollado con Django Framework**  
*4. Sistema de Gestión de Estudiantes y Notas*