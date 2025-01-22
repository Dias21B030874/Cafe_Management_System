from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm
from django.db import models
from typing import Any, Dict
from .serializers import OrderSerializer
from rest_framework import viewsets


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#

def order_list(request: Any) -> Any:
    """
    Отображает список заказов с возможностью фильтрации по номеру стола.
    """
    query = request.GET.get('q', '')
    orders = Order.objects.all()
    if query:
        orders = orders.filter(
            models.Q(table_number__icontains=query) |
            models.Q(status__icontains=query)
        )
    return render(request, 'orders/order_list.html', {'orders': orders, 'query': query})


def calculate_revenue(request: Any) -> Any:
    """
    Вычисляет общий доход от всех заказов со статусом 'Paid'.
    """
    revenue = Order.objects.filter(status='Paid').aggregate(total=models.Sum('total_price'))['total'] or 0
    return render(request, 'orders/calculate_revenue.html', {'revenue': revenue})


def order_create(request: Any) -> Any:
    """
    Создает новый заказ.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})


def order_update(request: Any, pk: int) -> Any:
    """
    Обновляет данные существующего заказа.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'orders/order_form.html', {'form': form})


def order_delete(request: Any, pk: int) -> Any:
    """
    Удаляет заказ.
    """
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'orders/order_confirm_delete.html', {'order': order})
