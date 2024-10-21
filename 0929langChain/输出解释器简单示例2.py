# from langchain.output_parsers import CommaSeparatedListOutputParser

# # 解析输入
# output_parser = CommaSeparatedListOutputParser().parse("foo ,bar,baz")
# # 自定义输出格式
# formatted_result = "-".join(output_parser)
# print(formatted_result)  # 输出: foo-bar-baz


from langchain_openai import ChatOpenAI
from langchain.output_parsers import DatetimeOutputParser

# 创建一个 DatetimeOutputParser 实例
output_parser = DatetimeOutputParser()
# 创建一个 ChatOpenAI 实例，使用 gpt-4o-mini 模型
llm = ChatOpenAI(model_name="gpt-4o-mini")
# 构造请求字符串
request = "中华人民共和国是什么时候成立的"
format_instructions = output_parser.get_format_instructions()
print("formatInstructions是", format_instructions)
# 构造消息字典
messages = [{"role": "user", "content": f" {request}\n{format_instructions}"}]
# 使用构造的消息调用模型
result = llm.invoke(messages)
# 打印模型的响应内容
print("模型响应:", result)
# 假设 result 有 content 属性
response_text = result.content
parsed_result = output_parser.parse(response_text)
print("解析结果:", parsed_result)
