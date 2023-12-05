from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from personas.models import Administrativo
from .models import CriterioCalidadPrograma, Acreditacion

# Create your views here.
@login_required()
@permission_required('calidad.view_criteriodecalidad')
def criteriosPrograma(request):
    data = {}
    administrativo = Administrativo.objects.get(email=request.user.email)
    criterios_rc = CriterioCalidadPrograma.objects.filter(programa=administrativo.programa, criterio__tipoCriterio='RC').order_by('estado')
    criterios_ac = CriterioCalidadPrograma.objects.filter(programa=administrativo.programa, criterio__tipoCriterio='AC').order_by('estado')
    data["rc"] = criterios_rc
    data["ac"] = criterios_ac
    return render(request, "criterios.html", context=data)


class CriterioDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = CriterioCalidadPrograma
    template_name = 'criterio_detail.html'
    permission_required = 'calidad.view_criteriodecalidad'
    context_object_name = 'criterio'


class CriterioUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = CriterioCalidadPrograma
    fields = ['responsable', 'estado']
    context_object_name = 'criterio'
    template_name = 'criterio_form.html'
    permission_required = 'calidad.change_criteriodecalidad'


class AcreditacionProgramaListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Acreditacion
    template_name = 'acreditaciones_programa.html'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        return (Acreditacion.objects.filter(programa=administrativo.programa).order_by('-fechaVencimiento'))


class AcreditacionDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Acreditacion
    template_name = 'acreditacion_detail.html'
    permission_required = 'calidad.view_acreditacion'
    context_object_name = 'acreditacion'


class AcreditacionUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Acreditacion
    fields = ['tipoAcreditacion', 'numResolucion', 'fechaObtencion', 'fechaVencimiento', 'estado']
    template_name = 'acreditacion_form.html'
    permission_required = 'calidad.view_acreditacion'
    context_object_name = 'acreditacion'
