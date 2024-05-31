from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_index.core.node_parser import SentenceSplitter

from test.llama_index.introduce.introduce_base import redis_store, mongo_doc_store

if __name__ == '__main__':
    # create parser and parse document into nodes
    # 加载数据
    documents = SimpleDirectoryReader("../data").load_data(show_progress=True)

    parser = SentenceSplitter()
    nodes = parser.get_nodes_from_documents(documents)

    # create (or load) docstore and add nodes
    # docstore = MongoDocumentStore.from_uri(uri="<mongodb+srv://...>")

    mongo_doc_store.add_documents(nodes)

    # # create storage context
    # storage_context = StorageContext.from_defaults(docstore=docstore)
    #
    # # build index
    # index = VectorStoreIndex(nodes, storage_context=storage_context)

    #  向量检索
    vector_index = VectorStoreIndex.from_vector_store(vector_store=redis_store)
    vector_index.insert_nodes(nodes=nodes)