from django.contrib import admin
from django.urls import path, include
from escolarize import views
from django.contrib.auth import views as auth_views
from usuarios import views as views_usuarios

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    path('notas/', views.notas, name='notas'),
    path('historico/', views.historico, name='historico'),
    path('criar_professor/', views_usuarios.criar_professor_view , name='criar_professor'),
    path('criar_aluno/', views_usuarios.criar_aluno, name='criar_aluno'),
    path('buscar_materias/', views_usuarios.buscar_materias, name='buscar_materias'),
    path('get_materias/', views_usuarios.get_materias, name='get_materias'),
    path('series_professor/', views_usuarios.series_professor, name='series_professor'),
    path('series_professor/<int:serie_id>/alunos/', views_usuarios.alunos_por_serie, name='alunos_por_serie'),
    path('get_alunos_por_serie/', views_usuarios.get_alunos_por_serie, name='get_alunos_por_serie'),
    path('salvar_nota/<int:aluno_id>/', views_usuarios.salvar_nota, name='salvar_nota'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('get_professores/', views_usuarios.get_professores, name='get_professores'),
    path('get_materias/', views_usuarios.get_materias, name='get_materias'),
    path('save_notas/', views_usuarios.save_notas, name='save_notas'),
    path('mensagens/', views_usuarios.mensagens, name='mensagens'),
    path('notas/', views_usuarios.notas, name='notas'),
]



