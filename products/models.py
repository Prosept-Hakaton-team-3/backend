from django.db import models


# TODO: узнать максимальную длину всех полей, мб убрать id, улучшить str
class Dealer(models.Model):
    id = models.IntegerField(primary_key=True)  # из-за корявых исходников
    name = models.CharField('Название', max_length=100)

    class Meta:
        verbose_name = 'Дилер'
        verbose_name_plural = 'Дилеры'

    def __str__(self):
        return self.name[:10]


class Product(models.Model):
    article = models.CharField('Артикул', max_length=100)
    ean_13 = models.CharField('EAN-13', max_length=100)
    name = models.CharField('Название', max_length=100)
    cost = models.FloatField('Цена')
    min_recommended_price = models.FloatField(
        'Минимальная рекомендованная цена'
    )
    recommended_price = models.FloatField('Рекомендованная цена')
    category_id = models.FloatField('Id категории')
    ozon_name = models.CharField('Название Озон', max_length=100)
    name_1c = models.CharField('Название 1С', max_length=100)
    wb_name = models.CharField('Название WB', max_length=100)
    ozon_article = models.CharField('Описание Озон', max_length=100)
    wb_article = models.CharField('Артикул WB', max_length=100)
    ym_article = models.CharField('Артикул Я.Маркет', max_length=100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name[:10]


class DealerPrice(models.Model):
    id = models.IntegerField(primary_key=True)
    # TODO: maybe unique
    product_key = models.CharField(
        'Номер позиции',
        max_length=100
    )
    price = models.IntegerField('Цена', )
    # TODO: maybe urlfield
    product_url = models.CharField(
        'Адрес получения данных',
        max_length=100
    )
    product_name = models.CharField('Заголовок', max_length=100)
    date = models.DateField('Дата получения данных', )
    dealer_id = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        verbose_name='Дилер'
    )

    class Meta:
        verbose_name = 'С площадок дилера'
        verbose_name_plural = 'С площадок дилеров'

    def __str__(self):
        return self.product_name[:10]


class ProductDealer(models.Model):
    key = models.ForeignKey(
        DealerPrice,
        related_name='matches',
        on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    dealer_id = models.ForeignKey(Dealer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт дилера'
        verbose_name_plural = 'Продукты дилеров'
