from django.shortcuts import render
from rest_framework import viewsets
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

from .serializers import (
    UsuarioSerializer,
    EstudanteSerializer,
    ProfessorSerializer,
    CoordenadorSerializer,
    EmpresaParceiraSerializer,
    SolicitacaoEstagioSerializer,
    DocumentoSerializer,
    PendenciaSerializer
)

# Create your views here.

from .models import ( Usuario, Estudante, Professor, Coordenador, EmpresaParceira, SolicitacaoEstagio, Documento)
from .serializers import ( UsuarioSerializer, EstudanteSerializer, ProfessorSerializer, CoordenadorSerializer, EmpresaParceiraSerializer, SolicitacaoEstagioSerializer, DocumentoSerializer)
def home(request):
    return render(request, 'home.html')
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
class EstudanteViewSet(viewsets.ModelViewSet):
    queryset = Estudante.objects.all()
    serializer_class = EstudanteSerializer
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
class CoordenadorViewSet(viewsets.ModelViewSet):
    queryset = Coordenador.objects.all()
    serializer_class = CoordenadorSerializer
class EmpresaParceiraViewSet(viewsets.ModelViewSet):    
    queryset = EmpresaParceira.objects.all()
    serializer_class = EmpresaParceiraSerializer
class SolicitacaoEstagioViewSet(viewsets.ModelViewSet):
    queryset = SolicitacaoEstagio.objects.all()
    serializer_class = SolicitacaoEstagioSerializer             
class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
class PendenciaViewSet(viewsets.ModelViewSet):
    queryset = Pendencia.objects.all()
    serializer_class = PendenciaSerializer

