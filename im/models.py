from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class GoodsCategory(MPTTModel):
    name = models.CharField(max_length=20, unique=True)
    category_parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'category_parent'

    def __str__(self):
        return self.name


class UoM(models.Model):
    uom_short_name = models.CharField(max_length=10, unique=True)
    uom_full_name = models.CharField(max_length=20, unique=True)


class GoodsCharacteristics(models.Model):
    characteristics_name = models.CharField(max_length=15)
    uom = models.ForeignKey(UoM, on_delete=models.PROTECT)
    characteristics_value = models.DecimalField(max_digits=15, decimal_places=8)


class Good(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    GOOD_TYPES_CHOICES = [
        ('GD', 'Goods'),
        ('RM', 'Raw materials'),
        ('SF', 'Semi-finished products'),
        ('PR', 'Products'),
        ('OS', 'Office supplies'),
    ]
    name = models.CharField(unique=True, max_length=50)
    full_name = models.CharField(unique=True, max_length=100, blank=True)
    good_image = models.ImageField(upload_to='images', blank=True)
    good_category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods')
    good_type = models.CharField(max_length=2, choices=GOOD_TYPES_CHOICES, default='GD')
    description = models.TextField(blank=True)
    bar_code = models.CharField(max_length=12, blank=True)

    def __str__(self):
        return self.name


class PriceType(models.Model):
    price_type = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True)
    calculation = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return self.price_type


class Price(models.Model):
    good = models.ForeignKey(Good, on_delete=models.PROTECT, related_name='prices')
    price_type = models.ForeignKey(PriceType, on_delete=models.PROTECT, related_name='prices')
    value = models.DecimalField(max_digits=8, decimal_places=2)
    price_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.good) + ' at ' + str(self.price_type) + ' on ' + str(self.price_date) + ' - ' + \
            str(self.value)



