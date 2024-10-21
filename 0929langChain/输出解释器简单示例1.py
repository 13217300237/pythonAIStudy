# 导入CommaSeparatedListOutputParser包，这个 包是用来解析以逗号分隔的字符串，并将其转换为列表
from langchain.output_parsers import CommaSeparatedListOutputParser

# 创建 CommaSeparatedListOutputParser 实例
output_parser = CommaSeparatedListOutputParser()
# 获取格式说明并打印
output_parser.get_format_instructions()
print(output_parser.get_format_instructions())
# 定义一个包含逗号分隔值的回复
reply = "foo,bar,baz"
# 解析回复并打印解析结果
print("***********************")
print(output_parser.parse(reply))  # 打印解 析后的结果
