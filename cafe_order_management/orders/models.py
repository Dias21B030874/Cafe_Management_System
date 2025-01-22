from django.db import models
from typing import List, Dict


class Order(models.Model):
    """
    Модель для хранения информации о заказах в ресторане.

    Поля:
    - id: Уникальный идентификатор заказа.
    - table_number: Номер стола, для которого сделан заказ.
    - items: Список предметов заказа, представленный в виде списка словарей.
    - total_price: Общая стоимость заказа.
    - status: Статус заказа (Pending, Ready, Paid).
    - created_at: Время создания заказа.
    - updated_at: Время последнего обновления заказа.
    """

    id = models.AutoField(primary_key=True)

    STATUS_CHOICES = [
        ('Pending', 'В ожидании'),
        ('Ready', 'Готово'),
        ('Paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    items = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs) -> None:
        if isinstance(self.items, list):
            self.total_price = sum(item['price'] for item in self.items if isinstance(item, dict) and 'price' in item)
        else:
            raise ValueError("The 'items' field must be a list of dictionaries with 'price' keys.")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта заказа.
        """
        return f"Заказ {self.id} для столика {self.table_number}"
