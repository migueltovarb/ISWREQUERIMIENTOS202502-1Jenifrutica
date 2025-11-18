# 5. Requisitos No Funcionales

A continuación se presentan los requisitos no funcionales del sistema, organizados por atributos de calidad. Cada requisito está identificado con un código único (EC-XXX), siguiendo el formato estándar para facilitar su trazabilidad y referencia en la documentación y el desarrollo.

## 5.1 Requisitos No Funcionales por Atributo de Calidad

### 5.1.1 Rendimiento

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-001  | Usuario final         | Consulta de notas             | Sistema completo  | Uso normal       | El sistema responde en ≤ 3 segundos a consultas básicas           | Tiempo de respuesta ≤ 3 segundos        |
| EC-002  | Usuario final         | Generación de reportes        | Sistema completo  | Uso normal       | El sistema genera reportes en ≤ 5 segundos                        | Tiempo de respuesta ≤ 5 segundos        |
| EC-003  | Administrador         | Pico de usuarios simultáneos  | Sistema completo  | Pico de uso      | Soporta 100-300 usuarios sin degradación                          | Usuarios simultáneos ≥ 100 y ≤ 300      |
| EC-004  | Administrador         | Crecimiento de cursos         | Sistema completo  | Escalabilidad    | Soporta de 20 a 200+ cursos sin degradación                       | Cursos activos ≥ 200                    |
| EC-005  | Administrador         | Crecimiento de usuarios       | Sistema completo  | Escalabilidad    | Escala de 50-200 a 100-300 usuarios simultáneos                   | Usuarios simultáneos ≥ 300              |

### 5.1.2 Disponibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-006  | Usuario final         | Acceso al sistema             | Sistema completo  | 24/7             | Disponible 24/7 salvo mantenimientos notificados                  | Disponibilidad ≥ 99%                    |

### 5.1.3 Seguridad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-007  | Administrador         | Almacenamiento de contraseñas | Sistema completo  | Uso normal       | Contraseñas encriptadas con algoritmos seguros                    | Uso de bcrypt o Argon2                  |
| EC-008  | Administrador         | Acceso por roles              | Sistema completo  | Uso normal       | Control de acceso por roles (RBAC)                                | Funcionalidad restringida por perfil     |
| EC-009  | Auditor               | Acción crítica                | Sistema completo  | Uso normal       | Registro de auditoría de acciones críticas                        | Registro con fecha, hora y usuario       |
| EC-010  | Legal                 | Protección de datos           | Sistema completo  | Uso normal       | Cumple Habeas Data/confidencialidad académica                     | Cumplimiento normativo                  |
| EC-011  | Administrador         | Transmisión de datos          | Sistema completo  | Uso normal       | Comunicación cifrada por HTTPS                                    | 100% tráfico por HTTPS                  |

### 5.1.4 Accesibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-012  | Usuario final         | Acceso multiplataforma        | Sistema completo  | Diferentes dispositivos | Accesible desde PC, tablet y móvil con diseño responsivo      | Compatible con navegadores modernos      |
| EC-013  | Usuario final         | Accesibilidad web             | Sistema completo  | Uso normal       | Cumple WCAG 2.1 AA, contraste, fuente ajustable, lectores pantalla| Cumplimiento WCAG 2.1 AA                |

### 5.1.5 Usabilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-014  | Usuario final         | Interacción                   | Interfaz gráfica  | Uso normal       | Interfaz intuitiva, navegación sencilla                           | 90% usuarios completan tareas sin ayuda |
| EC-015  | Institución           | Identidad visual              | Interfaz gráfica  | Uso normal       | Respeta identidad visual institucional                            | Uso de logo y colores oficiales         |
| EC-016  | Usuario final         | Idioma                        | Sistema completo  | Uso normal       | Todo el sistema en español                                        | 100% interfaz y mensajes en español     |
| EC-017  | Usuario final         | Error                         | Sistema completo  | Uso normal       | Mensajes de error claros y orientados al usuario                   | Mensajes específicos y sugerencias      |

### 5.1.6 Mantenibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-018  | Desarrollador         | Solicitud de modificación     | Código fuente     | Desarrollo       | Código limpio, documentado y buenas prácticas                     | Cambios menores ≤ 2 horas               |

### 5.1.7 Exportación y Confirmación

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-019  | Usuario final         | Exportar reportes             | Sistema completo  | Uso normal       | Exporta reportes en PDF y Excel con formato y legibilidad         | Exportación funcional                   |
| EC-020  | Usuario final         | Acción crítica                | Sistema completo  | Uso normal       | Solicita confirmación antes de acciones críticas                  | Confirmación obligatoria                |

---

## 5.4 Árbol de utilidad

El siguiente árbol de utilidad representa la estructura funcional principal del sistema de gestión de notas. Puedes usar este esquema para diagramarlo en Miro:

```
Sistema de Gestión de Notas
├── Consultar Notas
│   └── Ver notas por estudiante
├── Registrar Notas
│   ├── Ingresar calificaciones
│   └── Modificar calificaciones
├── Generar Reportes
│   ├── Reporte por curso
│   └── Reporte por estudiante
├── Gestión de Usuarios
│   ├── Crear usuario (Estudiante, Profesor, Administrador)
│   ├── Editar usuario
│   └── Eliminar usuario
├── Control de Acceso
│   └── Restricción por roles (Estudiante, Profesor, Administrador)
├── Auditoría
│   └── Registro de acciones críticas
├── Exportar Reportes
│   ├── Exportar a PDF
│   └── Exportar a Excel
├── Notificaciones
│   ├── Confirmación de acciones críticas
│   └── Mensajes de error claros
├── Accesibilidad
│   ├── Multiplataforma (PC, tablet, móvil)
│   └── Accesibilidad para personas con discapacidad
├── Configuración
│   ├── Idioma español
│   └── Diseño visual institucional
```