from django.shortcuts import render, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import *
import bcrypt
from datetime import date

from .models import User

# Create your views here.
def login(request):
    return render(request, 'login.html')
def registrar(request):
    return render(request, 'registro.html')

def inicio(request):
    usuario = User.objects.filter(email=request.POST['email'])
    errores = User.objects.validar_login(request.POST, usuario)

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return redirect('/')
    else:
        request.session['user_id'] = usuario[0].id
        return redirect('home/')

def registro(request):
    #validacion de parametros
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, msg in errors.items():
            messages.error(request, msg)
        return redirect('/registrar')

    else:
        #encriptar password
        password = User.objects.encriptar(request.POST['password'])
        decode_hash_pw = password.decode('utf-8')
        #crear usuario
        if request.POST['rol'] == '1':
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=1,
            )
        else:
            user = User.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                email=request.POST['email'],
                password=decode_hash_pw,
                rol=2,
            )
        request.session['user_id'] = user.id
    return redirect('home/')

def logout(request):
    request.session.flush()
    return redirect('/')

def add (request):
    Appointment.objects.create(     # crea la nueva cita
        task= request.POST['task_name'], 
        date=request.POST['task_date'], 
        status=request.POST['task_status'],
        usuario=request.POST['user_id'] #crea la relacion del usuario con la cita
    )
    return render(request, 'home.html')

def edit (request):
    update =Appointment.objects.get(request.POST['task_id'])   #recibe el id de la tarea desde el input hidden
    update.task= request.POST['new_task']
    update.date= request.POST['new_date']
    update.status= request.POST['new_status']
    update.save()     #guarda los cambios
    return render(request, 'home.html')

def delete(request):
    Appointment.objects.filter(id=request.POST["task_id"]).delete()
    return redirect('/')

def appointments(request):
    appointments=Appointment.filter(date__range=["1900-01-01",date.today()])
    past_appointments= Appointment.filter(date__range=[date.today(),"2050-01-01"])
    context={
        'appointment_list' : appointments,
        'past_appointments' : past_appointments
    }
    render(request, 'home.html', context)