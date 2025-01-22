from django.test import TestCase
from .models import Order
from .forms import OrderForm
from django.urls import reverse


class OrderModelTest(TestCase):

    def test_calculate_total_price(self):
        """
        Тестирует корректность вычисления общей стоимости заказа.
        """
        items = [
            {'name': 'Burger', 'price': 10.99},
            {'name': 'Fries', 'price': 2.99}
        ]
        order = Order.objects.create(table_number=1, items=items, status='Paid')
        order.save()  # Сохраняем заказ, чтобы пересчитался total_price
        self.assertEqual(order.total_price, 13.98)  # Проверяем, что цена считается правильно

    def test_invalid_items_format(self):
        """
        Тестирует ошибку, если поле `items` не является списком словарей с ценами.
        """
        order = Order(table_number=1, items="Invalid format", status='Paid')
        with self.assertRaises(ValueError):
            order.save()  # Ожидаем исключение ValueError


class OrderViewsTest(TestCase):

    def test_order_list_view(self):
        """
        Тестирует представление списка заказов.
        """
        Order.objects.create(table_number=1, items=[{'name': 'Burger', 'price': 10.99}], status='Paid')
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Burger')  # Проверяем, что заказ отображается в списке

    def test_calculate_revenue_view(self):
        """
        Тестирует представление для подсчета выручки.
        """
        Order.objects.create(table_number=1, items=[{'name': 'Burger', 'price': 10.99}], status='Paid')
        Order.objects.create(table_number=2, items=[{'name': 'Fries', 'price': 2.99}], status='Paid')
        response = self.client.get(reverse('calculate_revenue'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '13.98')  # Проверяем, что выручка считается правильно

    def test_order_create_view(self):
        """
        Тестирует создание нового заказа.
        """
        data = {
            'table_number': 1,
            'items': [{'name': 'Burger', 'price': 10.99}],
            'status': 'Paid'
        }
        response = self.client.post(reverse('order_create'), data)
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после сохранения
        self.assertEqual(Order.objects.count(), 1)  # Проверяем, что заказ был сохранен

    def test_order_update_view(self):
        """
        Тестирует обновление существующего заказа.
        """
        order = Order.objects.create(table_number=1, items=[{'name': 'Burger', 'price': 10.99}], status='Paid')
        data = {
            'table_number': 1,
            'items': [{'name': 'Burger', 'price': 10.99}, {'name': 'Fries', 'price': 2.99}],
            'status': 'Paid'
        }
        response = self.client.post(reverse('order_update', args=[order.pk]), data)
        order.refresh_from_db()  # Обновляем заказ из базы данных
        self.assertEqual(order.total_price, 13.98)  # Проверяем, что цена обновилась

    def test_order_delete_view(self):
        """
        Тестирует удаление заказа.
        """
        order = Order.objects.create(table_number=1, items=[{'name': 'Burger', 'price': 10.99}], status='Paid')
        response = self.client.post(reverse('order_delete', args=[order.pk]))
        self.assertEqual(response.status_code, 302)  # Ожидаем редирект после удаления
        self.assertEqual(Order.objects.count(), 0)  # Проверяем, что заказ удален


class OrderFormTest(TestCase):

    def test_valid_form(self):
        """
        Тестирует корректную форму с правильными данными.
        """
        data = {
            'table_number': 1,
            'items': [{'name': 'Burger', 'price': 10.99}],
            'status': 'Paid'
        }
        form = OrderForm(data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма валидна

    def test_invalid_form(self):
        """
        Тестирует форму с некорректными данными (отсутствует поле 'items').
        """
        data = {
            'table_number': 1,
            'status': 'Paid'
        }
        form = OrderForm(data)
        self.assertFalse(form.is_valid())  # Форма должна быть невалидной
        self.assertIn('items', form.errors)  # Проверяем, что ошибка относится к полю 'items'
