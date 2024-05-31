from llama_index.core import SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline

from turing_planet.llama_index.docqa.docqa_node_parser import DocqaNodeParser
import introduce_base

if __name__ == '__main__':
    simple_reader = SimpleDirectoryReader(input_files=['/Users/wujian/workspace/引擎/01.大模型/08_星探平台/测试集/合政〔2022〕176号.docx'])
    documents = simple_reader.load_data(show_progress=True)
    pipeline = IngestionPipeline(transformations=[DocqaNodeParser(endpoint='172.31.221.74:8085', split_type=1, separator='', )])
    nodes = pipeline.run(documents=documents)
    for node in nodes:
        print(node)
