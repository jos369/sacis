from django.urls import path
from . import views


urlpatterns = [
    path('criterios', views.criteriosPrograma, name='Criterios'),
    path('criterio/<int:pk>', views.CriterioDetailView.as_view(), name='Criterio-detail'),
    path('criterio/<int:pk>/update', views.CriterioUpdateView.as_view(), name='Criterio-update'),
    path('acreditacion/<int:pk>', views.AcreditacionDetailView.as_view(), name='Acreditacion-detail'),
    path('acreditacion/<int:pk>/update', views.AcreditacionUpdateView.as_view(), name='Acreditacion-update'),

]