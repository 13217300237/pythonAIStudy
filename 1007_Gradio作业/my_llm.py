import hashlib
import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_openai import ChatOpenAI, OpenAI
from typing import List, Optional, Iterable
from langchain_core.messages import AIMessageChunk
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import AddableDict
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.document_loaders import BaseLoader
from langchain_community.vectorstores import Chroma
from langchain.retrievers import (
    ContextualCompressionRetriever,
    EnsembleRetriever,
    RePhraseQueryRetriever,
)
from langchain.retrievers.document_compressors import (
    LLMChainFilter,
    CrossEncoderReranker,
)
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.indexing import index
from langchain_community.retrievers import BM25Retriever
from langchain.indexes import SQLRecordManager

from my_knowledge_base import KNOWLEDGE_DIR, MyCustomLoader


def streaming_parse(chunks: Iterable[AIMessageChunk]):
    for chunk in chunks:
        yield AddableDict({"answer": chunk.content})


def get_md5(input_string):
    # 创建一个 md5 哈希对象
    hash_md5 = hashlib.md5()
    # 需要确保输入字符串是字节串，因此如果它是字符串，则需要编码为字节串
    hash_md5.update(input_string.encode("utf-8"))
    # 获取十六进制的哈希值
    return hash_md5.hexdigest()


embedding_model = "BAAI/bge-large-zh-v1.5"
model_kwargs = {"device": "cpu"}
# 向量化模型
embeddings = HuggingFaceBgeEmbeddings(
    model_name=embedding_model, model_kwargs=model_kwargs
)


# 创建我的LLM功能管理类
class MyLLM:
    __chat_history = ChatMessageHistory()  # 创建历史记录
    __retrievers = {}
    __llm = OpenAI(temperature=0)

    collections = []

    # 做知识库文件的向量化
    def knowledge_file_embedding(self):
        os.makedirs(os.path.dirname(KNOWLEDGE_DIR), exist_ok=True)  # 创建

        list = os.listdir(KNOWLEDGE_DIR)
        print("已有的知识库", list)
        self.collections = []
        for file in list:
            print(file)
            self.collections.append(file)
            file_path = os.path.join(KNOWLEDGE_DIR, file)
            collection_name = get_md5(file)  # 用md5算法对一个知识库进行唯一标识

            # 过滤掉已经向量化的文件放置重复动作
            if collection_name in self.__retrievers:
                continue
            loader = MyCustomLoader(file_path)
            print("loader", loader)
            self.__retrievers[collection_name] = self.create_indexes(
                collection_name, loader, embeddings
            )
            print("collections:", self.collections)
        return self.collections

    # 创建知识库索引
    def create_indexes(
        self,
        collection_name: str,
        loader: BaseLoader,
        embedding_function: Optional[Embeddings] = None,
    ):
        # 使用chromar这个向量数据库来做向量化
        db = Chroma(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=os.path.join("./chroma", collection_name),
        )

        record_manager = SQLRecordManager(
            f"chromadb/{collection_name}", db_url="sqlite:///record_manager_cache.sql"
        )
        record_manager.create_schema()
        documents = loader.load()
        r = index(documents, record_manager, db, cleanup="full", source_id_key="source")
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                db.as_retriever(search_kwargs={"k": 3}),
                BM25Retriever.from_documents(documents),
            ]
        )

        return ensemble_retriever

    # 创建调用AI用的chain
    def get_chain(self, collections, model, max_length, temperature):
        retriever = None

        if collections:
            retriever = self.get_retrievers(collections)

        print("开始创建chain，保留最后6条历史")
        # 为了节约性能，不要在每次getChain的时候都去读取全部记忆
        if len(self.__chat_history.messages) > 6:
            self.__chat_history.messages = self.__chat_history.messages[
                -6:
            ]  # 只保留最后6条
        print("开始创建 ChatOpenAI")
        chat = ChatOpenAI(
            model=model, temperature=temperature, max_tokens=max_length
        )  # 创建client，为创建链条做准备

        print("开始创建 chain")

        # 考虑rag的情况
        if retriever:
            # 知识库问答指令
            qa_system_prompt = (
                "你叫瓜皮，一个帮助人们解答各种问题的助手。 "
                "使用检索到的上下文来回答问题。如果你不知道答案，就说你不知道。 "
                "\n\n"
                "{context}"
            )
            qa_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", qa_system_prompt),
                    ("placeholder", "{chat_history}"),
                    ("human", "{input}"),
                ]
            )
            chain = create_stuff_documents_chain(chat, qa_prompt)
            chain = create_retrieval_chain(retriever, chain)
            print("rag_chain:", chain)
        else:
            system_prompt = (
                "你叫豆瓜，一个帮助人们解答各种问题的助手。"  # 定义AI的自我认知
            )
            normal_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("placeholder", "{chat_history}"),
                    ("human", "{input}"),
                ]
            )
            chain = normal_prompt | chat | streaming_parse  # 创建基础链条

        # 创建一个带聊天记忆的链条
        memoryed_chain = RunnableWithMessageHistory(
            chain,
            lambda session_id: self.__chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        print("开始创建 memoryed_chain")

        return memoryed_chain

    # 创建知识库检索器
    def get_retrievers(self, collections):
        retrievers = []
        for collection in collections:
            if collection is None:
                continue
            print("collection:", collection)
            colleciton_name = get_md5(collection)
            print("知识库名字md5:", colleciton_name)
            if colleciton_name not in self.__retrievers:
                return None
            retriever = self.__retrievers[colleciton_name]
            contextualCompressionRetriever = ContextualCompressionRetriever(
                base_compressor=LLMChainFilter.from_llm(self.__llm),
                base_retriever=RePhraseQueryRetriever.from_llm(retriever, self.__llm),
            )
            retrievers.append(contextualCompressionRetriever)

        if len(retrievers) == 0:
            return None

        print("最终检索器列表", ">" * 10, retrievers)

        return EnsembleRetriever(retrievers=retrievers)

    # 进行流式回复
    def stream(self, collections: List[str], question, model, max_length, temperature):
        print(">>>question:", question)
        print(">>>model:", model)
        print(">>>max_length:", max_length)
        print(">>>temperature:", temperature)
        return self.get_chain(collections, model, max_length, temperature).stream(
            {"input": question},
            {"configurable": {"session_id": "unused"}},  # 这个unused应该是和历史有关系
        )
