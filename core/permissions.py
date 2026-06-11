from rest_framework.permissions import BasePermission


def has_estudante_profile(user):
    return user and user.is_authenticated and hasattr(user, 'estudante_profile')


def has_professor_profile(user):
    return user and user.is_authenticated and hasattr(user, 'professor_profile')


def has_coordenador_profile(user):
    return user and user.is_authenticated and hasattr(user, 'coordenador_profile')


class IsEstudante(BasePermission):
    def has_permission(self, request, view):
        return has_estudante_profile(request.user)


class IsProfessor(BasePermission):
    def has_permission(self, request, view):
        return has_professor_profile(request.user)


class IsCoordenador(BasePermission):
    def has_permission(self, request, view):
        return has_coordenador_profile(request.user)


class SolicitacaoEstagioActionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if view.action in ['list', 'retrieve']:
            return (
                has_estudante_profile(user)
                or has_professor_profile(user)
                or has_coordenador_profile(user)
            )

        if view.action == 'create':
            return has_estudante_profile(user)

        if view.action in ['update', 'partial_update', 'destroy']:
            return has_coordenador_profile(user)

        return False


class DocumentoActionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if view.action in ['list', 'retrieve']:
            return (
                has_estudante_profile(user)
                or has_professor_profile(user)
                or has_coordenador_profile(user)
            )

        if view.action == 'create':
            return has_estudante_profile(user)

        if view.action in ['update', 'partial_update', 'destroy']:
            return has_coordenador_profile(user)

        return False


class PendenciaActionPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if view.action in ['list', 'retrieve']:
            return (
                has_estudante_profile(user)
                or has_professor_profile(user)
                or has_coordenador_profile(user)
            )

        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            return has_coordenador_profile(user)

        return False


class IsSolicitacaoOwnerOrStaffProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if has_coordenador_profile(user) or has_professor_profile(user):
            return True

        if not has_estudante_profile(user):
            return False

        estudante = user.estudante_profile

        if hasattr(obj, 'estudante'):
            return obj.estudante_id == estudante.id

        if hasattr(obj, 'solicitacao'):
            return obj.solicitacao.estudante_id == estudante.id

        return False
