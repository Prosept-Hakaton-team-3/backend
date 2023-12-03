import csv

from .models import Dealer, Product, DealerPrice, ProductDealer


# TODO: возможно это все стоит засунуть в класс вроде CSVProcessing
# TODO: защита повторного заполнения базы (увеличит время подгрузки)
def try_convert(value, try_type):
    try:
        new_value = try_type(value)
    except ValueError as error:
        return value
    return new_value


# TODO: по мере необходимости добавить нужные поля повсюду
def import_dealers(file_path):
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        dealers = [
            Dealer(
                id=try_convert(row['id'], int),
                name=row['name']
            ) for row in reader
        ]
        Dealer.objects.bulk_create(dealers)


def import_products(file_path):
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        products = {
            Product(
                id=try_convert(row['id'], int),
                article=row['article'],
                ean_13=row['ean_13'],
                name=row['cost'],
                cost=try_convert(row['name'], float) if row['name'] else None,
            ) for row in reader
        }
        Product.objects.bulk_create(products)


def import_dealer_prices(file_path):
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        DealerPrice.objects.bulk_create({
            DealerPrice(
                id=try_convert(row['id'], int),
                price=try_convert(row['price'], float),
                product_url=row['product_url'],
                product_name=row['product_name'],
                date=row['date'],
                product_key=row['product_key'],
                dealer_id=try_convert(row['dealer_id'], int)
            ) for row in reader
        })


# там в этом файле вместо key_id лежат ссылки, поэтому непонятно как импортнуть
# def import_product_dealers(file_path):
#     with open(file_path, encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile, delimiter=';')
#         product_dealers = [
#             ProductDealer(
#                 id=int(row['id']),
#                 key_id=int(row['key']),
#                 dealer_id=int(row['dealer_id']),
#                 product_id=int(row['product_id'])
#             ) for row in reader
#         ]
#         ProductDealer.objects.bulk_create(product_dealers)


def import_csv_data(paths):
    # TODO: улучшить систему путей
    import_dealers(paths['marketing_dealer'])
    import_dealer_prices(paths['marketing_dealerprice'])
    import_products(paths['marketing_product'])
    # import_product_dealers(paths['marketing_productdealerkey'])
