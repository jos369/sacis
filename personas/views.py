from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Estudiante, Administrativo
from django.contrib.auth.decorators import login_required, permission_required
from .forms import RegisterForm

# Create your views here.


class RegisterView(View, PermissionRequiredMixin, LoginRequiredMixin):

    permission_required = 'auth.add_user'

    def get(self, request):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        filter_param = administrativo.programa
        data = {
            'form': RegisterForm(filter_param=filter_param)
        }
        return render(request, 'register.html', data)

    def post(self, request):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        user_creation_form = RegisterForm(data=request.POST, filter_param=administrativo.programa)
        if user_creation_form.is_valid():
            # user_creation_form.save()
            user_new = user_creation_form.save(commit=False)
            administrativo_new = user_creation_form.cleaned_data['administrativo']
            user_new.email = administrativo_new.email
            user_new.first_name = administrativo_new.nombres
            user_new.last_name = administrativo_new.apellidos
            user_new.groups.add(user_creation_form.cleaned_data['grupo'])
            user_new.save()

            return redirect('Registro')
        data = {
            'form': user_creation_form
        }
        return render(request, 'register.html', data)


class UsersListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    template_name = 'users_list.html'
    permission_required = 'auth.view_user'

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        programa = Administrativo.objects.filter(programa=administrativo.programa)
        correos = []
        for adm in programa:
            correos.append(adm.email)
        return User.objects.filter(email__in=correos)


class UserDetailView(generic.DetailView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_det'
    permission_required = 'auth.view_user'


class UserUpdateView(generic.UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    fields = ['email', 'username', 'password', 'is_active']
    context_object_name = 'user_det'
    permission_required = 'auth.change_user'
    template_name = 'user_form.html'


class EstudianteProgramaListView(generic.ListView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Estudiante
    template_name = 'estudiantes_programa.html'
    paginate_by = 20

    def get_queryset(self):
        administrativo = Administrativo.objects.get(email=self.request.user.email)
        return (Estudiante.objects.filter(programa=administrativo.programa).order_by('codigo'))


@login_required
def EstudianteDetailView(request, estudiante_id):
    administrativo = Administrativo.objects.get(email=request.user.email)
    estudiante = get_object_or_404(Estudiante, programa=administrativo.programa, id=estudiante_id)
    data = {
        "estudiante": estudiante,
        }
    return  render(request, "estudiante_detail.html", context=data)


class EstudianteCreate(generic.edit.CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Estudiante
    fields = ['codigo', 'nombres', 'apellidos', 'tipoDocIdentidad', 'numDocIdentidad', 'email', 'semestre', 'promedio',
              'activo', 'graduado', 'programa']
    permission_required = 'personas.add_estudiante'
    success_url = reverse('Estudiantes')


class EstudianteUpdate(PermissionRequiredMixin, generic.edit.UpdateView):
    model = Estudiante
    fields = ['codigo', 'nombres', 'apellidos', 'tipoDocIdentidad', 'numDocIdentidad', 'email', 'semestre', 'promedio',
              'activo', 'graduado', 'programa']
    permission_required = 'personas.change_estudiante'
