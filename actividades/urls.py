from django.urls import path
from . import views


urlpatterns = [
    path('actividad/<int:pk>', views.ActividadDetailView.as_view(), name="Actividad-detail"),
    path('actividad/<int:pk>/update', views.ActividadUpdateView.as_view(), name="Actividad-update"),
    path('planes', views.PlaneacionProgramaListView.as_view(), name="Planes"),
    path('planeacion/<int:pk>', views.PlaneacionDetailView.as_view(), name="Planeacion-detail"),
    path('actividad/<int:pk>/update', views.PlaneacionUpdateView.as_view(), name="Planeacion-update"),
    path('evidencias/<int:actividad>', views.EvidenciaActividadListView.as_view(), name="Evidencias"),
    path('evidencia/<int:pk>', views.EvidenciaDetailView.as_view(), name="Evidencia-detail"),
    path('evidencia/<int:pk>/update', views.EvidenciaUpdateView.as_view(), name="Evidencia-update"),
]