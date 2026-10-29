from django import forms

from .models import Comentario


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["tipo", "zona", "nombre", "texto"]
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej: Juan", "autocomplete": "given-name"}),
            "texto": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Ej: Hoy el agua estaba de otro color cerca de la orilla.",
            }),
        }
        error_messages = {
            "tipo": {"required": "Toca un dibujo para decir qué viste."},
            "zona": {"required": "Toca el lugar donde lo viste."},
            "nombre": {"required": "Escribe tu nombre."},
        }
