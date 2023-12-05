from django.contrib import admin
from .models import Universidad, Programa, Dependencia

# Register your models here.

admin.site.register(Universidad)
admin.site.register(Dependencia)
admin.site.register(Programa)
