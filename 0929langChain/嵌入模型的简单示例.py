from langchain_openai import OpenAIEmbeddings

# 创建一个 OpenAIEmbeddings 实例，指定使用的模型 为 "text-embedding-3-large"
embed = OpenAIEmbeddings(
    model="text-embedding-3-large",
)
# 使用 embed 对象嵌入查询文本并保存结果
result1 = embed.embed_query("我是A文档")
print(result1)  # 打印嵌入结果
print(len(result1))  # 打印嵌入结果的长度
# 使用 embed 对象嵌入多个文档并保存结果
result2 = embed.embed_documents(["我是A文 档", "我是B文档"])
print(result2)  # 打印嵌入的文档结果
print(len(result2))  # 打印嵌入文档的数量
print(len(result2[0]))  # 打印第一个文档嵌入结 果的长度
print(len(result2[1]))  # 打印第二个文档嵌入结 果的长度
