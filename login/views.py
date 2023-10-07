from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def sesion(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        usuario = request.POST['usuario']
        password = request.POST['password']
        user  = authenticate(request, username = usuario, password = password )
        if user is None:
            return render(request,'login.html',{
                "error":"Usuario y contraseña incorrecto","flag":True
            })
        else:
            login(request,user)
            return redirect('indexDashboard')
        
def cerrar_sesion(request):
    logout(request)
    return redirect('login')
        
