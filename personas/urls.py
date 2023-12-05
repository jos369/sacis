from django.urls import path
from personas import views


urlpatterns = [
    path('estudiante/registrar', views.EstudianteCreate.as_view(), name="Estudiante-create"),
    path('estudiantes', views.EstudianteProgramaListView.as_view(), name="Estudiantes"),
    path('estudiante/<int:estudiante_id>', views.EstudianteDetailView, name="Estudiante-detail"),
    path('usuario/registrar', views.RegisterView.as_view(), name="Registro"),
    path('usuario/<int:pk>', views.UserDetailView.as_view(), name="Usuario-detail"),
    path('usuario/<int:pk>/update', views.UserUpdateView.as_view(), name="Usuario-update"),
]
