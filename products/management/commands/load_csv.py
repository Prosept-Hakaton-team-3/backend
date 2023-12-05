import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from products.utils import CSVProcessing

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
                filepath.split('/')[-1].split('.')[0]:
                    settings.BASE_DIR / filepath
                for filepath in FILEPATHS
            }
            CSVProcessing(absolute_paths).import_csv_data()
        except Exception:
            logger.exception(
                f'Ошибка. Данные не были загружены.',
                exc_info=True
            )
            return
        logging.info('Данные успешно загружены.')
