# 5. Requisitos No Funcionales

---

## 5.1 OBJETIVOS DE NEGOCIO

| Objetivo | Descripción | Tiempo de cumplimiento | Mejora esperada al negocio |
|----------|-------------|-----------------------|----------------------------|
| OBJ-01 | Mejorar la eficiencia operativa a través del uso de la plataforma digital | 1 año | Reducción del tiempo de gestión de tareas y proyectos |
| OBJ-02 | Aumentar la satisfacción del usuario mediante una experiencia fluida y rápida | 1 año | Mayor adopción del sistema y retención de usuarios |
| OBJ-03 | Garantizar la seguridad y trazabilidad de la información en la plataforma | 1 año | Incremento en la confianza del cliente y cumplimiento normativo |
| OBJ-04 | Optimizar el rendimiento del sistema para soportar múltiples usuarios simultáneamente | 1 año | Mejor desempeño en operaciones críticas |
| OBJ-05 | Facilitar la integración con otras herramientas utilizadas por la empresa | 1 año | Mejora en la interoperabilidad y automatización de procesos |

---

## 5.2 RESTRICCIONES DE NEGOCIO

| Restricción | Usuario que expresa la restricción | Justificación |
|-------------|------------------------------------|---------------|
| El sistema debe estar en funcionamiento dentro del periodo establecido por la dirección | Gerente de Proyectos | Se debe cumplir con el cronograma para asegurar el inicio del uso operativo |
| El desarrollo y puesta en producción del sistema no debe exceder el presupuesto asignado | Director de Tecnología (CTO) | No se dispone dinero para implementación adicional a lo previsto |
| El desarrollo del sistema no incluye funciones de facturación o pagos en línea | Dueño del producto | Se prioriza la gestión de proyectos y tareas sobre funciones financieras externas |
| El proyecto debe realizarse utilizando el personal actual del equipo de TI | Gerente de Recursos Humanos | No se autoriza contratación adicional para el desarrollo del sistema |

---

## 5.3 RESTRICCIONES DE TECNOLOGÍA

| Restricción | Usuario que expresa la restricción | Justificación |
|-------------|------------------------------------|---------------|
| El desarrollo del sistema debe realizarse usando Python y el framework Django | Gerente de Tecnología | Python con Django facilita un desarrollo ágil, seguro y escalable, con amplia comunidad y soporte |
| Se utilizará SQLite como sistema gestor de base de datos | Gerente de Tecnología | SQLite es ligero, fácil de configurar y adecuado para entornos de desarrollo y proyectos de pequeña escala |
| El sistema debe implementar protocolos de seguridad actuales (SSL/TLS) para la protección de la información en tránsito | Gerente de Seguridad Informática | Garantiza la confidencialidad e integridad de los datos durante la comunicación |

---

## 5.4 REQUISITOS SIGNIFICATIVOS DE ARQUITECTURA

| Código | Categoría | Descripción |
|--------|-----------|-------------|
| RNF001 | Usabilidad | La interfaz debe presentar únicamente los elementos necesarios para cada tarea según el rol del usuario, con etiquetas claras y una jerarquía visual bien definida |
| RNF002 | Seguridad | El sistema debe implementar autenticación mediante correo electrónico y contraseña con encriptación de credenciales |
| RNF003 | Seguridad | El sistema debe implementar control de acceso granular según roles: Estudiante, Profesor, Administrador |
| RNF004 | Rendimiento | El sistema debe responder a las acciones del usuario en menos de 3 segundos para operaciones normales y menos de 10 segundos para generación de reportes |
| RNF005 | Fiabilidad | El sistema debe estar disponible 24/7 con un tiempo de actividad del 99% durante horario laboral (7 am - 6 pm) |
| RNF006 | Escalabilidad | El sistema debe soportar al menos 100 usuarios concurrentes sin degradación de rendimiento |
| RNF007 | Portabilidad | El sistema debe funcionar correctamente en Chrome, Firefox, Edge y Safari (últimas 2 versiones) |
| RNF008 | Usabilidad/Portabilidad | La interfaz debe adaptarse a diferentes tamaños de pantalla (desktop, tablet, smartphone) manteniendo funcionalidad completa |
| RNF009 | Funcionalidad | El sistema debe permitir adjuntar archivos PDF, Excel (XLS/XLSX) e imágenes (JPG, PNG) con tamaño máximo de 10MB por archivo |
| RNF010 | Funcionalidad / Rendimiento | Los comentarios en tareas y proyectos deben reflejarse en tiempo real para todos los usuarios con acceso |
| RNF011 | Seguridad | Datos sensibles (contraseñas, información de proyectos críticos) deben estar encriptados en base de datos |
| RNF012 | Mantenibilidad | El código debe seguir estándares de programación y estar documentado para facilitar mantenimiento futuro |
| RNF013 | Fiabilidad | El sistema debe realizar backups automáticos diarios de la base de datos con capacidad de recuperación en menos de 4 horas |
| RNF014 | Seguridad / Mantenibilidad | El sistema debe registrar todas las acciones críticas realizadas por los usuarios con fecha, hora y usuario responsable para auditoría |

---

## 5.5 ESCENARIOS DE CALIDAD

### Requisitos No Funcionales por Atributo de Calidad

#### 5.5.1 Rendimiento

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-001  | Usuario final         | Consulta de notas             | Sistema completo  | Uso normal       | El sistema responde en ≤ 3 segundos a consultas básicas           | Tiempo de respuesta ≤ 3 segundos        |
| EC-002  | Usuario final         | Generación de reportes        | Sistema completo  | Uso normal       | El sistema genera reportes en ≤ 5 segundos                        | Tiempo de respuesta ≤ 5 segundos        |
| EC-003  | Administrador         | Pico de usuarios simultáneos  | Sistema completo  | Pico de uso      | Soporta 100-300 usuarios sin degradación                          | Usuarios simultáneos ≥ 100 y ≤ 300      |
| EC-004  | Administrador         | Crecimiento de cursos         | Sistema completo  | Escalabilidad    | Soporta de 20 a 200+ cursos sin degradación                       | Cursos activos ≥ 200                    |
| EC-005  | Administrador         | Crecimiento de usuarios       | Sistema completo  | Escalabilidad    | Escala de 50-200 a 100-300 usuarios simultáneos                   | Usuarios simultáneos ≥ 300              |

#### 5.5.2 Disponibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-006  | Usuario final         | Acceso al sistema             | Sistema completo  | 24/7             | Disponible 24/7 salvo mantenimientos notificados                  | Disponibilidad ≥ 99%                    |

#### 5.5.3 Seguridad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-007  | Administrador         | Almacenamiento de contraseñas | Sistema completo  | Uso normal       | Contraseñas encriptadas con algoritmos seguros                    | Uso de bcrypt o Argon2                  |
| EC-008  | Administrador         | Acceso por roles              | Sistema completo  | Uso normal       | Control de acceso por roles (RBAC)                                | Funcionalidad restringida por perfil     |
| EC-009  | Auditor               | Acción crítica                | Sistema completo  | Uso normal       | Registro de auditoría de acciones críticas                        | Registro con fecha, hora y usuario       |
| EC-010  | Legal                 | Protección de datos           | Sistema completo  | Uso normal       | Cumple Habeas Data/confidencialidad académica                     | Cumplimiento normativo                  |
| EC-011  | Administrador         | Transmisión de datos          | Sistema completo  | Uso normal       | Comunicación cifrada por HTTPS                                    | 100% tráfico por HTTPS                  |

#### 5.5.4 Accesibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-012  | Usuario final         | Acceso multiplataforma        | Sistema completo  | Diferentes dispositivos | Accesible desde PC, tablet y móvil con diseño responsivo      | Compatible con navegadores modernos      |
| EC-013  | Usuario final         | Accesibilidad web             | Sistema completo  | Uso normal       | Cumple WCAG 2.1 AA, contraste, fuente ajustable, lectores pantalla| Cumplimiento WCAG 2.1 AA                |

#### 5.5.5 Usabilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-014  | Usuario final         | Interacción                   | Interfaz gráfica  | Uso normal       | Interfaz intuitiva, navegación sencilla                           | 90% usuarios completan tareas sin ayuda |
| EC-015  | Institución           | Identidad visual              | Interfaz gráfica  | Uso normal       | Respeta identidad visual institucional                            | Uso de logo y colores oficiales         |
| EC-016  | Usuario final         | Idioma                        | Sistema completo  | Uso normal       | Todo el sistema en español                                        | 100% interfaz y mensajes en español     |
| EC-017  | Usuario final         | Error                         | Sistema completo  | Uso normal       | Mensajes de error claros y orientados al usuario                   | Mensajes específicos y sugerencias      |

#### 5.5.6 Mantenibilidad

| ID      | Fuente                | Estímulo                      | Artefacto         | Ambiente         | Respuesta                                                        | Medida de la Respuesta                  |
|---------|-----------------------|-------------------------------|-------------------|------------------|-------------------------------------------------------------------|-----------------------------------------|
| EC-018  | Desarrollador         | Solicitud de modificación     | Código fuente     | Desarrollo       | Código limpio, documentado y buenas prácticas                     | Cambios menores ≤ 2 horas               |

#### 5.5.7 Exportación y Confirmación

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