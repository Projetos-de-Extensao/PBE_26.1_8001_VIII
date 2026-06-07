from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import (
    Coordenador,
    Documento,
    EmpresaParceira,
    Estudante,
    Pendencia,
    Professor,
    SolicitacaoEstagio,
    Usuario,
)
from .permissions import IsCoordenador, IsEstudante, IsProfessor
from .serializers import (
    CoordenadorSerializer,
    DocumentoSerializer,
    EmpresaParceiraSerializer,
    EstudanteSerializer,
    PendenciaSerializer,
    ProfessorSerializer,
    SolicitacaoEstagioSerializer,
    UsuarioSerializer,
)

def home(request):
    return HttpResponse("API de Estágios Funcionando")

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]

class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.select_related('usuario').all()
    serializer_class = EstudanteSerializer
    permission_classes = [IsAuthenticated, IsEstudante]

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.select_related('usuario').all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAuthenticated, IsProfessor]

class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.select_related('usuario').all()
    serializer_class = CoordenadorSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]

class EmpresaParceiraViewSet(viewsets.ModelViewSet):
    queryset = EmpresaParceira.objects.all()
    serializer_class = EmpresaParceiraSerializer
    permission_classes = [IsAuthenticated, IsCoordenador]

class SolicitacaoEstagioViewSet(viewsets.ModelViewSet):
    queryset = SolicitacaoEstagio.objects.select_related(
        'estudante__usuario',
        'empresa',
    ).all()
    serializer_class = SolicitacaoEstagioSerializer
    permission_classes = [IsAuthenticated, IsEstudante | IsProfessor | IsCoordenador]

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.select_related(
        'solicitacao__estudante__usuario',
        'solicitacao__empresa',
    ).all()
    serializer_class = DocumentoSerializer
    permission_classes = [IsAuthenticated, IsEstudante | IsProfessor | IsCoordenador]

class PendenciaViewSet(viewsets.ModelViewSet):
    queryset = Pendencia.objects.select_related(
        'solicitacao__estudante__usuario',
        'solicitacao__empresa',
    ).all()
    serializer_class = PendenciaSerializer
    permission_classes = [IsAuthenticated, IsEstudante | IsProfessor | IsCoordenador]

