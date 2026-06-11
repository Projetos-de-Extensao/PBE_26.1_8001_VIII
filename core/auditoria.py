from .models import RegistroAuditoria


def registrar_auditoria(usuario, acao, recurso, objeto_id='', descricao=''):
    if usuario is not None and not usuario.is_authenticated:
        usuario = None

    return RegistroAuditoria.objects.create(
        usuario=usuario,
        acao=acao,
        recurso=recurso,
        objeto_id=str(objeto_id or ''),
        descricao=descricao,
    )
