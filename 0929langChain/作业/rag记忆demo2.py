from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage

memoryList = []

# 加载线上文档
loader = WebBaseLoader("https://doc.yuanfenju.com/")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# 文档内容向量化
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# k is the number of chunks to retrieve
retriever = vectorstore.as_retriever(k=4)


def ask(question):
    memoryList.append(HumanMessage(question))

    docs = retriever.invoke(question)

    SYSTEM_TEMPLATE = """
    基于上下文来回答问题，如果上下文中没有提及，你不要瞎扯，直接说“不知道”即可。

    <context>
    {context}
    </context>
    """

    question_answering_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_TEMPLATE,
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chat = ChatOpenAI(model="gpt-4o-mini")
    document_chain = create_stuff_documents_chain(chat, question_answering_prompt)

    result = document_chain.invoke(
        {
            "context": docs,
            "messages": memoryList,
        }
    )

    print("AI的回答是", result)
    memoryList.append(AIMessage(result))


if __name__ == "__main__":
    ask("缘分居能做什么")
    ask("缘分居能测评qq号吉凶么")
    ask("我刚才问了你什么问题")
