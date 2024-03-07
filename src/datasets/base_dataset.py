import logging
import random
from typing import List

import numpy as np
import torch
from torch import Tensor
from torch.utils.data import Dataset

logger = logging.getLogger(__name__)


class BaseDataset(Dataset):
    def __init__(
        self,
        index,
        limit=None,
    ):
        self._assert_index_is_valid(index)
        self._index: List[dict] = index

    def __getitem__(self, ind):
        data_dict = self._index[ind]
        data_path = data_dict["path"]
        data_object = self.load_object(data_path)
        data_label = data_dict["label"]
        data_object = self.process_object(data_object)
        return {"object": data_object, "label": data_label}

    def __len__(self):
        return len(self._index)

    def load_object(self, path):
        # TODO load object from path
        data_object = torch.load(path)
        return data_object

    def process_object(self, data_object):
        # TODO apply augs
        return data_object

    @staticmethod
    def _filter_records_from_dataset(
        index: list,
    ) -> list:
        # TODO Filter logic
        pass

    @staticmethod
    def _assert_index_is_valid(index):
        for entry in index:
            assert "path" in entry, (
                "Each dataset item should include field 'path'" " - path to audio file."
            )

    @staticmethod
    def _sort_index(index):
        return sorted(index, key=lambda x: x["KEY_FOR_SORTING"])

    @staticmethod
    def _limit_index(index, limit):
        return index[:limit]