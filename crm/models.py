import uuid
from django.db import models
from user.models import User
from im.models import Good


class OrderStatus(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    status_name = models.CharField(max_length=20, unique=True)
    users = models.ManyToManyField(User)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.status_name}'


class Order(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    order_number = models.CharField(max_length=15, blank=True, null=True)
    order_place_point = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=4, decimal_places=3)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='order_user')
    additional_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.order_number} {self.order_place_point}'


class StatusChange(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='status_change_orders')
    status_change_point = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='status_change_users')

    def __str__(self):
        return f'{self.status_change_point}'


class OrderLine(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_line_order')
    good = models.ForeignKey(Good, on_delete=models.PROTECT, related_name='order_line_good')
    quantity = models.DecimalField(max_digits=3, decimal_places=0)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.public_id} {self.order}'


class PostCompany(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PostOffice(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    post = models.ForeignKey(PostCompany, on_delete=models.PROTECT)
    zip = models.CharField(max_length=10)
    locality_type = models.CharField(max_length=15, blank=True, null=True)
    locality = models.CharField(max_length=35, blank=True, null=True)
    max_weight = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('zip', 'locality'),)

    def __str__(self):
        return f'{self.post} {self.zip} {self.locality}'


class OrderDestination(models.Model):
    public_id = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    post_office = models.ForeignKey(PostOffice, on_delete=models.PROTECT)
    region = models.CharField(max_length=15, blank=True, null=True)
    district = models.CharField(max_length=25, blank=True, null=True)
    street_type = models.CharField(max_length=35, blank=True, null=True)
    street = models.CharField(max_length=35, blank=True, null=True)
    building = models.CharField(max_length=7, blank=True, null=True)
    apartment = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return f'{self.post_office.__str__()}, {self.street_type}{self.street}, ' \
               f'{self.building} {self.apartment}'

