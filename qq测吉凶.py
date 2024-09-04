import json
import os
import requests

from openai import OpenAI

api_key = "xk-3c1666dd4a5911efa8a900163e082994caadfccb65c243c9"
base_url = "https://openai.zhixueyouke.cn/v1/"


client = OpenAI(api_key=api_key, base_url=base_url)


prompt = "测一下这个qq号 545679452 的吉凶?"

# 先定义一个外部方法，查询一个qq号的吉凶

qqJixiongUrl = (
    "https://api.yuanfenju.com/index.php/v1/Jixiong/qq?api_key={api_key}&qq=${qq}"
)

myQQ = "545679452999"


def queryQQJixiong(qqNumber):
    url = qqJixiongUrl.format(api_key="RKoilS8orozOxFhBwLiJKUg86", qq=qqNumber)
    response = requests.get(url).json()
    print('\n queryQQJixiong 的查询结果是：', response)
    return json.dumps(response, ensure_ascii=False)


# 然后，准备message和tools
messages = []  # 提示词

messages.append(
    {
        "role": "system",
        "content": "你是一个查询qq号吉凶的机器人,你要将用户输入的qq号码调用 查询qq号吉凶的函数来告诉用户他qq号的吉凶情况",
    },
)
messages.append(
    {
        "role": "user",
        "content": f"""我的qq号 {myQQ} 的吉凶情况如何?""",
    }
)

# 准备FunctionCalling的工具链
tools = [
    {
        "type": "function",
        "function": {
            "name": "queryQQJixiong",
            "description": "查询qq号吉凶",
            "parameters": {
                "type": "object",
                "properties": {
                    "qqNumber": {
                        "type": "string",
                        "description": "qq号码,比如545679452",
                    },
                },
                "required": ["qqNumber"],
            },
        }
    }
]


# 将tools传入到openAI的client


# 没有调用外部API功能时
def get_completion(model="gpt-3.5-turbo"):
    print('预先调用的提示词：\n', messages, '\n')
    responses = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
    )
    return responses.choices[0].message


def get_completion2(messages, model="gpt-3.5-turbo"):
    print('真正的调用提示词：\n', messages, '\n')
    responses = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return responses.choices[0].message.content


# print(queryQQJixiong("545679452"))
firstMessage = get_completion()
print('第一次调用后的message:', firstMessage)
messages.append(firstMessage)

args = firstMessage.tool_calls[0].function.arguments
print('args 是 ', args)

args = json.loads(args)

print('qqNumber是', args['qqNumber'])

qqNumber = args['qqNumber']

print('qqNumber的类型是 ', type(qqNumber))

messages.append(
    {
        "tool_call_id": firstMessage.tool_calls[0].id,
        "role": "tool",  # 表示是function call
        "name": firstMessage.tool_calls[0].function.name,
        "content": queryQQJixiong(args['qqNumber']),
    }
)

response = get_completion2(messages)

print(response)
