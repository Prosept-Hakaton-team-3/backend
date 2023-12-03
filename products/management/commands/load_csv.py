import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from products.utils import import_csv_data

logger = logging.getLogger(__name__)

FILEPATHS = [
    'data/marketing_dealer.csv',
    'data/marketing_dealerprice.csv',
    'data/marketing_product.csv',
    'data/marketing_productdealerkey.csv'
]


class Command(BaseCommand):
    """Команда для загрузки csv файлов."""

    def handle(self, *args, **options):
        try:
            absolute_paths = {
                filepath.split('/')[-1].split('.')[
                    0]: settings.BASE_DIR / filepath
                for filepath in FILEPATHS
            }
            import_csv_data(absolute_paths)
        except Exception:
            logger.exception(
                f'Ошибка. Данные не были загружены.',
                exc_info=True
            )
            return
        logging.info('Данные успешно загружены.')
