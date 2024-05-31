from llama_index.core import get_response_synthesizer
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import ResponseMode

from turing_planet.llama_index.docqa.docqa_index import DocqaIndex
from turing_planet.llama_index.docqa.docqa_retriever import DocqaRetriever

import introduce_base

if __name__ == '__main__':
    docqa_index = DocqaIndex(endpoint='172.30.94.42:8906', index_name='docqa-test')
    # docqa_retriever = DocqaRetriever(endpoint='172.30.94.42:8906', index_names=['docqa-test'])
    docqa_retriever = docqa_index.as_retriever(topk=5, emb_topk=5, keyword_topk=2)

    response_synthesizer = get_response_synthesizer(
        response_mode=ResponseMode.COMPACT,
    )

    query_engine = RetrieverQueryEngine(retriever=docqa_retriever, response_synthesizer=response_synthesizer)

    question = "截止2024年1月，合肥市创建国家卫生城市计划实施步骤进展到什么阶段了？"
    response = query_engine.query(question + "\n中文回答")
    print(f"Q:{question}")
    print("A:" + response.response.replace("<ret>", "\n").replace("<end>", "\n"))
    print("---------------\n")
