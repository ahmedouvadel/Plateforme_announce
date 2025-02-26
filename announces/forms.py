from django import forms
from .models import Categories, Annonce, AnnonceStatus


# Form for Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['titre']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            })
        }

# Form for Annonce
class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie']  # Removed 'statut'
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

    def save(self, commit=True):
        # Automatically set statut to "En attente"
        annonce = super().save(commit=False)
        annonce.statut = AnnonceStatus.EN_ATTENTE  # Set status to "En attente"

        if commit:
            annonce.save()
        return annonce