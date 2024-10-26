# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Professor, Aluno, PaiMae, Serie, Materia, Mensagem, AlunoMateria
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
import json

def criar_professor_view(request):
    if request.method == 'POST':
        identificador = request.POST.get('identificador')
        nome = request.POST.get('nome')
        series_ids = request.POST.getlist('series')
        materias_ids = request.POST.getlist('materias')

        # Verifica se o identificador já existe
        if User.objects.filter(username=identificador).exists():
            return render(request, 'usuarios/criar_professor.html', {
                'error': 'Identificador já existe. Por favor, escolha outro.',
                'series': Serie.objects.all(),
                'materias': Materia.objects.all()
            })

        user = User.objects.create_user(username=identificador, password='senha_temporaria')
        professor = Professor.objects.create(
            identificador=identificador,
            nome=nome,
            user=user
        )

        series = Serie.objects.filter(id__in=series_ids)
        materias = Materia.objects.filter(id__in=materias_ids)
        professor.series.set(series)
        professor.materias.set(materias)

        return redirect('home')

    series = Serie.objects.all()
    materias = Materia.objects.all()
    return render(request, 'usuarios/criar_professor.html', {'series': series, 'materias': materias})



def get_professores(request):
    serie_id = request.GET.get('serie_id')
    if serie_id:
        serie = Serie.objects.get(id=serie_id)
        professores = serie.professores.all()
        professores_data = [{'id': professor.id, 'nome': professor.nome} for professor in professores]
        return JsonResponse({'professores': professores_data})
    return JsonResponse({'professores': []})


def criar_aluno(request):
    if request.method == 'POST':
        identificador = request.POST['identificador']
        nome = request.POST['nome']
        idade = request.POST['idade']
        serie_id = request.POST['serie']
        pai_nome = request.POST['pai_nome']  # Nome do responsável

        # Verifica se o identificador já existe
        if User.objects.filter(username=identificador).exists():
            # Adicione uma mensagem de erro ou outra lógica para lidar com o conflito de identificadores
            return render(request, 'usuarios/criar_aluno.html', {
                'error': 'Identificador já existe. Por favor, escolha outro.'
            })

        user = User.objects.create_user(username=identificador, password='senha_temporaria')
        pai_user = User.objects.create_user(username=f'{identificador}_pai', password='senha_temporaria')
        pai_mae = PaiMae.objects.create(user=pai_user, nome=pai_nome)

        aluno = Aluno.objects.create(
            user=user,
            identificador=identificador,
            nome=nome,
            idade=idade,
            serie_id=serie_id,
            pai_mae=pai_mae
        )

        return redirect('home')

    series = Serie.objects.all()
    professores = Professor.objects.all()  # Ajuste conforme necessário para listar os professores
    return render(request, 'usuarios/criar_aluno.html', {'series': series, 'professores': professores})


def mensagens(request):
    if request.method == 'POST':
        Mensagem.objects.create(
            remetente=request.user.paimae,
            destinatario=request.POST['destinatario'],  # Você precisará de lógica para pegar o professor correto
            conteudo=request.POST['mensagem'],
        )
    mensagens = Mensagem.objects.filter(destinatario=request.user.paimae)  # Para mostrar as mensagens recebidas 
    return render(request, 'usuarios/mensagens.html', {'mensagens': mensagens})

def buscar_materias(request):
    serie_id = request.GET.get('serie_id')
    materias = Materia.objects.filter(serie_id=serie_id)
    materias_data = [{'id': materia.id, 'nome': materia.nome} for materia in materias]
    return JsonResponse({'materias': materias_data})


def get_materias(request):
    serie_id = request.GET.get('serie_id')
    if serie_id:
        materias = Materia.objects.filter(serie_id=serie_id)
        materias_data = [{'id': materia.id, 'nome': materia.nome} for materia in materias]
        return JsonResponse({'materias': materias_data})
    return JsonResponse({'materias': []})

def series_professor(request):
    # Verifica se o usuário está autenticado
    if request.user.is_authenticated:
        try:
            # Verifica se o usuário é professor
            professor = request.user.professor
            series = Serie.objects.filter(professores=professor)
            return render(request, 'usuarios/series_professor.html', {'series': series})
        except Professor.DoesNotExist:
            # Se não é professor, redireciona ou mostra uma mensagem de erro
            return redirect('home')
    else:
        return redirect('login')



def get_alunos_por_serie(request):
    serie_id = request.GET.get('serie_id')
    alunos = Aluno.objects.filter(serie_id=serie_id)
    
    alunos_data = []
    for aluno in alunos:
        alunos_data.append({
            'id': aluno.id,
            'nome': aluno.nome,
            'nota_1': aluno.nota_1bimestre,
            'nota_2': aluno.nota_2bimestre,
            'nota_3': aluno.nota_3bimestre,
            'nota_4': aluno.nota_4bimestre,
        })
    
    return JsonResponse({'alunos': alunos_data})



def alunos_por_serie(request, serie_id):
    serie = get_object_or_404(Serie, id=serie_id)
    alunos = Aluno.objects.filter(serie=serie)

    if request.method == 'POST':
        for aluno in alunos:
            aluno.nota_1 = request.POST.get(f'nota_1_{aluno.id}', aluno.nota_1)
            aluno.nota_2 = request.POST.get(f'nota_2_{aluno.id}', aluno.nota_2)
            aluno.nota_3 = request.POST.get(f'nota_3_{aluno.id}', aluno.nota_3)
            aluno.nota_4 = request.POST.get(f'nota_4_{aluno.id}', aluno.nota_4)
            aluno.save()

        return redirect('series_professor')  # Redireciona de volta para a lista de séries

    return render(request, 'alunos_por_serie.html', {'serie': serie, 'alunos': alunos})


def salvar_nota(request, aluno_id):
    if request.method == "POST":
        aluno = Aluno.objects.get(id=aluno_id)
        nota = request.POST['nota']
        # Aqui você pode salvar a nota em um campo específico do aluno ou em um modelo de notas
        aluno.nota = nota  # Exemplo
        aluno.save()
    return redirect('alunos_serie', serie_id=aluno.serie.id)


@login_required
def mensagens(request):
    if request.method == "POST":
        mensagem_texto = request.POST.get("mensagem")
        if mensagem_texto:
            Mensagem.objects.create(
                autor=request.user,
                texto=mensagem_texto,
                data_envio=timezone.now()
            )
        return redirect('mensagens')  # Redireciona para limpar o campo

    mensagens = Mensagem.objects.all().order_by('data_envio')
    context = {'mensagens': mensagens}
    return render(request, 'mensagens.html', context)

@login_required
def notas(request):
    try:
        # Obter o aluno associado ao usuário logado
        aluno = request.user.aluno
        
        # Debug prints
        print(f"Aluno encontrado: {aluno.nome}")
        
        # Buscar todas as notas do aluno
        notas = AlunoMateria.objects.filter(aluno=aluno)
        print(f"Notas encontradas: {notas.count()}")
        
        context = {
            'aluno': aluno,
            'notas': notas,
        }
        return render(request, 'notas.html', context)
    except Aluno.DoesNotExist:
        context = {
            'mensagem_erro': 'Usuário não está associado a nenhum aluno.'
        }
        return render(request, 'notas.html', context)

@csrf_exempt
def save_notas(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aluno_id = data.get('aluno_id')
            materia_id = data.get('materia_id')
            
            aluno = get_object_or_404(Aluno, id=aluno_id)
            materia = get_object_or_404(Materia, id=materia_id)
            
            # Verifica se o professor tem permissão para alterar notas desta matéria
            if not request.user.professor.materias.filter(id=materia_id).exists():
                return JsonResponse({
                    'success': False, 
                    'error': 'Professor não tem permissão para esta matéria'
                })
            
            # Atualiza as notas
            aluno.nota_1bimestre = data.get('nota_1bimestre', aluno.nota_1bimestre)
            aluno.nota_2bimestre = data.get('nota_2bimestre', aluno.nota_2bimestre)
            aluno.nota_3bimestre = data.get('nota_3bimestre', aluno.nota_3bimestre)
            aluno.nota_4bimestre = data.get('nota_4bimestre', aluno.nota_4bimestre)
            aluno.save()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})


def notas_view(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    notas = AlunoMateria.objects.filter(aluno=Aluno)  # Filtrando as notas do aluno

    # Caso haja uma mensagem de erro
    mensagem_erro = None
    if not notas.exists():
        mensagem_erro = "Nenhuma nota cadastrada para este aluno."

    return render(request, 'notas_aluno.html', {
            'aluno': Aluno,
            'notas': notas,
            'mensagem_erro': mensagem_erro,
})
