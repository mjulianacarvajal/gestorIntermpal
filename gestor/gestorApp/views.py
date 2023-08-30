from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required

import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import RegistrarUsuario, ActualizarPerfil,ActualizarContrasena,GuardarEmpresa, GuardarSede, GuardarBus, GuardarProgramado, GuardarDespachado,SalidaDespachado
from .models import Empresa, Sede, Bus, Programado, Despachado

from datetime import datetime
from django.db.models import Q

context = {
    'page_title' : 'Visor de Viajes',
}

def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Usuario o Contraseña: Incorrecta"
        else:
            resp['msg'] = "Usuario o Contraseña: Incorrecta"
    return HttpResponse(json.dumps(resp),content_type='application/json')


def inicio(request):
    context['page_title'] = 'Inicio'
    context['buses'] = Bus.objects.count()
    context['empresas'] = Empresa.objects.count()
    context['upcoming_trip'] = Programado.objects.filter(estado= 1, programado__gt = datetime.today()).count()
    return render(request, 'inicio.html',context)


def logoutuser(request):
    logout(request)
    return redirect('/')

@login_required
def registrarUsuario(request):
    user = request.user
    context['page_title'] = "Registrar Usuario"
    if request.method == 'POST':
        data = request.POST
        form = RegistrarUsuario(data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            loginUser = authenticate(username= username, password = pwd)
            login(request, loginUser)
            return redirect('inicio')
        else:
            context['reg_form'] = form

    return render(request,'registro.html',context)

@login_required
def perfil(request):
    context['page_title'] = 'Pelfil del Usuario'
    return render(request, 'perfil.html',context)

@login_required
def actualizarPerfil(request):
    context['page_title'] = 'Actualizar Perfil'
    user = User.objects.get(id=request.user.id)
    if not request.method == 'POST':
        form = ActualizarPerfil(instance=user)
        context['form'] = form
        print(form)
    else:
        form = ActualizarPerfil(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect("perfil")
        else:
            context['form'] = form

    return render(request, 'gestion_perfil.html', context)


@login_required
def actualizarContrasena(request):
    context['page_title'] = "Actualizar Contraseña"
    if request.method == 'POST':
        form = ActualizarContrasena(user = request.user, data= request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contraseña actualizada correctamente")
            update_session_auth_hash(request, form.user)
            return redirect("perfil")
        else:
            context['form'] = form
    else:
        form = ActualizarContrasena(request.POST)
        context['form'] = form
    return render(request,'actualizar_contrasena.html',context)

@login_required
def empresa(request):
    context['page_title'] = "Empresa"
    empresas = Empresa.objects.all()
    context['empresas'] = empresas

    return render(request, 'empresa.html', context)

@login_required
def guardar_empresa(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            empresa = Empresa.objects.get(pk=request.POST['id'])
        else:
            empresa = None
        if empresa is None:
            form = GuardarEmpresa(request.POST)
        else:
            form = GuardarEmpresa(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'La Empresa se ha guardado exitosamente.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No se han guardado datos.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def adm_empresa(request, pk=None):
    context['page_title'] = "Gestión de Empresas"
    if not pk is None:
        empresa = Empresa.objects.get(id=pk)
        context['empresa'] = empresa
    else:
        context['empresa'] = {}

    return render(request, 'adm_empresa.html', context)


@login_required
def eliminar_empresa(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            empresa = Empresa.objects.get(id=request.POST['id'])
            empresa.delete()
            messages.success(request, 'La Empresa se ha eliminado exitosamente.')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'La Empresa no se pudo eliminar'
            print(err)

    else:
        resp['msg'] = 'La Empresa no se pudo eliminar'

    return HttpResponse(json.dumps(resp), content_type="application/json")



# Location

@login_required
def sede(request):
    semaforo = {
        '1': 'bg-primary',
        '2': 'bg-secondary',
        '3': 'bg-success'
    }
    context['page_title'] = "Sedes"
    sedes = Sede.objects.all()
    context['sedes'] = sedes
    context['semaforo'] = semaforo
    return render(request, 'sede.html', context)



@login_required
def guardar_sede(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            sede = Sede.objects.get(pk=request.POST['id'])
        else:
            sede = None
        if sede is None:
            form = GuardarSede(request.POST)
        else:
            form = GuardarSede(request.POST, instance=sede)
        if form.is_valid():
            form.save()
            messages.success(request, 'La Sede se ha guardado exitosamente.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No se han guardado datos.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def adm_sede(request, pk=None):
    context['page_title'] = "Gestion de Sedes"
    if not pk is None:
        sede = Sede.objects.get(id=pk)
        context['sede'] = sede
    else:
        context['sede'] = {}

    return render(request, 'adm_sede.html', context)


@login_required
def eliminar_sede(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            sede = Sede.objects.get(id=request.POST['id'])
            sede.delete()
            messages.success(request, 'La Sede se ha eliminado exitosamente')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'La Sede no se pudo eliminar'
            print(err)

    else:
        resp['msg'] = 'La Sede no se pudo eliminar'

    return HttpResponse(json.dumps(resp), content_type="application/json")



# bus
@login_required
def bus(request):
    context['page_title'] = "Buses"
    buses = Bus.objects.all()
    context['buses'] = buses

    return render(request, 'bus.html', context)


@login_required
def guardar_bus(request):
    resp = {'status': 'failed', 'msg': ''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            bus = Bus.objects.get(pk=request.POST['id'])
        else:
            bus = None
        if bus is None:
            form = GuardarBus(request.POST)
        else:
            form = GuardarBus(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            messages.success(request, 'El Bus se ha guardado exitosamente')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No se han guardado datos.'
    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def adm_bus(request, pk=None):
    context['page_title'] = " Manage Bus"
    empresas = Empresa.objects.filter(estado=1).all()
    context['empresas'] = empresas
    if not pk is None:
        bus = Bus.objects.get(id=pk)
        context['bus'] = bus
    else:
        context['bus'] = {}

    return render(request, 'manage_bus.html', context)


@login_required
def eliminar_bus(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            bus = Bus.objects.get(id=request.POST['id'])
            bus.delete()
            messages.success(request, 'Bus has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'bus has failed to delete'
            print(err)

    else:
        resp['msg'] = 'bus has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")



@login_required
def programado(request):
    context['page_title'] = "Progamación"
    programados = Programado.objects.all()
    context['programados'] = programados

    return render(request, 'programado.html', context)


@login_required
def guardar_programado(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            programado = Programado.objects.get(pk=request.POST['id'])
        else:
            programado = None
        if programado is None:
            form = GuardarProgramado(request.POST)
        else:
            form = GuardarProgramado(request.POST, instance=programado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule has been saved successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

@login_required
def adm_programado(request, pk=None):
    context['page_title'] = "Manage Schedule"
    buses = Bus.objects.filter(estado=1).all()
    sedes = Sede.objects.filter(tipo=1).all()
    context['buses'] = buses
    context['sedes'] = sedes
    if not pk is None:
        programado = Programado.objects.get(id = pk)
        context['programado'] = programado
    else:
        context['programado'] = {}

    return render(request, 'adm_programado.html', context)

@login_required
def eliminar_programado(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            programado = Programado.objects.get(id=request.POST['id'])
            programado.delete()
            messages.success(request, 'Schedule has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'schedule has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Schedule has failed  to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")



# find trips va cuando se meten los datos a  ST-->
# scheduled Trips

def viajes_programados(request):
    if not request.method == 'POST':
        context['page_title'] = "Viajes Programados"
        programados = Programado.objects.filter(estado=1, programado__gt=datetime.now()).all()
        context['programados'] = programados
        context['is_searched'] = False
        context['data'] = {}
    else:
        context['page_title'] = "Search Result | Scheduled Trips"
        context['is_searched'] = True
        date = datetime.strptime(request.POST['date'],"%Y-%m-%d").date()
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')
        origen = Sede.objects.get(id=request.POST['origen'])
        destino = Sede.objects.get(id=request.POST['destino'])
        programados = Programado.objects.filter(Q(estado=1) & Q(programado__year=year) & Q(programado__month=month) & Q(programado__day=day) & Q(Q(origen=origen) | Q(destino=destino))).all()
        context['programados'] = programados
        context['data'] = {'date':date,'origen': origen, 'destino': destino}

    return render(request, 'viajes_programados.html', context)

#bookings  book_despacho
def adm_despachado(request, schedPK=None, pk=None):
    context['page_title'] = "Despacho"
    context['schedPK'] = schedPK
    if not schedPK is None:
        programado = Programado.objects.get(id = schedPK)
        context['programado'] = programado
    else:
        context['programado'] = {}
    if not pk is None:
        despacho = Despachado.objects.get(id = pk)
        context['despacho'] = despacho
    else:
        context['despacho'] = {}

    return render(request, 'manage_book.html', context)

#save_booking
def save_despachado(request):
    resp = {'status':'failed','msg':''}
    if request.method == 'POST':
        if (request.POST['id']).isnumeric():
            despachado = Despachado.objects.get(pk=request.POST['id'])
        else:
            despachado = None
        if despachado is None:
            form = GuardarDespachado(request.POST)
        else:
            form = GuardarDespachado(request.POST, instance= despachado)
        if form.is_valid():
            form.save()
            if despachado is None:
                despachado = Despachado.objects.last()
                messages.success(request, f'Booking has been saved successfully. Your Booking Refderence Code is: <b>{despachado.codigo}</b>', extra_tags = 'stay')
            else:
                messages.success(request, f'<b>{despachado.codigo}</b> Booking has been updated successfully.')
            resp['status'] = 'success'
        else:
            for fields in form:
                for error in fields.errors:
                    resp['msg'] += str(error + "<br>")
    else:
        resp['msg'] = 'No data has been sent.'
    return HttpResponse(json.dumps(resp), content_type = 'application/json')

def despachados(request):
    context['page_title'] = "Viajes Despachados"
    despachados = Despachado.objects.all()
    context['despachados'] = despachados

    return render(request, 'despachados.html', context)

@login_required
def view_despachado(request,pk=None):
    if pk is None:
        messages.error(request, "Unkown Booking ID")
        return redirect('booking-page')
    else:
        context['page_title'] = 'View Despachados'
        context['despachado'] = Despachado.objects.get(id = pk)
        return render(request, 'view_booked.html', context)


def buscar_programado(request):
    context['page_title'] = 'Find Trip Schedule'
    context['sedes'] = Sede.objects.filter(tipo__gt = 0).all
    today = datetime.today().strftime("%Y-%m-%d")
    context['today'] = today
    return render(request, 'buscar_viaje.html', context)

#booked
@login_required
def pay_despachado(request):
    resp = {'status': 'failed', 'msg': ''}
    if not request.method == 'POST':
        resp['msg'] = "Unknown Booked ID"
    else:
        despachado = Despachado.objects.get(id=request.POST['id'])
        form = SalidaDespachado(request.POST,instance=despachado)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{despachado.codigo}</b> has been paid successfully", extra_tags='stay')
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + "<br>")

    return HttpResponse(json.dumps(resp), content_type='application/json')


@login_required
def SalidaDespachado(request):
    resp = {'status': 'failed', 'msg': ''}
    if not request.method == 'POST':
        resp['msg'] = "Unknown Booked ID"
    else:
        programado = Programado.objects.get(id=request.POST['id'])
        form = SalidaDespachado(request.POST, instance=programado)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{programado.codigo}</b> has been paid successfully", extra_tags='stay')
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + "<br>")

    return HttpResponse(json.dumps(resp), content_type='application/json')


# usuario
@login_required
def delete_despachado(request):
    resp = {'status': 'failed', 'msg': ''}

    if request.method == 'POST':
        try:
            despachado = Despachado.objects.get(id=request.POST['id'])
            codigo = despachado.codigo
            despachado.delete()
            messages.success(request, f'[<b>{codigo}</b>] Booking has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'booking has failed to delete'
            print(err)

    else:
        resp['msg'] = 'booking has failed to delete'

    return HttpResponse(json.dumps(resp), content_type="application/json")


"""
#book=despacho

def manage_programado(request, schedPK=None, pk=None):
    context['page_title'] = "Manage Booking"
    context['schedPK'] = schedPK
    if not schedPK is None:
        programado = Schedule.objects.get(id = schedPK)
        context['programado'] = programado
    else:
        context['programado'] = {}
    if not pk is None:
        despacho = Despachado.objects.get(id = pk)
        context['despacho'] = despacho
    else:
        context['despacho'] = {}

    return render(request, 'manage_book.html', context)

@login_required
def delete_programado(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            programado = Programado.objects.get(id = request.POST['id'])
            programado.delete()
            messages.success(request, 'Schedule has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'schedule has failed to delete'
            print(err)

    else:
        resp['msg'] = 'Schedule has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")

def find_trip(request):
    context['page_title'] = 'Find Trip Schedule'
    context['sedes'] = Sede.objects.filter(tipo__gt = 0).all
    today = datetime.today().strftime("%Y-%m-%d")
    context['today'] = today
    return render(request, 'find_trip.html', context)
    
gestion_despacho     
    
@login_required
def SalidaDespachado(request):
    resp = {'status':'failed','msg':''}
    if not request.method == 'POST':
        resp['msg'] = "Unknown Booked ID"
    else:
        programado = Programado.objects.get(id= request.POST['id'])
        form = SalidaDespachado(request.POST, instance=despachado)
        if form.is_valid():
            form.save()
            messages.success(request, f"<b>{despachado.codigo}</b> has been paid successfully", extra_tags='stay')
            resp['status'] = 'success'
        else:
            for field in form:
                for error in field.errors:
                    resp['msg'] += str(error + "<br>")
    
    return HttpResponse(json.dumps(resp),content_type = 'application/json')   

#usuario 
@login_required
def delete_despachado(request):
    resp = {'status':'failed', 'msg':''}

    if request.method == 'POST':
        try:
            despachado = Despachado.objects.get(id = request.POST['id'])
            codigo = despachado.codigo
            despachado.delete()
            messages.success(request, f'[<b>{codigo}</b>] Booking has been deleted successfully')
            resp['status'] = 'success'
        except Exception as err:
            resp['msg'] = 'booking has failed to delete'
            print(err)

    else:
        resp['msg'] = 'booking has failed to delete'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")  


def find_trip(request):
    context['page_title'] = 'Find Trip Schedule'
    context['sedes'] = Sede.objects.filter(estado__gt = 0).all
    today = datetime.today().strftime("%Y-%m-%d")
    context['today'] = today
    return render(request, 'find_trip.html', context)




###crear variable e iterar para que no sea el mismo destino

def consulta_objetos(request):
    objeto_seleccionado_id = request.session.get('objeto_seleccionado_id')  # Obtenemos el ID del objeto seleccionado de la sesión

    # Realizamos la consulta excluyendo el objeto seleccionado
    objetos = Objeto .objects.all()
    if objeto_seleccionado_id:
        objetos = objetos.exclude(id=objeto_seleccionado_id)

    return render(request, 'consulta.html', {'objetos': objetos})
###




"""