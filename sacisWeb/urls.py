from django.urls import path
from sacisWeb import views
from django.conf import settings
from django.conf.urls.static import static
from personas.views import UsersListView
from calidad.views import AcreditacionProgramaListView

urlpatterns = [
    path('', views.home, name="Home"),
    path('contacto/', views.contacto, name="Contacto"),
    path('login/', views.signin, name="Login"),
    path('logout/', views.signout, name="Logout"),
    path('board/', views.board, name="Board"),
    path('actividades/', views.actividades , name="Actividades"),
    path('calidad/', AcreditacionProgramaListView.as_view() , name="Calidad"),
    path('direccion/', UsersListView.as_view() , name="Direccion"),
    path('perfil/', views.myPerfil , name="MiPerfil"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
