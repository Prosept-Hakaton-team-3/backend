import csv

from .models import Dealer, DealerPrice, Product, ProductDealer


# TODO: type hinting
# TODO: Log everything, unittest
# TODO: возможно отказаться от id
def try_convert(value, try_type):
    try:
        new_value = try_type(value)
    except ValueError:
        return None
    return new_value


class CSVProcessing:
    def __init__(self, paths):
        self.dealer_path = paths.get('marketing_dealer')
        self.dealer_price_path = paths.get('marketing_dealerprice')
        self.product_path = paths.get('marketing_product')
        self.product_dealers_path = paths.get('marketing_productdealerkey')

    def import_dealers(self):
        with open(self.dealer_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            dealers = [
                Dealer(
                    id=try_convert(row['id'], int),
                    name=row['name']
                ) for row in reader
            ]
            Dealer.objects.bulk_create(dealers, ignore_conflicts=True)

    def import_products(self):
        with open(self.product_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            products = {
                Product(
                    id=try_convert(row['id'], int),
                    article=row['article'],
                    ean_13=row['ean_13'],
                    name=row['cost'],
                    cost=try_convert(row['name'], float),
                    recommended_price=try_convert(
                        row['recommended_price'], float
                    ),
                    category_id=(try_convert(row['category_id'], float)),
                    ozon_name=row['ozon_name'],
                    name_1c=row['name_1c'],
                    wb_name=row['wb_name'],
                    ozon_article=row['ozon_article'],
                    wb_article=row['wb_article'],
                    ym_article=row['ym_article']

                ) for row in reader
            }
            Product.objects.bulk_create(products, ignore_conflicts=True)

    def import_dealer_prices(self):
        with open(self.dealer_price_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            dealer_prices = {
                DealerPrice(
                    id=try_convert(row['id'], int),
                    price=try_convert(row['price'], float),
                    product_url=row['product_url'],
                    product_name=row['product_name'],
                    date=row['date'],
                    product_key=row['product_key'],
                    dealer_id=try_convert(row['dealer_id'], int)
                ) for row in reader
            }
            DealerPrice.objects.bulk_create(
                dealer_prices, ignore_conflicts=True
            )

    def import_product_dealers(self):
        with open(self.product_dealers_path, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            product_dealers = [
                ProductDealer(
                    id=try_convert(row['id'], int),
                    key=DealerPrice.objects.filter(
                        product_key=row['key']
                    ).first(),
                    dealer_id=try_convert(row['dealer_id'], int),
                    product_id=try_convert(row['product_id'], int)
                ) for row in reader
            ]
            ProductDealer.objects.bulk_create(
                product_dealers, ignore_conflicts=True
            )

    def import_csv_data(self):
        self.import_dealers()
        self.import_dealer_prices()
        self.import_products()
        self.import_product_dealers()
