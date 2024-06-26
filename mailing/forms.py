from django import forms
from mailing.models import Mailing
from client.forms import StyleFormMixin


class MailingForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания/редактирования рассылки"""

    class Meta:
        model = Mailing
        exclude = ('created_by',)


class MailingManagerForm(StyleFormMixin, forms.ModelForm):
    """Форма для менеджера для изменения статуса рассылки """

    class Meta:
        model = Mailing
        fields = ('status', )