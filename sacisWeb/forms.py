from django import forms

class FormularioContacto(forms.Form):
    nombre = forms.CharField(required=True)
    email = forms.CharField(required=True)
    telefono = forms.CharField()
    mensaje = forms.CharField()

