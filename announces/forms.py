from django import forms
from announces.models import Categories, Annonce, AnnonceStatus

# Formulaire pour la catégorie
from django import forms
from announces.models import Categories

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['titre']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Nom de la catégorie'
            })
        }

    def clean_titre(self):
        titre = self.cleaned_data.get('titre')
        if Categories.objects.filter(titre=titre).exists():
            raise forms.ValidationError("Cette catégorie existe déjà.")
        return titre


# Formulaire pour l'annonce
class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre de l\'annonce'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Description de l\'annonce',
                'rows': 4
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prix'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, user=None, commit=True):
        annonce = super().save(commit=False)
        annonce.statut = AnnonceStatus.EN_ATTENTE  # ✅ Toujours en attente par défaut

        if user:  # ✅ Associe l'annonce à l'utilisateur connecté
            annonce.user = user

        if commit:
            annonce.save()
        return annonce

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie']  # Liste des champs du formulaire