

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserChangeForm

from django.contrib.auth.models import User

from .models import Empresa, Sede, Bus, Programado,Despachado
from datetime import datetime


class RegistrarUsuario(UserCreationForm):
    email = forms.EmailField(max_length=250, help_text="The email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class ActualizarPerfil(UserChangeForm):
    username = forms.CharField(max_length=250, help_text="The Username field is required.")
    email = forms.EmailField(max_length=250, help_text="The Email field is required.")
    first_name = forms.CharField(max_length=250, help_text="The First Name field is required.")
    last_name = forms.CharField(max_length=250, help_text="The Last Name field is required.")
    current_password = forms.CharField(max_length=250)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_current_password(self):
        if not self.instance.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError(f"Password is Incorrect")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"The {user.email} mail is already exists/taken")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(id=self.cleaned_data['id']).get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"The {user.username} mail is already exists/taken")


class ActualizarContrasena(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Contraseña Anterior")
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Nueva Constraseña")
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-sm rounded-0'}), label="Confirm New Password")

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class GuardarEmpresa(forms.ModelForm):
    nombre = forms.CharField(max_length="250")
    caracteristicas = forms.Textarea()
    estado = forms.ChoiceField(choices=[('1', 'Active'), ('2', 'Inactive')])

    class Meta:
        model = Empresa
        fields = ('nombre', 'caracteristicas', 'estado')

    def clean_name(self):
        id = self.instance.id if self.instance.id else 0
        nombre = self.cleaned_data['nombre']
        # print(int(id) > 0)
        # raise forms.ValidationError(f"{name} Category Already Exists.")
        try:
            if int(id) > 0:
                empresa = Empresa.objects.exclude(id=id).get(nombre=nombre)
            else:
                empresa = Empresa.objects.get(nombre=nombre)
        except:
            return nombre
            # raise forms.ValidationError(f"{name} Category Already Exists.")
        raise forms.ValidationError(f"{nombre} Category Already Exists.")


class GuardarSede(forms.ModelForm):
    sede = forms.CharField(max_length="250")
    tipo = forms.ChoiceField(choices=[('1','Terminal'),('2','Oficina'),('3','Paradero')])


    class Meta:
        model = Sede
        fields = ('sede', 'tipo',)

    def clean_sede(self):
        id = self.instance.id if self.instance.id else 0
        sede = self.cleaned_data['sede']
        # print(int(id) > 0)
        try:
            if int(id) > 0:
                loc = Sede.objects.exclude(id=id).get(sede=sede)
            else:
                loc = Sede.objects.get(sede=sede)
        except:
            return sede
            # raise forms.ValidationError(f"{location} Category Already Exists.")
        raise forms.ValidationError(f"{sede} Location Already Exists.")


class GuardarBus(forms.ModelForm):
    numero_bus = forms.CharField(max_length="250")
    empresa = forms.CharField(max_length="250")
    asientos = forms.CharField(max_length="2")
    estado = forms.ChoiceField(choices=[('1', 'Active'), ('2', 'Inactive')])

    class Meta:
        model = Bus
        fields = ('numero_bus', 'empresa', 'asientos', 'estado')

    def clean_empresa(self):
        id = self.cleaned_data['empresa']
        try:
            empresa = Empresa.objects.get(id=id)
            return empresa
        except:
            raise forms.ValidationError(f"Invalid Category Already Exists.")

    def clean_bus_number(self):
        id = self.instance.id if self.instance.id else 0
        numero_bus = self.cleaned_data['numero_bus']
        # print(int(id) > 0)
        try:
            if int(id) > 0:
                bus = Bus.objects.exclude(id=id).get(numero_bus=numero_bus)
            else:
                bus = Bus.objects.get(numero_bus=numero_bus)
        except:
            return numero_bus
            # raise forms.ValidationError(f"{bus_number} Category Already Exists.")
        raise forms.ValidationError(f"{numero_bus} bus Already Exists.")



class GuardarProgramado(forms.ModelForm):
    codigo = forms.CharField(max_length="250")
    bus = forms.CharField()
    origen = forms.CharField()
    destino = forms.CharField()
    precio = forms.IntegerField(min_value=0, max_value=999999)
    programado = forms.CharField()
    estado = forms.ChoiceField(choices=[('0','Cancelado'),('1','Activo')])

    class Meta:
        model = Programado
        fields = ('codigo', 'bus', 'origen', 'destino', 'precio', 'programado', 'estado')

    def clean_codigo(self):
        id = self.instance.id if self.instance.id else 0
        if id > 0:
            try:
                programado = Programado.objects.get(id=id)
                return programado.codigo
            except:
                codigo = ''
        else:
            codigo = ''
        pref = datetime.today().strftime('%Y%m%d')
        codigo = str(1).zfill(4)
        while True:
            prog = Programado.objects.filter(codigo=str(pref + codigo)).count()
            if prog > 0:
                codigo = str(int(codigo) + 1).zfill(4)
            else:
                codigo = str(pref + codigo)
                break
        return codigo

    def clean_bus(self):
        bus_id = self.cleaned_data['bus']

        try:
            bus = Bus.objects.get(id=bus_id)
            return bus
        except:
            raise forms.ValidationError("Bus is not recognized.")

    def clean_origen(self):
        sede_id = self.cleaned_data['origen']

        try:
            sede = Sede.objects.get(id=sede_id)
            return sede
        except:
            raise forms.ValidationError("Depart is not recognized.")

    def clean_destino(self):
        sede_id = self.cleaned_data['destino']

        try:
            sede = Sede.objects.get(id=sede_id)
            return sede
        except:
            raise forms.ValidationError("Destination is not recognized.")


class GuardarDespachado(forms.ModelForm):
    codigo = forms.CharField(max_length="250")
    programado = forms.CharField(max_length="250")
    nombre = forms.CharField(max_length="250")
    asientos = forms.CharField(max_length="250")

    class Meta:
        model = Despachado
        fields = ('codigo', 'programado', 'nombre', 'asientos')

    def clean_codigo(self):
        id = self.instance.id if self.instance.id else 0
        if id > 0:
            try:
                despachado = Despachado.objects.get(id=id)
                return despachado.codigo
            except:
                codigo = ''
        else:
            codigo = ''
        pref = datetime.today().strftime('%Y%m%d')
        codigo = str(1).zfill(4)
        while True:
            prog = Despachado.objects.filter(codigo=str(pref + codigo)).count()
            if prog > 0:
                codigo = str(int(codigo) + 1).zfill(4)
            else:
                codigo = str(pref + codigo)
                break
        print(codigo)
        return codigo

    def clean_progamado(self):
        programado_id = self.cleaned_data['programado']
        # print(int(id) > 0)
        try:
            prog = Programado.objects.get(id=programado_id)
            return prog
        except:
            raise forms.ValidationError(f"Trip Schedule is not recognized.")


class SalidaDespachado(forms.ModelForm):
    estado = forms.IntegerField()

    class Meta:
        model = Despachado
        fields = ('estado',)