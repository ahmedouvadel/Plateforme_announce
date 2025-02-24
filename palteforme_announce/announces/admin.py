from django.contrib import admin
from .models import Annonce
from .models import Categories
from .models import AnnonceStatus


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('titre',)
admin.site.register(Categories)

class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'statut', 'is_paid', 'categorie')
    list_filter = ('statut', 'categorie', )
    search_fields = ('titre', 'description')
    actions = ['valider_annonce', 'rejeter_annonce']

    def valider_annonce(self, request, queryset):
        queryset.update(statut=AnnonceStatus.VALIDEE)
    valider_annonce.short_description = "Valider les annonces sélectionnées"

    def rejeter_annonce(self, request, queryset):
        queryset.update(statut=AnnonceStatus.REJETEE)
    rejeter_annonce.short_description = "Rejeter les annonces sélectionnées"
admin.site.register(Annonce)

