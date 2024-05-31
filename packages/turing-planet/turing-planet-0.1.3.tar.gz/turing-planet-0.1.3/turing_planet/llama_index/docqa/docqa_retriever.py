from typing import List, Optional, Any

from llama_index.core import QueryBundle
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.schema import NodeWithScore, TextNode

from turing_planet.llama_index.docqa.docqa_client import DocqaClient


class DocqaRetriever(BaseRetriever):
    _index_names: List[str]
    _client: DocqaClient
    _topk: Optional[int]
    _emb_topk: Optional[int]
    _keyword_topk: Optional[int]
    _kwargs: Any

    def __init__(
            self,
            endpoint: str,
            index_names: Optional[List[str]] = None,
            topk: Optional[int] = 5,
            emb_topk: Optional[int] = 5,
            keyword_topk: Optional[int] = 2,
            **kwargs
    ):
        self._index_names = index_names
        self._client = DocqaClient(endpoint)
        self._topk = topk
        self._emb_topk = emb_topk
        self._keyword_topk = keyword_topk
        self._kwargs = kwargs
        super().__init__()

    def _retrieve(self, query_bundle: QueryBundle) -> List[NodeWithScore]:
        lib_list = []
        if self._index_names:
            for index_name in self._index_names:
                lib_id = self._client.get_lib_id(lib_name=index_name)
                if lib_id is None:
                    raise ValueError(f"index {index_name} does not exist.")
                lib_list.append({'name': lib_id, 'version': 1})

        docqa_nodes = self._client.retriever(
            content=query_bundle.query_str,
            lib_list=lib_list,
            topk=self._topk,
            emb_topk=self._emb_topk,
            keyword_topk=self._keyword_topk,
            **self._kwargs
        )
        return [NodeWithScore(node=TextNode(text=docqa_node['content']), score=docqa_node['score']) for docqa_node in docqa_nodes]
