from django.db import models


class SKU(models.Model):
    """A Stock Keeping Unit – a single type of pantry item."""

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    barcode = models.CharField(max_length=100, blank=True)
    unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="Unit of measurement, e.g. g, ml, each",
    )
    category = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "SKU"
        verbose_name_plural = "SKUs"

    def __str__(self) -> str:
        return self.name
