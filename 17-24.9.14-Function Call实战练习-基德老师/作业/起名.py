import json
import os
import requests

from openai import OpenAI

api_key = "xk-3c1666dd4a5911efa8a900163e082994caadfccb65c243c9"
base_url = "https://openai.zhixueyouke.cn/v1/"


client = OpenAI(api_key=api_key, base_url=base_url)


prompt = "测一下这个qq号 545679452 的吉凶?"

# 再来试试AI起名


aiQimingUrl = (
    "https://api.yuanfenju.com/index.php/v1/Dafen/qiming?api_key={api_key}&sex={sex}&surname={surname}&page=1&limit=10"
)


def aiQimingFunc(sex, surname):

    print('\n aiQiming 参数是：','\n 你输入的性别是：', sex, '\n 你输入的姓氏是：', surname)

    if (sex == '男'):
        sex = '0'
    elif (sex == '女'):
        sex = '1'
    else:
        sex = '2'

    url = aiQimingUrl.format(
        api_key="RKoilS8orozOxFhBwLiJKUg86", sex=0, surname=surname)
    response = requests.get(url).json()
    print('\n aiQiming 的查询结果是：', response)
    return json.dumps(response, ensure_ascii=False)


# 然后，准备message和tools
messages = []  # 提示词

messages.append(
    {
        "role": "system",
        "content": "你是一个取名字的机器人,用户会输入他宝宝的性别，姓氏，名字， 你的任务是根据他宝宝的信息来给出他宝宝的名字,越多越好。",
    },
)
messages.append(
    {
        "role": "user",
        "content": f"""宝宝的性别是男，姓周，帮我取宝宝的名字。""",
    }
)

# 准备FunctionCalling的工具链
tools = [
    {
        "type": "function",
        "function": {
            "name": "aiQiming",
            "description": "取名字",
            "parameters": {
                "type": "object",
                "properties": {
                    "sex": {
                        "type": "string",
                        "description": "性别，男或者女，或者不限性别",
                    },
                    "surname": {
                        "type": "string",
                        "description": "姓氏，比如张，李",
                    },
                },
                "required": ["sex", 'surname'],
            },
        }
    }
]


# 将tools传入到openAI的client
# 第一次调用
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


firstMessage = get_completion()
print('第一次调用后的message:', firstMessage)
messages.append(firstMessage)

args = firstMessage.tool_calls[0].function.arguments
print('args 是 ', args)

args = json.loads(args)

sex = args['sex']
surname = args['surname']

print('sex是', sex, '\nsurname是', surname)

messages.append(
    {
        "tool_call_id": firstMessage.tool_calls[0].id,
        "role": "tool",  # 表示是function call
        "name": firstMessage.tool_calls[0].function.name,
        "content": aiQimingFunc(sex, surname),
    }
)

response = get_completion2(messages)

print(response)
