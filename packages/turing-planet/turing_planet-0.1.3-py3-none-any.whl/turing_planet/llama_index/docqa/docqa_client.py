import json
import logging
from typing import List, Optional

import requests

logger = logging.getLogger(__name__)


class DocqaClient:

    def __init__(
            self,
            endpoint: str,
    ) -> None:
        self.endpoint = endpoint

    def split(
            self,
            content: str,
            file_name: str,
            file_type: str,
            split_type: Optional[int] = 1,
            separator: Optional[str] = '',
            **kwargs
    ) -> List[dict]:
        """
        文本切分
        """
        api_url = f'http://{self.endpoint}/doc/split'
        body = {
            'content': content,
            'fileName': file_name,
            'fileType': file_type,
            'splitType': split_type,
            'separator': separator
        }
        body = {**body, **kwargs}
        logger.debug(f'docqa split document. request = {body}')
        response = requests.post(url=api_url, json=body, headers={'content-type': 'application/json'}).text
        logger.debug(f'docqa split document. response = {response}')

        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa split document. code={code}')
        else:
            return data['data']

    def create_lib(self, lib_name: str, **kwargs) -> str:
        body = {
            'name': lib_name,
        }
        body = {**body, **kwargs}
        api_url = f'http://{self.endpoint}/doc/semantic-doc/lib/create'
        logger.debug(f'docqa create lib. request = {body}')
        response = requests.post(url=api_url, json=body, headers={'content-type': 'application/json'}).text
        logger.debug(f'docqa create lib. response = {response}')

        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa create lib error. code={code}')
        else:
            return data['data']['id']

    def delete_lib(self, lib_id: str):
        api_url = f'http://{self.endpoint}/doc/semantic-doc/lib/{lib_id}'
        logger.debug(f'docqa delete lib. request = {lib_id}')
        response = requests.delete(url=api_url).text
        logger.debug(f'docqa delete lib. response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa delete lib error. code={code}')

    def get_lib_id(self, lib_name) -> str:
        api_url = f'http://{self.endpoint}/doc/semantic-doc/lib/page'
        params = {
            'name': lib_name,
            'pageNumber': 1,
            'pageSize': 1
        }
        logger.debug(f'docqa get lib id. request = {params}')
        response = requests.get(url=api_url, params=params, headers={'content-type': 'application/json'}).text
        logger.debug(f'docqa get lib id. response = {response}')
        print(response)
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa get lib id error. code={code}')
        else:
            return data['items'][0]['id'] if data['total'] > 0 else None

    def get_category_id(self, lib_id: str, version: Optional[int] = 1) -> str:
        body = {
            'libId': lib_id,
            'version': version
        }
        api_url = f'http://{self.endpoint}/doc/semantic-doc/category/list'
        logger.debug(f'docqa get category id. request = {body}')
        response = requests.post(url=api_url, json=body, headers={'content-type': 'application/json'}).text
        print(response)
        logger.debug(f'docqa get category id. response = {response}')

        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa get category id error. code={code}')
        else:
            return data['data'][0]['id']

    def upload_file(self, file_path: str) -> str:
        logger.debug(f'docqa upload file. request = {file_path}')
        api_url = f'http://{self.endpoint}/doc/semantic-doc/document/files/upload'
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(url=api_url, files=files).text
        logger.debug(f'docqa upload file. response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa upload file error. code={code}')
        else:
            return data['data'][0]['id']

    def save_document(self, file_id: str, lib_id: str, category_id: str, split_type: Optional[int] = 1, version: Optional[int] = 1, **kwargs):
        logger.debug(f'docqa save document. file_id = {file_id}, lib_id={lib_id}')
        body = {
            'fileID': [
                file_id  # 文档id
            ],
            'libId': lib_id,  # 文档库id
            'version': version,
            'splitType': split_type,
            'categoryID': category_id,
            # 'fileType': 'text',
            # 'preview': True,
        }
        body = {**body, **kwargs}
        api_url = f'http://{self.endpoint}/doc/semantic-doc/document'
        logger.debug(f'docqa save document. request = {body}')
        response = requests.post(url=api_url, json=body, headers={'content-type': 'application/json'}).text
        print(f'docqa save document:  {response}')
        logger.debug(f'docqa save document. response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa save document error. code={code}')
        else:
            return data['data'][0]['id']

    def preview_nodes(self, document_id: str) -> List[dict]:
        logger.debug(f'docqa preview nodes. document_id = {document_id}')
        api_url = f'http://{self.endpoint}/doc/semantic-doc/document/preview/{document_id}'
        response = requests.get(url=api_url).text
        print(f'docqa preview nodes:  {response}')
        logger.debug(f'docqa preview nodes response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa save document error. code={code}')
        else:
            return data['data']

    def index_document(self, document_ids: List[str]):
        logger.debug(f'docqa index document. document_ids = {document_ids}')
        api_url = f'http://{self.endpoint}/doc/semantic-doc/document/split/batch'
        response = requests.post(url=api_url, json=document_ids, headers={'content-type': 'application/json'}).text
        print(f'docqa index document:  {response}')
        logger.debug(f'docqa index document response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa index document error. code={code}')

    def retriever(
            self,
            content: str,
            lib_list: List[dict],
            topk: int = 5,
            emb_topk: int = 5,
            keyword_topk: int = 2,
            qa_enable: Optional[bool] = False,
            threshold_score: Optional[float] = 0.1,
            qa_threshold_score: Optional[float] = 0.8,
            **kwargs
    ) -> List[dict]:
        api_url = f'http://{self.endpoint}/doc/milvus/embedding/larger'
        body = {
            'content': content,
            'top': topk,
            'embeddingTop': emb_topk,
            'esTop': keyword_topk,
            'dbList': lib_list,
            # 'categoryId': [],
            # 'docId': [],
            'qaEnable': qa_enable,
            'thresholdScore': threshold_score,
            'qaThresholdScore': qa_threshold_score
        }
        body = {**body, **kwargs}
        logger.debug(f'docqa retriever. request = {body}')
        response = requests.post(url=api_url, json=body, headers={'content-type': 'application/json'}).text
        logger.debug(f'docqa retriever. response = {response}')
        data = json.loads(response)
        code = data['retcode']
        if code != 200:
            raise DocqaClientError(f'docqa retriever error. code={code}')
        else:
            return data['data']['parts']


class DocqaClientError(Exception):
    pass


if __name__ == '__main__':
    # client = DocqaClient(endpoint='172.31.221.74:8085')
    client = DocqaClient(endpoint='172.30.94.42:8906')

    # lib_id = client.create_lib(lib_name='wj_test_5')
    # print(f'lib_id = {lib_id}')
    lib_id = 'fae792c53a744758a7a935feb476caac'

    print(client.get_category_id(lib_id=lib_id))

    # file_id = client.upload_file(file_path='/Users/wujian/workspace/引擎/01.大模型/08_星探平台/测试集/合政〔2022〕176号.docx')
    # print(f'file_id = {file_id}')
    file_id = '663c2c9ea53eee2b1b78ed7d'

    # document_id = client.save_document(file_id=file_id, lib_id=lib_id)
    # print(f'document_id = {document_id}')
    document_id = '3f45c9fe5c96484590ccad5693053a7c'

    # client.preview_nodes(document_id=document_id);
    # client.index_document(document_ids=[document_id])

    # client.retriever(content='截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？', lib_list=[{'name': lib_id, 'version': 1}], emb_topk=5,
    #                  keyword_topk=2)
    # print(client.retriever(content='火影忍者剧情', lib_list=[{'name': '07f271fbd6034b928ffa135419884802', 'version': 1}]))
