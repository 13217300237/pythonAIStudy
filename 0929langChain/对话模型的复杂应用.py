# 假设已经正确导入了必要的模块
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage, ChatMessage

# 创建一个 ChatOpenAI 实例，指定使用的模型为 "gpt-4o-mini"
llm = ChatOpenAI(model="gpt-4o-mini")
# 定义消息列表
messages = [
    SystemMessage(content="描述一个顾客进入饭店并点餐的场景。"),  # 系统消息
    HumanMessage(content="我进入饭店吃饭。"),  # 用户消息
    ChatMessage(role="assistant", content="欢迎光临，请问您几位?"),  # 迎宾
    HumanMessage(content="就我一位，我点菜。"),  # 用户消息
    ChatMessage(role="assistant", content="好的，这边请"),  # 迎宾回应
    HumanMessage(
        content="我想点一份牛肉炒饭，还有一份糖醋排骨。另外，我注意到糖醋排骨的价格比其他 菜品要高一些，为什么呢?"
    ),  # 用户询问
    AIMessage(content="?"),
]  # AI 生成的服务 员回应

# 调用 llm 对象的 invoke 方法，传入消息列表并打印 响应内容
print(llm.invoke(messages).content)
