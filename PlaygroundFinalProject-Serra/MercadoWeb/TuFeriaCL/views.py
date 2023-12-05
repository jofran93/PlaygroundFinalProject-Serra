from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Item, Post,UserExtension
from .forms import ItemForm, PostForm, editperfilform, RegistrationForm, FormCambioPassword
from django.contrib import messages
from django.urls import reverse_lazy #<--------------------------------------
from django.views.generic.edit import UpdateView, DeleteView #<------------------------------
from django.contrib.auth.mixins import LoginRequiredMixin #<------------------------------
from django.contrib.auth.views import PasswordChangeView #<------------------------------
from django.contrib.auth.forms import AuthenticationForm
from .forms import ArticuloForm
from django.views.generic import ListView,CreateView





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()        
            return redirect('login')  # Redirige a la página de inicio de sesión después del registro
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_autentic(request):
    if request.method == 'GET':
        return render(request, 'login.html',{
            'form': AuthenticationForm
        })
    else:
        user= authenticate(request, username=request.POST["username"], password= request.POST["password"])
        if user is None:
            return render(request,"login.html",{
                "form": AuthenticationForm,
                "error": "Usuario o Contraseña Incorrecta"
            })
        else:
            login(request, user)
            user_extension,nuevo_userextension = UserExtension.objects.get_or_create(user=request.user)
            return redirect("dashboard")


def index_views(request):
    return render(request, 'index.html') #redirige a la pagina principal

def about(request):
    return render(request, 'about.html') # redirige a la pagina about

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html') # Redirige al Panel de usuario

@login_required
def dashboard_logout(request):
    logout(request)
    return redirect('index')  # URL para la página principal

@login_required
def editPerfil(request):
    if request.method == 'POST':
        formedit = editperfilform(request.POST, request.FILES)

        if formedit.is_valid():
            datos_perfil = formedit.cleaned_data

            request.user.email = datos_perfil['email']
            request.user.first_name = datos_perfil['first_name']
            request.user.last_name = datos_perfil['last_name']


            if datos_perfil['profile_picture'] == False:
                request.user.userextension.profile_picture = None
            elif datos_perfil['profile_picture'] != None:
                request.user.userextension.profile_picture = datos_perfil['profile_picture']

            request.user.userextension.phone_number = datos_perfil['phone_number']

            request.user.save()
            request.user.userextension.save()

            return redirect('profile')
    else:
        formedit = editperfilform(
            initial={
                'email' : request.user.email,
                'first_name' : request.user.first_name,
                'last_name' : request.user.last_name,
                'profile_picture' : request.user.userextension.profile_picture,
                'phone_number' :request.user.userextension.phone_number,
            }
        )
    return render(request, 'edit_perfil.html', { 'formedit' : formedit })

def profile(request):
    return render(request, 'profile.html')

class passwordedit(LoginRequiredMixin, PasswordChangeView):
    form_class = FormCambioPassword
    template_name='edit_password.html'
    success_url= reverse_lazy ('dashboard')
    

def item_list(request):
    
    items = Item.objects.all()
    return render(request, "item_list.html",{"items": items})
    

class item_listview(ListView):
    model= Item
    template_name = "item_list.html"
    context_object_name= "item"


class Itemupdateview(UpdateView):
    model= Item
    template_name="update_item.html"
    form_class = ItemForm
    success_url= reverse_lazy("item_list")

class Item_Delete(DeleteView):
    model=Item
    template_name= "delete_item.html"
    success_url= reverse_lazy("item_list")

def add_item(request):
    if request.method == "POST":
        formitem = ItemForm(request.POST, request.FILES)
        if formitem.is_valid():
            item = formitem.save()
            return redirect("item_list")
    else:
        formitem = ItemForm
    return render(request,"create_item.html",{"formitem": formitem})


