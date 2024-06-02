from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Propuesta

# Create your views here.

def homePage(request):
    tema = ""
    filtrar = "1"
    if request.GET:
        if request.user.is_authenticated:
            filtrar = request.GET['filtrar']
        else:
            tema = request.GET['tema']
    else:
        if request.user.is_authenticated:
            filtrar = "1"
        else:
            filtrar = "0"

    if filtrar == "2":
        tabla = Propuesta.objects.all().filter(profesor='').values()
    elif filtrar == "1" and tema == "":
        tabla = Propuesta.objects.all().values()
    elif filtrar == "1":
        tabla = Propuesta.objects.all().filter(tema=tema).values()
    else:
        tabla = Propuesta.objects.all().exclude(profesor='').values()

    datalist = Propuesta.objects.values_list("tema")

    data = {
        "tabla": tabla,
        "datalist": datalist
    }
    
    return render(request, 'core/base.html', data)

def nueva_propuesta(request):
    if (request.POST):
        # Capturo datos del formulario
        nombre = request.POST['Proyecto']
        nombreEstudiante = request.user.first_name + ' ' + request.user.last_name
        tema = request.POST['Tema']
        descripcion = request.POST['Descripcion']

    # validaciones de reglas de negocio

    # Construir y cargar el objeto con los datos del form
    propuesta = Propuesta()
    propuesta.nombre = nombre
    propuesta.estudiante = nombreEstudiante
    propuesta.tema = tema
    propuesta.descripcion = descripcion

    # Guardar en la base de datos
    propuesta.save()

    return redirect(homePage)

def editar_propuesta(request):
    if (request.GET):
        # Capturo datos del formulario
        propuestaId = request.GET['id']
        nombre = request.GET['Proyecto']
        nombreEstudiante = request.GET['nombreEstudiante']
        tema = request.GET['Tema']
        descripcion = request.GET['Descripcion']

    # validaciones de reglas de negocio
    usuario_actual = request.user.first_name + ' ' + request.user.last_name
    if usuario_actual != nombreEstudiante:
        return render(request, "core/noAutorizado.html")

    # Construir y cargar el objeto con los datos del form
    data = Propuesta.objects.filter(id=propuestaId)[0]
    data.nombre = nombre
    data.estudiante = nombreEstudiante
    data.tema = tema
    data.descripcion = descripcion

    # Guardar en la base de datos
    data.save()

    return redirect(homePage)


def apoyar(request):
    if (request.GET):
        idPropuesta = request.GET['namePropuesta']
    
    data = Propuesta.objects.filter(id=idPropuesta)[0]
    data.profesor = request.user.first_name + ' ' + request.user.last_name
    data.save()

    return redirect(homePage)
    #return render(request, 'core/base.html')


def logging(request):
    if (request.POST):
        usuario = request.POST['usuario']
        password = request.POST['password']

    user = authenticate(request, username=usuario, password=password)
    if user is not None:
        login(request, user)

    return redirect(homePage)

def loggingOut(request):
    logout(request)
    return redirect(homePage)