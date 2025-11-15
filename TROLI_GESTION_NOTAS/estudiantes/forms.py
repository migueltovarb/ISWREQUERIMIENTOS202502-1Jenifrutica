from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import FieldError, ValidationError
from django.core.validators import validate_email
import re
from .models import Usuario, Curso, Inscripcion, ReporteAcademico

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2', 'rol')

class UsuarioAdminForm(forms.ModelForm):
    """Formulario para crear/editar usuarios con criterios de aceptación."""
    DOC_CHOICES = (
        ('CC', 'Cédula de ciudadanía'),
        ('TI', 'Tarjeta de identidad'),
        ('RC', 'Registro civil'),
        ('PA', 'Pasaporte'),
        ('CE', 'Cédula de extranjería'),
    )

    # Campos adicionales requeridos
    tipo_documento = forms.ChoiceField(
        choices=DOC_CHOICES,
        required=True,
        label='Tipo de documento',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    numero_documento = forms.CharField(
        required=True,
        min_length=6,
        max_length=15,
        label='Número de documento',
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': 15})
    )

    # Passwords (confirmación)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Contraseña',
        help_text='8-20 caracteres, incluir mayúscula, minúscula, número y carácter especial.'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirmar contraseña'
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'rol', 'telefono', 'activo']
        labels = {
            'username': 'Usuario',
            'email': 'Email',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'rol': 'Rol',
            'telefono': 'Teléfono',
            'activo': 'Usuario Activo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 20}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 100}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 10}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Estado como radio (activo/inactivo)
        self.fields['activo'].widget = forms.RadioSelect(
            choices=((True, 'Activo'), (False, 'Inactivo'))
        )

        # En creación, exigir contraseña y confirmación
        if not self.instance or not self.instance.pk:
            self.fields['password'].required = True
            self.fields['confirm_password'].required = True

        # Orden de campos en el formulario (muestra primero doc y contacto)
        order = [
            'username', 'email', 'first_name', 'last_name', 'rol', 'telefono',
            'tipo_documento', 'numero_documento',
            'password', 'confirm_password', 'activo'
        ]
        try:
            self.order_fields(order)
        except Exception:
            pass

    def clean_username(self):
        username = (self.cleaned_data.get('username') or '').strip()
        # Usuario: 4 a 20 caracteres, obligatorio y único
        if not (4 <= len(username) <= 20):
            raise ValidationError('El usuario debe tener entre 4 y 20 caracteres.')
        qs = Usuario.objects.filter(username__iexact=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un usuario con ese nombre de usuario.')
        return username

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        if not email:
            raise ValidationError('El email es obligatorio.')
        validate_email(email)
        qs = Usuario.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un usuario con ese correo electrónico.')
        return email

    def clean(self):
        cleaned = super().clean()

        # Nombre completo (Nombre + Apellido): mínimo 3 y máximo 100
        fn = (cleaned.get('first_name') or '').strip()
        ln = (cleaned.get('last_name') or '').strip()
        full_len = len((fn + ' ' + ln).strip())
        if full_len < 3 or full_len > 100:
            raise ValidationError('El nombre completo debe tener entre 3 y 100 caracteres.')

        # Rol obligatorio
        if not cleaned.get('rol'):
            raise ValidationError('El rol es obligatorio.')

        # Teléfono: exactamente 10 dígitos
        tel = (cleaned.get('telefono') or '').strip()
        if not re.fullmatch(r'^\d{10}$', tel or ''):
            raise ValidationError('El teléfono debe contener exactamente 10 dígitos.')

        # Tipo/Número documento obligatorios
        tipo_doc = cleaned.get('tipo_documento')
        num_doc = (cleaned.get('numero_documento') or '').strip()
        if not (tipo_doc and num_doc):
            raise ValidationError('Tipo y número de documento son obligatorios.')
        # 6-15, alfanumérico y - . _
        if not re.fullmatch(r'^[A-Za-z0-9\-\._]{6,15}$', num_doc):
            raise ValidationError('El número de documento debe tener entre 6 y 15 caracteres alfanuméricos.')

        # Unicidad número_documento si existe en el modelo
        try:
            if hasattr(Usuario, '_meta') and any(f.name == 'numero_documento' for f in Usuario._meta.fields):
                qs_doc = Usuario.objects.filter(numero_documento__iexact=num_doc)
                if self.instance and self.instance.pk:
                    qs_doc = qs_doc.exclude(pk=self.instance.pk)
                if qs_doc.exists():
                    raise ValidationError('Ya existe un usuario con ese número de documento.')
        except FieldError:
            pass

        # Contraseña y confirmación (en creación obligatoria; en edición si se provee)
        pwd = cleaned.get('password') or ''
        pwd2 = cleaned.get('confirm_password') or ''
        creating = not self.instance or not self.instance.pk

        if creating or pwd or pwd2:
            if pwd != pwd2:
                raise ValidationError('Las contraseñas no coinciden.')
            if not (8 <= len(pwd) <= 20):
                raise ValidationError('La contraseña debe tener entre 8 y 20 caracteres.')
            if not re.search(r'[A-Z]', pwd):
                raise ValidationError('La contraseña debe incluir al menos una letra mayúscula.')
            if not re.search(r'[a-z]', pwd):
                raise ValidationError('La contraseña debe incluir al menos una letra minúscula.')
            if not re.search(r'\d', pwd):
                raise ValidationError('La contraseña debe incluir al menos un número.')
            if not re.search(r'[^A-Za-z0-9]', pwd):
                raise ValidationError('La contraseña debe incluir al menos un carácter especial.')

        return cleaned

    def save(self, commit=True):
        usuario: Usuario = super().save(commit=False)

        # Mapear documento si existe en el modelo
        tipo_doc = self.cleaned_data.get('tipo_documento')
        num_doc = self.cleaned_data.get('numero_documento')
        if hasattr(usuario, 'tipo_documento'):
            setattr(usuario, 'tipo_documento', tipo_doc)
        if hasattr(usuario, 'numero_documento'):
            setattr(usuario, 'numero_documento', num_doc)

        # Estado (radio)
        usuario.activo = self.cleaned_data.get('activo') in (True, 'True', 'true', '1', 1)

        # Contraseña
        pwd = self.cleaned_data.get('password')
        if pwd:
            usuario.set_password(pwd)

        if commit:
            usuario.save()
        return usuario

class CursoAdminForm(forms.ModelForm):
    """Formulario para crear/editar cursos desde el panel de administración"""
    class Meta:
        model = Curso
        fields = ['codigo', 'nombre', 'descripcion', 'creditos', 'profesor', 'activo']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'creditos': forms.NumberInput(attrs={'class': 'form-control'}),
            'profesor': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo profesores activos
        self.fields['profesor'].queryset = Usuario.objects.filter(rol='profesor', activo=True)

class InscripcionAdminForm(forms.ModelForm):
    """Formulario para crear inscripciones desde el panel de administración"""
    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'curso', 'activo']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estudiante'].queryset = Usuario.objects.filter(rol='estudiante', activo=True)
        self.fields['curso'].queryset = Curso.objects.filter(activo=True)

class ReporteAcademicoForm(forms.ModelForm):
    """Formulario para guardar reportes académicos"""
    class Meta:
        model = ReporteAcademico
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': 100,
                'placeholder': 'Ejemplo: Notas Semestre 1 2025'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'maxlength': 500,
                'placeholder': 'Descripción opcional del reporte...'
            }),
            'activo': forms.RadioSelect(choices=[(True, 'Activo'), (False, 'Inactivo')]),
        }
        labels = {
            'nombre': 'Nombre del Reporte',
            'descripcion': 'Descripción',
            'activo': 'Estado del Reporte',
        }
    
    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if not nombre:
            raise ValidationError('El nombre del reporte es obligatorio.')
        # Solo letras, números, espacios y guiones
        if not re.fullmatch(r'^[A-Za-z0-9\s\-]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras, números, espacios y guiones.')
        return nombre
