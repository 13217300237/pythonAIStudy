# 实现的效果，
# 1. 要类似 ollama 的多轮对话的效果
# 2. 并且要能够支持加载外部知识库
# 3. 并且要实现对话上下文记忆

# 先来一个基本效果，创建模型，结果解析器，以及 提示词，直接用 langChain来写


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.output_parsers import MarkdownListOutputParser
from langchain.prompts.chat import HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_from_dict, messages_from_dict
from langchain.chains.conversation.memory import ConversationBufferMemory
import datetime


def log(*args):
    # 获取当前时间并格式化为字符串
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 将所有传入的参数连接成一个字符串
    message = " ".join(map(str, args))
    # 打印时间戳和日志消息
    print(f"[{current_time}] {message}")


# 基本测试
def base():
    # 创建大模型
    llm = ChatOpenAI(model="gpt-4o-mini")

    print("llm的名字是", llm.get_name())

    # 结果解析器
    output_parser = MarkdownListOutputParser()

    print("output_parser是", output_parser.get_name())

    # 创建提示词
    # 设计一些问题，那就还是关于民法典的吧
    chat_prompt = ChatPromptTemplate.from_messages(
        [HumanMessagePromptTemplate.from_template("{request} \n {format_instruction}")]
    )

    model_request = chat_prompt.format_prompt(
        request="民法典是什么？", format_instruction=output_parser
    )

    print("开始invoke")
    result = llm.invoke(model_request)
    print("=-========")
    print("格式化之前的结果是：\n", result.content)
    print("=-========")
    print(
        "格式化之后等结果是：\n", output_parser.parse(result.content)
    )  # 格式化之后的结果居然是空的


# 获取提示词
def get_prompt():
    # 定义一个模版，用于生成聊天提示
    template = """
    仅根据上下文回答问题：
    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt


# 获得检索器
def get_rag_retriever():
    filePath = "作业/实验室守则.pdf"
    log("开始检索文档...", filePath)
    loader = PyPDFLoader(filePath)
    documents = loader.load()
    # 切分文档，并且向量化
    page_spliter = CharacterTextSplitter(
        chunk_size=100, chunk_overlap=5
    )  # 创建文档分隔器
    texts = page_spliter.split_documents(documents)  # 进行分割
    embed = OpenAIEmbeddings()
    db = FAISS.from_documents(texts, embed)
    retriever = db.as_retriever(search_kwargs={"k": 1})
    # 下面是测试代码
    # result = retriever.invoke("简要描述李华先生的病史")
    # print("简要描述李华先生的病史 ----  文档检索的结果是：")
    # for doc in result:
    #     content = doc.page_content
    #     print(content)
    log("文档检索器生成完毕...")
    return retriever


# 创建大模型
def get_llm():
    return ChatOpenAI(model="gpt-4o-mini")


# 获得结果解析器
def get_output_parser():
    return StrOutputParser()


# 在 Python 文件中定义一个 main 函数是一个常见的做法，尤其是当你想要将程序的执行逻辑与函数逻辑分开时。
# 一个标准的做法是使用 if __name__ == "__main__": 结构来确保 main 函数只在脚本直接运行时执行，而不是作为模块导入时执行。
if __name__ == "__main__":

    # 创建历史记录
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    rag_retriever = get_rag_retriever()

    # 无限循环，直到用户输入 "exit"
    while True:
        # 接收用户输入
        user_input = input("用户提问（输入 'exit' 退出）：")

        # 检查用户输入是否为 "exit"
        if user_input.lower() == "exit":
            print("程序已退出。")
            break

        # 调用chain进行输出
        chain = (
            RunnableParallel(
                {"context": rag_retriever, "question": RunnablePassthrough()}
            )
            | (
                lambda x: {
                    "context": x["context"],
                    "question": x["question"],
                    "chat_history": memory.load_memory_variables({})["chat_history"],
                }
            )
            | get_prompt()
            | get_llm()
            | get_output_parser()
        )
        log("AI正在思考...")
        result = chain.invoke(user_input)  # 将查询传递给链
        log("AI回复:", result)  # 现在基本实现了从文档中检索结果
        # 保存当前对话到历史记录
        memory.save_context({"input": user_input}, {"output": result})
