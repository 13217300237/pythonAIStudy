from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
import datetime
import time


memoryList = []

# 加载线上文档
loader = WebBaseLoader("https://juejin.cn/post/7308289054029037607")
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# 文档内容向量化
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# k is the number of chunks to retrieve
retriever = vectorstore.as_retriever(k=4)


def log(*args):
    # 获取当前时间并格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 将所有传入的参数连接成一个字符串
    message = " ".join(map(str, args))
    # 打印时间戳和日志消息
    print(f"[{current_time}] {message}")


def typewriter_effect_array(texts, delay=0.01):
    for text in texts:
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
    print()  # 在每个字符串结束后换行
    time.sleep(delay * 2)  # 在每个字符串之间暂停一会儿


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
    log("AI正在思考......")
    result = document_chain.stream(
        {
            "context": docs,
            "messages": memoryList,
        }
    )
    typewriter_effect_array(result)
    memoryList.append(AIMessage("".join(result)))


if __name__ == "__main__":
    log("聊天机器人已启动，输入 exit退出")
    while True:
        # 接收用户输入
        user_input = input("用户提问：")

        # 检查用户输入是否为 "exit"
        if user_input.lower() == "exit":
            print("程序已退出。")
            break
        ask(user_input)
