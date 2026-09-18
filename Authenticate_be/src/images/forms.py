# images/forms.py
from django import forms
from .models import Image
from .widgets import MultiFileWidget

class ImageAdminAddForm(forms.ModelForm):
    image_file = forms.ImageField(
        label="Fichiers image",
        widget=MultiFileWidget(attrs={"multiple": True}),
        required=False,  # important pour éviter l'erreur "No file was submitted"
        help_text="Sélectionnez un ou plusieurs fichiers. Un enregistrement sera créé par fichier.",
    )

    class Meta:
        model = Image
        fields = ("title", "image_file")
        help_texts = {
            "title": "Optionnel : servira de préfixe. Si vide, le titre = nom du fichier.",
        }

class MultipleFileField(forms.Field):
    widget = MultiFileWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def to_python(self, data):
        if not data:
            return []
        if isinstance(data, (list, tuple)):
            return list(data)
        return [data]

    def validate(self, value):
        super().validate(value)
        # Exemple : forcer au moins 1 fichier si required=True
        if self.required and not value:
            raise forms.ValidationError("Veuillez sélectionner au moins un fichier.")


class BatchImageUploadForm(forms.Form):
    files = MultipleFileField(
        label="Images",
        help_text="Sélectionnez une ou plusieurs images."
    )
    common_title_prefix = forms.CharField(
        label="Préfixe commun pour le titre",
        required=False, 
    )
