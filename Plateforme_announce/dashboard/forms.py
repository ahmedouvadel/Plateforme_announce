from django import forms
from announces.models import Categories, Annonce, AnnonceStatus

class CategoryForm(forms.ModelForm):
    titre = forms.CharField(
        max_length=50,
        label="Nom de la catégorie",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Entrez un nom de catégorie'
        })
    )

    class Meta:
        model = Categories
        fields = ['titre']

    def clean_titre(self):
        """
        Vérifie si la catégorie existe déjà avant de l'enregistrer.
        """
        titre = self.cleaned_data.get('titre').strip()  # Supprime les espaces inutiles
        if Categories.objects.filter(titre__iexact=titre).exists():  # Ignorer la casse
            raise forms.ValidationError("⚠️ Cette catégorie existe déjà.")
        return titre


class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'prix', 'image', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Titre de l\'annonce'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Description de l\'annonce',
                'rows': 4
            }),
            'prix': forms.NumberInput(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Prix'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
            'categorie': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg'}),
        }

    def save(self, commit=True, user=None):
        annonce = super().save(commit=False)
        annonce.statut = AnnonceStatus.EN_ATTENTE  # ✅ Toujours en attente par défaut

        if user:
            annonce.user = user  # ✅ Associe l'annonce à l'utilisateur connecté

        if commit:
            annonce.save()
        return annonce
