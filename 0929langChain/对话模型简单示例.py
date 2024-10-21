from langchain_openai import ChatOpenAI

# 创建一个 ChatOpenAI 实例，指定使用的模型为 "gpt-4o-mini"
chat = ChatOpenAI(model="gpt-4o-mini")  # 默认情况下使用gpt-3.5-turbo 模型
# 输出当前实例的模型名称
print(chat.model_name)
# 打印模型对该消息的响应内容
print(chat.invoke("请默写鹅鹅鹅").content)
