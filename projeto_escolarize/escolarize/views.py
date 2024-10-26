from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
import logging

logger = logging.getLogger(__name__)

@login_required
def login_page(request):
    return render(request, 'registration/login.html')


@login_required
def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            logger.info(f'User {user.username} logged in successfully.')
            return redirect(resolve_url('home'))
        else:
            logger.warning(f'Login failed for user {username}.')
            return render(request, 'registration/login.html', {'error': 'Usuário ou senha incorretos'})
    return render(request, 'registration/login.html')



@login_required
def notas(request):
    # busca as notas do aluno a partir do banco de dados
    notas = []  # Exemplo: buscar notas do aluno logado
    return render(request, 'notas.html', {'notas': notas})

@login_required
def historico(request):
    # busca o histórico do aluno
    historico = {}  # Exemplo: buscar histórico do aluno logado
    return render(request, 'historico.html', {'historico': historico})

def user_logout(request):
    logout(request)
    return redirect('login')
