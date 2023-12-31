from django.db import models

from config.constants import CHAR_FIELD_SIZE, EAN_13_SIZE, TEXT_VIEW_SIZE


class Dealer(models.Model):
    name = models.CharField('Название', max_length=CHAR_FIELD_SIZE)

    class Meta:
        verbose_name = 'Дилер'
        verbose_name_plural = 'Дилеры'

    def __str__(self):
        return self.name[:TEXT_VIEW_SIZE]


class Product(models.Model):
    article = models.CharField('Артикул', max_length=CHAR_FIELD_SIZE)
    ean_13 = models.CharField('EAN-13', max_length=EAN_13_SIZE)
    name = models.CharField(
        'Название', blank=True,
        null=True, max_length=CHAR_FIELD_SIZE
    )
    cost = models.FloatField('Цена', null=True)
    min_recommended_price = models.FloatField(
        'Минимальная рекомендованная цена', null=True,
    )
    recommended_price = models.FloatField('Рекомендованная цена', null=True)
    category_id = models.FloatField('Id категории', null=True)
    ozon_name = models.CharField(
        'Название Озон', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )
    name_1c = models.CharField(
        'Название 1С', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )
    wb_name = models.CharField(
        'Название WB', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )
    ozon_article = models.CharField(
        'Описание Озон', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )
    wb_article = models.CharField(
        'Артикул WB', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )
    ym_article = models.CharField(
        'Артикул Я.Маркет', max_length=CHAR_FIELD_SIZE, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name[:TEXT_VIEW_SIZE]


class DealerPrice(models.Model):
    product_key = models.CharField(
        'Номер позиции',
        max_length=CHAR_FIELD_SIZE
    )
    price = models.IntegerField('Цена')
    product_url = models.URLField(
        'Адрес получения данных',
        max_length=CHAR_FIELD_SIZE
    )
    product_name = models.CharField('Заголовок', max_length=CHAR_FIELD_SIZE)
    date = models.DateField('Дата получения данных')
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        verbose_name='Дилер'
    )

    class Meta:
        verbose_name = 'С площадок дилера'
        verbose_name_plural = 'С площадок дилеров'

    def __str__(self):
        return self.product_name[:TEXT_VIEW_SIZE]


class ProductDealer(models.Model):
    key = models.ForeignKey(
        DealerPrice,
        on_delete=models.CASCADE,
        related_name='matches'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт дилера'
        verbose_name_plural = 'Продукты дилеров'
        constraints = (
            models.UniqueConstraint(
                fields=['key', 'dealer', 'product'],
                name='unique_dealer_product_key'),
        )
