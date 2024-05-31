import os
from abc import ABC
from typing import Optional, List

from llama_index.core.readers.file.base import get_default_fs

from turing_planet.llama_index.docqa.docqa_client import DocqaClient
from turing_planet.llama_index.docqa.docqa_retriever import DocqaRetriever


def list_files_in_directory(root_dir) -> List[str]:
    file_paths = []  # 用于存储所有文件的绝对路径

    # 遍历 root_dir 及其子目录下的所有文件和文件夹
    for root, dirs, files in os.walk(root_dir):
        # root 是当前目录的路径
        # dirs 是当前目录中的子目录名列表
        # files 是当前目录中的文件名列表
        for file in files:
            file_path = os.path.join(root, file)  # 拼接文件的绝对路径
            file_paths.append(file_path)

    return file_paths


class DocqaIndex(ABC):
    def __init__(
            self,
            endpoint: str,
            index_name: str = "docqa",
    ) -> object:
        self._endpoint = endpoint
        self._index_name = index_name
        self._client = DocqaClient(endpoint)

    def add_from_files(
            self,
            input_dir: Optional[str] = None,
            input_files: Optional[List] = None,
            split_type: Optional[int] = 1,
            version: Optional[int] = 1,
            overwrite: Optional[bool] = False,
            **kwargs
    ):
        if not input_dir and not input_files:
            raise ValueError("Must provide either `input_dir` or `input_files`.")
        fs = get_default_fs()
        file_paths = []
        if input_files:
            for path in input_files:
                if not fs.isfile(path):
                    raise ValueError(f"File {path} does not exist.")
                file_paths.append(path)
        elif input_dir:
            if not fs.isdir(input_dir):
                raise ValueError(f"Directory {input_dir} does not exist.")
            file_paths = list_files_in_directory(input_dir)

        lib_id = self._client.get_lib_id(lib_name=self._index_name)
        if lib_id is None:
            lib_id = self._client.create_lib(lib_name=self._index_name)
        elif overwrite:
            self._client.delete_lib(lib_id=lib_id)
            lib_id = self._client.create_lib(lib_name=self._index_name)

        category_id = self._client.get_category_id(lib_id=lib_id)

        for input_file in file_paths:
            file_id = self._client.upload_file(file_path=input_file)
            self._client.save_document(file_id=file_id, lib_id=lib_id, category_id=category_id, split_type=split_type, version=version, **kwargs)

    def as_retriever(
            self,
            topk: Optional[int] = 5,
            emb_topk: Optional[int] = 5,
            keyword_topk: Optional[int] = 2,
            **kwargs
    ):
        return DocqaRetriever(
            endpoint=self._endpoint,
            index_names=[self._index_name],
            topk=topk,
            emb_topk=emb_topk,
            keyword_topk=keyword_topk,
            **kwargs)
