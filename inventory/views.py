from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import SKU


class SKUListView(ListView):
    model = SKU
    template_name = "inventory/sku_list.html"
    context_object_name = "skus"


class SKUCreateView(CreateView):
    model = SKU
    fields = ["name", "description", "barcode", "unit", "category"]
    template_name = "inventory/sku_form.html"
    success_url = reverse_lazy("inventory:sku-list")


class SKUUpdateView(UpdateView):
    model = SKU
    fields = ["name", "description", "barcode", "unit", "category"]
    template_name = "inventory/sku_form.html"
    success_url = reverse_lazy("inventory:sku-list")


class SKUDeleteView(DeleteView):
    model = SKU
    template_name = "inventory/sku_confirm_delete.html"
    success_url = reverse_lazy("inventory:sku-list")
