from langchain_openai import OpenAI


# 创建一个 OpenAI 实例，指定使用的模型为 "gpt- 3.5-turbo-instruct"
llm = OpenAI(model="gpt-3.5-turbo-instruct")
# 定义输入文本
input_text = "请默写鹅鹅鹅"
# 调用 llm 对象的 invoke 方法，传入输入文本并打印 响应
print(llm.invoke(input_text))
