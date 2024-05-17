from rest_framework import permissions

class DynamicModelPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Permitir siempre a superusuarios
        if request.user and request.user.is_superuser:
            return True

        # Obtener el modelo asociado a la vista
        model_cls = view.queryset.model

        # Mapeo de acciones a permisos de Django
        perms_map = {
            'GET': f'view_{model_cls._meta.model_name}',
            'OPTIONS': f'view_{model_cls._meta.model_name}',
            'HEAD': f'view_{model_cls._meta.model_name}',
            'POST': f'add_{model_cls._meta.model_name}',
            'PUT': f'change_{model_cls._meta.model_name}',
            'PATCH': f'change_{model_cls._meta.model_name}',
            'DELETE': f'delete_{model_cls._meta.model_name}',
        }

        required_perm = perms_map.get(request.method)
        if not required_perm:
            return False  # Método HTTP no soportado

        return request.user.has_perm(f'{model_cls._meta.app_label}.{required_perm}')
