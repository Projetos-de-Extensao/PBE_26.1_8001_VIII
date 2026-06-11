from rest_framework.permissions import BasePermission


class IsEstudante(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'estudante_profile')
        )


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'professor_profile')
        )


class IsCoordenador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'coordenador_profile')
        )


class IsSolicitacaoOwnerOrStaffProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if hasattr(user, 'coordenador_profile') or hasattr(user, 'professor_profile'):
            return True

        if not hasattr(user, 'estudante_profile'):
            return False

        estudante = user.estudante_profile

        if hasattr(obj, 'estudante'):
            return obj.estudante_id == estudante.id

        if hasattr(obj, 'solicitacao'):
            return obj.solicitacao.estudante_id == estudante.id

        return False
