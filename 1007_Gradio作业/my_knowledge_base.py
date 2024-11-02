from langchain_text_splitters import RecursiveCharacterTextSplitter
from unstructured.file_utils.filetype import FileType, detect_filetype
from langchain_core.document_loaders import BaseLoader
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredMarkdownLoader,
)

# UPLOAD_DIR = "uploads"
LLM_MODELS = "gpt-4o", [
    "gpt-3.5-turbo",
]
KNOWLEDGE_DIR = "chroma/knowledge/"


class MyKnowledgeBase:

    pass


class MyCustomLoader(BaseLoader):

    # 支持加载的文件类型
    file_type = {
        FileType.CSV: (CSVLoader, {"autodetect_encoding": True}),
        FileType.TXT: (TextLoader, {"autodetect_encoding": True}),
        FileType.PDF: (PyPDFLoader, {}),
        FileType.DOC: (UnstructuredWordDocumentLoader, {}),
        FileType.DOCX: (UnstructuredWordDocumentLoader, {}),
        FileType.MD: (UnstructuredMarkdownLoader, {}),
    }

    # 初始化方法  将加载的文件进行切分
    def __init__(self, file_path: str):
        loader_class, params = self.file_type[
            detect_filetype(file_path)
        ]  # 加载对应的文件加载器
        print("loader_class:", loader_class)
        print("params:", params)
        self.loader: BaseLoader = loader_class(file_path, **params)
        print("self.loader:", self.loader)
        self.text_splitter = RecursiveCharacterTextSplitter(  # 内容分隔
            separators=["\n\n", "\n", " ", ""],
            chunk_size=1000,  # 每1000个字符分隔一次
            chunk_overlap=200,  # 用末尾200个字符当做衔接词，增强语义
            length_function=len,
        )

    def lazy_load(self):
        # 懒惰切分加载
        return self.loader.load_and_split(self.text_splitter)

    def load(self):
        # 加载
        return self.lazy_load()
