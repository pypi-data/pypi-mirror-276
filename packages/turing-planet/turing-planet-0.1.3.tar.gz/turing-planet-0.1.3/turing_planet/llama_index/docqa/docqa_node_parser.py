import logging
from enum import IntEnum
from typing import Callable, List, Optional, Any

from llama_index.core.bridge.pydantic import Field, PrivateAttr
from llama_index.core.callbacks import CallbackManager
from llama_index.core.node_parser import TextSplitter
from llama_index.core.schema import Document

from turing_planet.llama_index.docqa.docqa_client import DocqaClient

logger = logging.getLogger(__name__)

DEFAULT_FILE_TYPE = 'text'
DEFAULT_SEPARATOR = ''


class SplitType(IntEnum):
    INTELLIGENT_SPLIT = 1,
    """
    智能拆分
    """

    SEPARATOR_SPLIT = 2,
    """
    分隔符拆分
    """

    PARA_THRESHOLD = 3,
    """
    按目录拆分
    """

    NORMAL_SPLIT = 4,
    """
    按自然段拆分
    """

    NOT_SPLIT = 5,
    """
    不拆分
    """

    COUNT_SPLIT = 6,
    """
    按字数拆分
    """


class DocqaNodeParser(TextSplitter):
    _file_type: str = PrivateAttr()
    _split_type: str = PrivateAttr()
    _separator: str = PrivateAttr()
    _client: DocqaClient = PrivateAttr()
    _kwargs: Any = PrivateAttr()

    def __init__(
            self,
            endpoint: str,
            file_type: Optional[str] = DEFAULT_FILE_TYPE,
            split_type: Optional[int] = SplitType.INTELLIGENT_SPLIT,
            separator: Optional[str] = DEFAULT_SEPARATOR,
            callback_manager: Optional[CallbackManager] = None,
            include_metadata: bool = True,
            include_prev_next_rel: bool = True,
            id_func: Optional[Callable[[int, Document], str]] = None,
            **kwargs,
    ):
        self._client = DocqaClient(endpoint)
        self._file_type = file_type
        self._split_type = split_type
        self._separator = separator
        self._kwargs = kwargs
        super().__init__(
            callback_manager=callback_manager or CallbackManager(),
            include_metadata=include_metadata,
            include_prev_next_rel=include_prev_next_rel,
            id_func=id_func,
        )

    def split_text(self, text: str) -> List[str]:
        """Split text into sentences."""
        nodes = self._client.split(content=text,
                                   file_name='123.txt',
                                   file_type=self._file_type,
                                   split_type=self._split_type,
                                   separator=self._separator,
                                   **self._kwargs
                                   )
        return [node['content'] for node in nodes]
