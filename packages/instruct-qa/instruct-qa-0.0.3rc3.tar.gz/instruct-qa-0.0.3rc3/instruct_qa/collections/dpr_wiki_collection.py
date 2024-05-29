import csv
import os
from typing import Dict, List

import requests
from tqdm import tqdm

import instruct_qa.experiment_utils as utils

from . import PassageCollection

DPR_WIKI_DOWNLOAD_URL = (
    "https://dl.fbaipublicfiles.com/dpr/wikipedia_split/psgs_w100.tsv.gz"
)


class DPRWikiCollection(PassageCollection):
    def __init__(
        self,
        name: str = "dpr_wiki",
        file_name: str = "psgs_w100.tsv",
        cachedir: str = "data/nq/collection",
        id_col: int = 0,
        text_col: int = 1,
        title_col: int = 2,
        id_prefix: str = "wiki:",
        normalize: bool = True,
    ):
        super().__init__(name)
        self.id_col = id_col
        self.text_col = text_col
        self.title_col = title_col
        self.id_prefix = id_prefix
        self.normalize = normalize
        self._id_to_index = {}
        self.header_included = False
        self.load_data(os.path.join(cachedir, file_name))

    def load_data(self, path_to_file: str):

        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
        if not os.path.exists(path_to_file):
            utils.wget(DPR_WIKI_DOWNLOAD_URL, path_to_file, compressed=True)

        with open(path_to_file) as ifile:
            reader = csv.reader(ifile, delimiter="\t")
            for i, row in enumerate(tqdm(reader, desc="Loading DPR Wiki")):
                if row[self.id_col] == "id":
                    self.header_included = True
                    continue
                sample_id = self.id_prefix + str(row[self.id_col])
                passage = row[self.text_col]
                title = row[self.title_col]
                sub_title = ""
                if self.normalize:
                    passage = normalize_passage(passage)
                index = i - 1 if self.header_included else i
                self.passages.append(
                    {
                        "id": sample_id,
                        "text": passage,
                        "title": title,
                        "sub_title": sub_title,
                        "index": index,
                    }
                )
                self._id_to_index[sample_id] = index

    def get_passage_from_id(self, id: str) -> Dict[str, str]:
        passage = self.passages[self._id_to_index[id]]
        assert passage["index"] == self._id_to_index[id]
        return passage

    def get_indices_from_ids(self, ids: List[str]) -> List[int]:
        return [self._id_to_index[id] for id in ids]


def normalize_passage(ctx_text: str):
    ctx_text = ctx_text.replace("\n", " ").replace("’", "'")
    return ctx_text
