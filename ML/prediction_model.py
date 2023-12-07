import os
import re
from pathlib import Path
from typing import Dict, Optional

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util


class ProseptDescriptionSearcher:

    def __init__(
            self,
            number_of_matching: Optional[int] = 5,
            cache_embeddings_update: Optional[bool] = False,
    ):
        try:
            self.model = SentenceTransformer(
                os.path.join(Path(__file__).parent.parent / 'data/model')
            )
        except:
            self.model = SentenceTransformer('LaBSE')

        self.number_of_matching = number_of_matching
        self.cache_embeddings_update = cache_embeddings_update

        self.initialization_matching()
        self.generate_embeddings()

    def initialization_matching(self):
        self.product = pd.read_csv(
            filepath_or_buffer=Path(
                __file__
            ).parent.parent / 'data/marketing_product.csv',
            sep=';',
            index_col='id'
        )
        self.clean_product()

    def clean_product(self):
        self.product = self.product[['name']]
        self.product.dropna(subset=['name'], inplace=True)
        self.product.drop_duplicates(subset=['name'], inplace=True)
        self.product = self.product.loc[~self.product['name'].str.isspace()]
        self.product.columns = ['original_name']
        for column in self.product.columns:
            self.product[f'{column}_normalized'] = self.product[column].apply(
                ProseptDescriptionSearcher.clean_description
            )

    def generate_embeddings(self):
        try:
            pre_loaded_embeddings = np.load(
                Path(
                    __file__
                ).parent.parent / 'cache_embeddings/embeddings.npy',
                allow_pickle=True
            )
            pre_loaded_embeddings = (
                pd.DataFrame(pre_loaded_embeddings,
                             columns=['original_name',
                                      'original_name_embeddings'])
            ).set_index(
                'original_name', drop=True
            )
            self.product = self.product.merge(
                pre_loaded_embeddings['original_name_embeddings'],
                left_on='original_name',
                right_index=True,
                how='left'
            )
            if self.product['original_name_embeddings'].isna().any():
                temp_df = self.product.loc[
                    self.product['original_name_embeddings'].isna()
                ].copy()
                temp_df['original_name_embeddings'] = self.model.encode(
                    temp_df['original_name_normalized'].values
                ).tolist()
                self.product['original_name_embeddings'].fillna(
                    temp_df['original_name_embeddings'], inplace=True
                )
                del temp_df
                self.save_embeddings()
        except:
            self.product['original_name_embeddings'] = self.model.encode(
                self.product['original_name_normalized'].values
            ).tolist()
            self.save_embeddings()

        if self.cache_embeddings_update:
            self.save_embeddings()

        self.unique_embeddings_matrix = torch.tensor(
            np.stack(self.product['original_name_embeddings'].values),
            dtype=torch.float32
        )

    def save_embeddings(self):
        try:
            os.makedirs(Path(__file__).parent.parent / 'cache_embeddings',
                        exist_ok=True)
            temp_df = self.product.reset_index()
            embeddings = np.array(
                temp_df[['id', 'original_name', 'original_name_embeddings']]
            )
            np.save(Path(
                __file__
            ).parent.parent / 'cache_embeddings/embeddings.npy', embeddings)
        except:
            pass

    def match_product(
            self,
            query_dictionary: Dict[str, Dict],
            number_of_matching: Optional[int] = 5,
    ):
        self.result_dict = {}

        try:
            self.number_of_matching = number_of_matching
        except:
            pass

        description = ProseptDescriptionSearcher.clean_description(
            query_dictionary['target']['product_name']
        )
        vector = torch.tensor(
            self.model.encode(description),
            dtype=torch.float32
        )
        similarity = util.cos_sim(vector, self.unique_embeddings_matrix)
        max_positions = np.argsort(
            similarity, axis=1
        )[:, -self.number_of_matching:]
        max_positions_reverse = torch.flip(max_positions, [0, 1])

        self.top_n_recommendations = self.product.iloc[
            max_positions_reverse[0]
        ]
        return self.top_n_recommendations.index

    # region description_fix
    @staticmethod
    def clean_description(text):

        extra_words = (
            r'(?:готовый\sсостав|для|концентрат|просепт|prosept|средство|'
            r'невымываемый|гелеобразный|канистра|'
            r'чистящее|спрей|универсальный|универсальная|универсальное|'
            r'пэт|жидкое|моющее|гель|чистки|'
            r'концентрированное|professional|готовое|superrubber)'
        )
        # Приведение текста к нижнему регистру
        text = text.lower()

        # Удаление чисел в скобках
        text = re.sub(r'\(\d+\)', ' ', text)

        # Вставка пробелов между кириллицей и латиницей
        text = re.sub(r'(?<=[а-яА-Я])(?=[a-zA-Z])|(?<=[a-zA-Z])(?=[а-яА-Я])',
                      ' ', text)

        # Добавление пробелов между цифрами и буквами
        text = re.sub(r'(?<=\d)(?=[а-яА-Яa-zA-Z])', ' ', text)
        text = re.sub(r'(?<=[а-яА-Яa-zA-Z])(?=\d)', ' ', text)

        # Удаление диапазонов чисел, разделенных дефисом или двоеточием
        text = re.sub(r'\b\d+(?::\d+)?[-:]\d+(?::\d+)?\b', ' ', text)

        # Удаление серийных номеров или артикулов
        text = re.sub(r'\b\d+-\d+[а-яА-Яa-zA-Z]*\b', ' ', text)

        # Преобразование объемов из литров в миллилитры и веса из кг в граммы
        text = re.sub(
            r'(\d+[,.]\d+)\s*л',
            lambda x: f"{int(float(x.group(1).replace(',', '.')) * 1000)} мл",
            text
        )
        text = re.sub(
            r'(\d+[,.]\d+)\s*кг',
            lambda x: f"{int(float(x.group(1).replace(',', '.')) * 1000)} г",
            text
        )

        # Замена "/" и "." меджду слов на пробелы
        text = re.sub(r'[/\.]', ' ', text)

        text = text.replace('-', ' ')

        # Удаление избыточных слов из списка extra_words
        text = re.sub(extra_words, ' ', text)

        # Удаление пунктуационных знаков и специальных символов
        text = re.sub(r'[,"“”/\.()–;]', ' ', text)

        # Удаление слова "и"
        text = re.sub(r'\bи\b', ' ', text)

        # Удаление дефисов, окруженных пробелами
        text = re.sub(r'\s-\s', ' ', text)

        # Удаление всех двойных пробелов и пробелов в начале/конце строки
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        # Удаление всех двойных пробелов и пробелов в начале/конце строки
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text
    # endregion description_fix
