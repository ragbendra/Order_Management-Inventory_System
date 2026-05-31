from django.urls import path
from .views import CreateOrderView, CancelOrderView, OrderDetailView

app_name = 'orders'

urlpatterns = [
    path('', CreateOrderView.as_view(), name='create_order'),
    path('<int:pk>/cancel/', CancelOrderView.as_view(), name='cancel_order'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]
