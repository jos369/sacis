from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Planeacion, Actividad, Evidencia
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from personas.models import Administrativo

# Create your views here.

class PlaneacionProgramaListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Planeacion
    template_name = 'planeacion_programa.html'
    paginate_by = 10

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        return {
            Planeacion.objects.filter(programa=administrativo.programa).order_by('-fechaInicio')
        }


class PlaneacionDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Planeacion
    template_name = 'planeacion_detail.html'
    permission_required = 'sctividades.view_planeacion'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        queryset = super().get_queryset()
        return queryset.filter(programa=administrativo.programa)


class PlaneacionCreateView(generic.edit.CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Planeacion
    fields = ['periodicidad', 'fechaInicio', 'fechaFin', 'estado', 'programa']
    permission_required = 'actividades.add_planeacion'
    success_url = reverse('Planes')


class PlaneacionUpdateView(generic.edit.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Planeacion
    fields = ['periodicidad', 'fechaInicio', 'fechaFin', 'estado', 'programa']
    template_name = 'planeacion_form.html'
    permission_required = 'actividades.change_planeacion'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        queryset = super().get_queryset()
        return queryset.filter(programa=administrativo.programa)


class PlaneacionDeleteView(generic.edit.DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Planeacion
    success_url = reverse_lazy('Planes')
    permission_required = 'actividades.delete_planeacion'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("Planeacion-delete", kwargs={"pk": self.object.pk})
            )


class ActividadProgramaListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Actividad
    template_name = 'actividades_programa.html'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        return (Actividad.objects.filter(programas__in=[administrativo.programa]).order_by('-fechaIniProgramada'))


class ActividadDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Actividad
    template_name = 'actividad_detail.html'
    context_object_name = 'actividad'
    permission_required = 'actividades.view_actividad'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        queryset = super().get_queryset()
        return queryset.filter(programas__in=[administrativo.programa])


class ActividadUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Actividad
    fields = ['periodicidad', 'fechaInicio', 'fechaFin', 'estado']
    template_name = 'actividad_form.html'
    permission_required = 'actividades.change_actividad'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        queryset = super().get_queryset()
        return queryset.filter(programas__in=[administrativo.programa])


class ActividadCreate(generic.edit.CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Actividad
    fields = ['periodicidad', 'fechaInicio', 'fechaFin', 'estado', 'programa']
    permission_required = 'actividades.add_actividad'
    success_url = reverse('Actividades')


class EvidenciaActividadListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Evidencia
    template_name = 'evidencias_actividad.html'
    permission_required = 'actividades.view_evidencia'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        return (Evidencia.objects.filter())


class EvidenciaDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model =  Evidencia
    template_name = 'evidencia_detail.html'
    permission_required = 'actividades.view_evidencia'
    context_object_name = 'evidencia'


class EvidenciaUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Evidencia
    fields = []
    template_name = 'evidencia_form.html'
    permission_required = 'actividades.change_evidencia'