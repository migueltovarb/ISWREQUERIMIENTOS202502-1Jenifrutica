from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def admin_required(view_func):
    """Decorador para verificar que el usuario sea administrador"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión para acceder')
            return redirect('login')
        if request.user.rol != 'administrador':
            messages.error(request, 'No tiene permisos de administrador')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def profesor_required(view_func):
    """Decorador para verificar que el usuario sea profesor"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión para acceder')
            return redirect('login')
        if request.user.rol not in ['profesor', 'administrador']:
            messages.error(request, 'No tiene permisos de profesor')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

def estudiante_required(view_func):
    """Decorador para verificar que el usuario sea estudiante"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debe iniciar sesión para acceder')
            return redirect('login')
        if request.user.rol != 'estudiante':
            messages.error(request, 'No tiene permisos de estudiante')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
