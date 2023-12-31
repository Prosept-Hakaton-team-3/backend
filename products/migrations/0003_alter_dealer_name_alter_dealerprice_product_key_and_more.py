# Generated by Django 4.2.7 on 2023-12-04 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productdealer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dealer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='dealerprice',
            name='product_key',
            field=models.CharField(max_length=255, verbose_name='Номер позиции'),
        ),
        migrations.AlterField(
            model_name='dealerprice',
            name='product_name',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='dealerprice',
            name='product_url',
            field=models.URLField(max_length=255, verbose_name='Адрес получения данных'),
        ),
        migrations.AlterField(
            model_name='product',
            name='article',
            field=models.CharField(max_length=255, verbose_name='Артикул'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_1c',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название 1С'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ozon_article',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание Озон'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ozon_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название Озон'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wb_article',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Артикул WB'),
        ),
        migrations.AlterField(
            model_name='product',
            name='wb_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название WB'),
        ),
        migrations.AlterField(
            model_name='product',
            name='ym_article',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Артикул Я.Маркет'),
        ),
    ]
