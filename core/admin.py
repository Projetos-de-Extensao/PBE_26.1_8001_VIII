from django.contrib import admin
from .models import (
    Usuario,
    Estudante,
    Professor,
    Coordenador,
    EmpresaParceira,
    SolicitacaoEstagio,
    Documento,
    Pendencia
)

admin.site.register(Usuario)
admin.site.register(Estudante)
admin.site.register(Professor)
admin.site.register(Coordenador)
admin.site.register(EmpresaParceira)
admin.site.register(SolicitacaoEstagio)
admin.site.register(Documento)
admin.site.register(Pendencia)
# Register your models here.
