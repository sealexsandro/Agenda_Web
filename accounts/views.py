from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    # usuario que vem do html name= usuario
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Bem vindo.')
        return redirect('dashboard')




def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    # messages.success(request, 'Olá meu Rei')
    # print(request.POST)
    if request.method != 'POST':
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    repetir_senha = request.POST.get('repetir_senha')

    if not nome or not sobrenome or not email or not usuario or not senha or not repetir_senha:
        messages.error(request, 'Nenhum campo pode ser vazio.')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter mais de 6 caracteres.')
        return render(request, 'accounts/register.html')

    if len(senha) < 6:
        messages.error(request, 'Senha precisa ter mais de 6 caracteres.')
        return render(request, 'accounts/register.html')

    if senha != repetir_senha:
        messages.error(request, 'Senhas devem ser iguais.')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'E-mail inválido.')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe.')
        return render(request, 'accounts/register.html')
    if User.objects.filter(email=email).exists():
        messages.error(request, 'E-mail já está cadastrado.')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Contato Salvo. Faça login com o contato salvo.')
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha,first_name= nome,
                                    last_name= sobrenome)
    user.save()
    return redirect('login')

@login_required(redirect_field_name='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
