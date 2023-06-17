# Generated by Django 4.2 on 2023-06-09 19:51

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('full_name', models.CharField(blank=True, max_length=100, unique=True)),
                ('good_image', models.ImageField(blank=True, upload_to='images')),
                ('good_type', models.CharField(choices=[('GD', 'Goods'), ('RM', 'Raw materials'), ('SF', 'Semi-finished products'), ('PR', 'Products'), ('OS', 'Office supplies')], default='GD', max_length=2)),
                ('description', models.TextField(blank=True)),
                ('bar_code', models.CharField(blank=True, max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='PriceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_type', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('calculation', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='UoM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uom_short_name', models.CharField(max_length=10, unique=True)),
                ('uom_full_name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('price_date', models.DateTimeField(auto_now_add=True)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prices', to='im.good')),
                ('price_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='prices', to='im.pricetype')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsCharacteristics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characteristics_name', models.CharField(max_length=15)),
                ('characteristics_value', models.DecimalField(decimal_places=8, max_digits=15)),
                ('uom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='im.uom')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('category_parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subcategories', to='im.goodscategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='good',
            name='good_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='goods', to='im.goodscategory'),
        ),
    ]