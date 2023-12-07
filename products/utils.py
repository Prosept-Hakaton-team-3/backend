import csv
from pathlib import Path
from typing import Any, Union

from .models import Dealer, DealerPrice, Product, ProductDealer


def try_convert(value: Any, try_type: type) -> Any:
    try:
        new_value = try_type(value)
    except ValueError:
        return None
    return new_value


def import_dealers(file_path: Union[Path, str],
                   encoding: str,
                   delimiter: str) -> None:
    with open(file_path, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        dealers = set(
            Dealer(
                id=index,
                name=row['name']
            ) for index, row in enumerate(reader, 1)
        )
        Dealer.objects.bulk_create(dealers, ignore_conflicts=True)


def import_products(file_path: Union[Path, str],
                    encoding: str,
                    delimiter) -> None:
    with open(file_path, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        products = set(
            Product(
                id=index,
                article=row['article'],
                ean_13=row['ean_13'].split('.')[0],
                name=row['name'],
                cost=try_convert(row['cost'], float),
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

            ) for index, row in enumerate(reader, 1)
        )
        Product.objects.bulk_create(products, ignore_conflicts=True)


def import_dealer_prices(file_path: Union[Path, str],
                         encoding: str,
                         delimiter: str) -> None:
    with open(file_path, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        dealer_prices = set()
        for index, row in enumerate(reader, 1):
            dealer_id = try_convert(row['dealer_id'], int)
            if Dealer.objects.filter(id=dealer_id).exists():
                dealer_prices.add(
                    DealerPrice(
                        id=index,
                        price=try_convert(row['price'], float),
                        product_url=row['product_url'],
                        product_name=row['product_name'],
                        date=row['date'],
                        product_key=row['product_key'],
                        dealer_id=try_convert(row['dealer_id'], int)
                    )
                )
        DealerPrice.objects.bulk_create(
            dealer_prices, ignore_conflicts=True
        )


def import_product_dealers(file_path: Union[Path, str],
                           encoding: str,
                           delimiter: str) -> None:
    with open(file_path, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        product_dealers = set()
        for index, row in enumerate(reader, 1):
            key = row['key']
            dealer_id = try_convert(row['dealer_id'], int)
            product_id = try_convert(row['product_id'], int)
            if (DealerPrice.objects.filter(product_key=key).exists()
                    and Dealer.objects.filter(id=dealer_id).exists()
                    and Product.objects.filter(id=product_id).exists()):
                product_dealers.add(
                    ProductDealer(
                        id=index,
                        key=DealerPrice.objects.filter(
                            product_key=row['key']
                        ).first(),
                        dealer_id=dealer_id,
                        product_id=product_id
                    )
                )
        ProductDealer.objects.bulk_create(
            product_dealers, ignore_conflicts=True
        )


NAME_TO_METHOD = {
    'dealer': import_dealers,
    'dealerprice': import_dealer_prices,
    'product': import_products,
    'productdealerkey': import_product_dealers
}


def import_csv_data(paths: dict[str, Union[Path, str]],
                    encoding='utf-8',
                    delimiter=';') -> None:
    for name, absolute_path in paths.items():
        if name in NAME_TO_METHOD:
            NAME_TO_METHOD[name](absolute_path, encoding, delimiter)
