from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Administrativo


class RegisterForm(UserCreationForm):
    administrativo = forms.ModelChoiceField(queryset=Administrativo.objects.all(), empty_label="----------", required=True,
                                                label="Administrativo")
    grupo = forms.ModelChoiceField(queryset=Group.objects.all().exclude(name='Direccion'), empty_label="----------", required=True,
                                                label="Grupo")

    def __init__(self, *args, **kwargs):
        filter_param = kwargs.pop('filter_param', None)
        super().__init__(*args, **kwargs)
        qset = Administrativo.objects.filter(programa=filter_param)
        self.fields['administrativo'].queryset = qset

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_email(self):
        email_field = self.cleaned_data['email']

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        elif Administrativo.objects.filter(email=email_field).aexists():
            pass

        return email_field
