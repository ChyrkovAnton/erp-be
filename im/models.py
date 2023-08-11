from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import uuid


class GoodsCategory(MPTTModel):
    name = models.CharField(max_length=30)
    category_parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                                     related_name='subcategories')

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'category_parent'

    def __str__(self):
        return self.name


class UoM(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    uom_short_name = models.CharField(max_length=10, unique=True)
    uom_full_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.uom_full_name


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
    full_name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    good_image = models.ImageField(upload_to='images', blank=True, null=True)
    good_category = models.ForeignKey(GoodsCategory,
                                      on_delete=models.PROTECT,
                                      related_name='categories')
    good_type = models.CharField(max_length=2, choices=GOOD_TYPES_CHOICES, default='GD')
    description = models.TextField(blank=True, null=True)
    bar_code = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.name


class GoodCharacteristicType(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    characteristics_full_name = models.CharField(max_length=50,
                                                 verbose_name='Повна назва типу характеристики')
    characteristics_short_name = models.CharField(max_length=50, blank=True, null=True)
    priority = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)
    input_type = models.CharField(max_length=1, default=1)

    def __str__(self):
        return f'{self.characteristics_full_name}'


class GoodsCharacteristic(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    characteristics_type = models.ForeignKey(GoodCharacteristicType,
                                             on_delete=models.PROTECT,
                                             related_name='characteristic_types',
                                             default=1)
    good = models.ForeignKey(Good,
                             on_delete=models.PROTECT,
                             related_name='characteristics',
                             default=1)
    uom = models.ForeignKey(UoM, on_delete=models.PROTECT)
    characteristics_value = models.DecimalField(max_digits=15, decimal_places=8)


class PriceType(models.Model):
    price_type = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    calculation = models.CharField(max_length=250, blank=True, null=True)

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



