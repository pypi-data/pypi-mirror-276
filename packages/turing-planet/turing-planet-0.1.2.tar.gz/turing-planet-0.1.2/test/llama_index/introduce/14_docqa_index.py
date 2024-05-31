from turing_planet.llama_index.docqa.docqa_index import DocqaIndex
import introduce_base

if __name__ == '__main__':
    docqa_index = DocqaIndex(endpoint='172.30.94.42:8906', index_name='docqa-test')

    docqa_index.add_from_files(input_dir='../data', overwrite=True)
