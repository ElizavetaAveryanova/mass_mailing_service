from django import forms
from client.models import Client


class StyleFormMixin:
    """Миксин стилизации формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания/редактирования клиента сервиса"""
    class Meta:
        model = Client
        exclude = ('created_by',)
