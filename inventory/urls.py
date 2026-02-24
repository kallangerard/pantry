from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.SKUListView.as_view(), name="sku-list"),
    path("new/", views.SKUCreateView.as_view(), name="sku-create"),
    path("<int:pk>/edit/", views.SKUUpdateView.as_view(), name="sku-update"),
    path("<int:pk>/delete/", views.SKUDeleteView.as_view(), name="sku-delete"),
]
