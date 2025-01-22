from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
       Форма для создания или редактирования заказа.

       Используется для ввода данных о номере стола, списке предметов и статусе заказа.
    """
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']
        widgets = {
            'items': forms.Textarea(attrs={'rows': 3})
        }
