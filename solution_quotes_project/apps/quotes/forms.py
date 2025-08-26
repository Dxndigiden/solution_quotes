from django import forms

from .models import Quote


class QuoteForm(forms.ModelForm):
    """Форма для создания и редактирования цитаты."""

    class Meta:
        model = Quote
        fields = ["text", "source", "weight"]
        labels = {
            "text": "Текст",
            "source": "Источник",
            "weight": "Вес",
        }
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Введите цитату",
                    "class": "form-control",
                }
            ),
            "source": forms.TextInput(
                attrs={
                    "placeholder": "Источник: фильм, книга...",
                    "class": "form-control",
                }
            ),
            "weight": forms.NumberInput(
                attrs={"min": 1, "max": 7, "class": "form-control"}
            ),
        }

    def clean_weight(self):
        """Проверяет, что вес цитаты в нужном диапазоне."""
        quote_weight = self.cleaned_data.get("weight")
        if quote_weight < 1:
            raise forms.ValidationError(
                "Вес цитаты должен быть не меньше 1."
            )
        if quote_weight > 7:
            raise forms.ValidationError(
                "Вес цитаты должен быть не больше 7."
            )
        return quote_weight
