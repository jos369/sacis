from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormularioContacto
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from personas.models import Administrativo
from academia.models import Programa
from calidad.models import CriterioDeCalidad, Acreditacion
from actividades.models import Planeacion, Actividad

# Create your views here.


def home(request):
    return render(request, "index.html")


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombreUsuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")
            usuario = authenticate(username=nombreUsuario, password=contra)
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request, "Su nombre de usuario o contraseña no coinciden. Inténtalo de nuevo")
        else:
            messages.error(request, "Información incorrecta")

    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


@login_required()
def signout(request):
    logout(request)

    return redirect('Home')


@login_required
def board(request):
    myBoard = {"error": ""}
    try:
        administrativo = Administrativo.objects.get(email=request.user.email)
        programa = Programa.objects.get(id=administrativo.programa_id)
        registro = Acreditacion.objects.filter(programa_id=programa.id).filter(tipoAcreditacion="RC").latest("fechaObtencion")
        altaCalidad = Acreditacion.objects.filter(programa_id=programa.id).filter(tipoAcreditacion="AC").latest("fechaObtencion")
        criterios = CriterioDeCalidad.objects.values("nombre").distinct()
        planes = Planeacion.objects.filter(programa=programa)[:3]
        actSpontaneas = programa.actividad_set.filter(planeacion=None)
        myBoard = {
            "url": programa.url,
            "administrativo": administrativo,
            "programa": programa,
            "registro": registro,
            "alta": altaCalidad,
            "criterios": criterios,
            "actSpontaneas": actSpontaneas,
            "planes": {},
        }
        if registro.exists():
            myBoard["registro"] = registro
        else:
            myBoard["registro"] = ""

        if altaCalidad.exists():
            myBoard["alta"] = altaCalidad
        else:
            myBoard["alta"] = "Sin Acreditación"

        for plan in planes:
            myBoard.get('planes').update({'planid': {'plan': plan, 'acts': Actividad.objects.filter(planeacion=plan)}})

        return render(request, "board.html", context=myBoard)
    except Exception as e:
        return render(request, "board.html", context=myBoard)


def contacto(request):
    if request.method == "POST":
        formulario_contacto = FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            nombre = formulario_contacto.cleaned_data.get("nombre")
            email = formulario_contacto.cleaned_data.get("email")
            telefono = formulario_contacto.cleaned_data.get("telefono")
            mensaje = formulario_contacto.cleaned_data.get("mensaje")
            correo = EmailMessage("Mensaje de Contacto desde Web SACIS",
                                  "El usuario de nombre {} manifiesta:\n\n{}\n"
                                  "Adicionalmente, proporciona los siguientes datos para su contacto:\nemail: {}\nteléfono: {}"
                                  "\n\nEste correo corresponde a un soporte de su contacto con SACIS."
                                  .format(nombre, mensaje, email, telefono),
                                  "sacis-info@udes.com.co", [email], ["sacis@udes.com.co"])
            try:
                correo.send()
                return render(request, "contact.html", {"error": "success"})
            except:
                return render(request, "contact.html", {"error": "error"})

    return render(request, "contact.html")


@login_required
def actividades(request):
    return render(request, "actividades.html")


@login_required
def myPerfil(request):
    return render(request, "perfil.html")
