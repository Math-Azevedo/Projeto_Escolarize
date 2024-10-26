from django.contrib import admin
from .models import Professor

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('user', )
    filter_horizontal = ('series', 'materias')  # Permitir múltipla seleção no Django Admin

admin.site.register(Professor, ProfessorAdmin)
