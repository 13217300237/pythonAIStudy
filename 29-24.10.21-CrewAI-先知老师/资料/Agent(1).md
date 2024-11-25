# CrewAI

## 1. CrewAI的介绍

- CrewAI 是一个创新的开源框架，旨在促进复杂的多Agent人工智能系统的创建。
- CrewAI 的设计旨在使 AI Agent能够承担角色、共享目标，并在一个紧密合作的团队中运作
- 与其他Agent框架对比
  - **Autogen**: 虽然 Autogen 在创建能够协同工作的对话代理方面表现良好，但它缺乏内在的过程概念。在 Autogen 中，协调代理之间的互动需要额外的编程，随着任务规模的增长，这可能变得复杂且繁琐。
  - **ChatDev**: ChatDev 将过程的概念引入了 AI Agent的领域，但其实现相当僵化。ChatDev 的定制选项有限，且不适合生产环境，这可能会妨碍在实际应用中的可扩展性和灵活性。
- **CrewAI 的优势**: CrewAI 的构建考虑到了生产。它结合了 Autogen 对话代理的灵活性和 ChatDev 结构化过程的方法，但没有僵化的限制。CrewAI 的过程设计为动态和可适应的，能够无缝融入开发和生产工作流程中。
- 仓库地址
  - [CrewAI官网](https://docs.crewai.com/introduction)
  - [CrewAI GitHub](https://github.com/crewAIInc/crewAI?tab=readme-ov-file)
  - [CrewAI GitHub中文地址](https://github.com/hypier/crewAI_docs_cn)
- 核心组件
  - 代理（Agent）：负责执行特定任务的个体，具备独特的个性和技能，能够根据情况作出决策。
  - 任务（Task）：设定明确的目标和要求，通过细化的小任务来确保工作顺利进行，便于管理和评估。
  - 工具（Tools）：为完成任务提供必要的支持和资源，依据需求进行定制，以提升工作效率。
  - 流程（Process）：定义任务执行的步骤，包括任务分解、资源分配和沟通协调，确保各环节有序进行。
  - 执行者（Crew）：在CrewAI框架下，负责具体任务的实际执行，连接代理、任务和流程，推动整体目标的实现。
- Agent参数介绍
  - role => 角色
  - goal => 目标
  - backStory => 背景信息
  - verbose => 日志输出
  - allow_delegation => 是否与其他Agent协同
  - tools => 引入工具
- Task参数介绍
  - description：任务的详细描述，说明任务要求。
  - expected_output：期望的任务输出格式和内容。
  - agent：指定负责该任务的代理。

## 2. Crew的基本使用

- Crew的基本使用

> 示例

```python
# 导入必要的模块和类
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"

# 初始化搜索工具，使用 SerperDevTool 实现一个搜索功能的工具实例。
# 注意这里的环境变量名是 SERPER_API_KEY
search_tool = SerperDevTool()

# 定义第一个代理（chef），其角色为专业厨师，负责设计和制作青椒炒肉。
# role: 代理的角色名称。
# goal: 代理的目标描述。
# backstory: 为代理创建背景故事，描述其经验和技能。
# verbose: 控制日志输出的详细程度。
# allow_delegation: 控制是否允许代理委派任务。
# tools: 定义代理使用的工具，这里传递了上面创建的 search_tool 工具。
chef = Agent(
  role='专业厨师',
  goal='设计并制作一道美味的青椒炒肉',
  backstory="""您是一位经验丰富的大厨，擅长中式烹饪。您对食材的选择和调味有独到的见解。""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool]  # 假设厨师可能需要搜索一些食材或食谱信息。
)

# 定义第二个代理（prepper），其角色为厨房助手，负责准备青椒炒肉所需的食材。
# role: 代理的角色名称。
# goal: 代理的目标描述。
# backstory: 为代理创建背景故事，描述其经验和技能。
# verbose: 控制日志输出的详细程度。
# allow_delegation: 设置为False，表示不允许此代理将其任务委派给其他代理或进程。
prepper = Agent(
  role='厨房助手',
  goal='高效准确地准备青椒炒肉所需的食材',
  backstory="""您是厨房的得力助手，确保所有食材都准备好，以便主厨能够顺利制作菜肴。您注重细节，效率高。""",
  verbose=True,
  allow_delegation=False
)

# 创建第一个任务（task1），该任务将分配给 prepper 代理。
# description: 任务的详细描述，说明任务要求。
# expected_output: 期望的任务输出格式和内容。
# agent: 指定负责该任务的代理，这里是 prepper。
task1 = Task(
  description="""准备青椒炒肉所需的食材。
  包括青椒、瘦猪肉、蒜末、生姜等。
  确保所有食材都清洗干净并切成适当大小。""",
  expected_output="所有青椒炒肉所需的食材都已准备就绪",
  agent=prepper
)

# 创建第二个任务（task2），该任务分配给 chef 代理。
# description: 描述任务的要求。
# expected_output: 期望的输出为一道美味的青椒炒肉。
# agent: 指定 chef 代理负责该任务。
task2 = Task(
  description="""根据准备好的食材制作青椒炒肉。
  确保火候适中，调味恰当，最终成品色香味俱佳。""",
  expected_output="一道美味的青椒炒肉",
  agent=chef
)

# 创建一个团队（crew），并将之前创建的代理（chef 和 prepper）和任务（task1 和 task2）分配给它。
# agents: 团队的代理列表。
# tasks: 团队的任务列表。
# verbose: 设置日志输出详细程度（2 表示详细输出）。
# process: 定义任务处理的流程，这里设置为 sequential（顺序执行）。
crew = Crew(
  agents=[prepper, chef],
  tasks=[task1, task2],
  verbose=True,
  process=Process.sequential
)

# 启动团队的任务执行流程。
# kickoff(): 开始执行团队的任务，任务将按顺序执行，并返回最终的结果。
result = crew.kickoff()

# 输出团队执行任务的结果。
# 打印结果，查看任务执行的情况和最终成果。
print("######################")
print(result)
```

## 3. 基于crew实现多Agent协同邮件推送

- Agent
  - 经理安排出差工作，指定出差人员和任务。
  - 审核和批准出差申请。
  - 编写出差通知并准备出差，最终发送邮件。
- Task
  - 先知出差至河北
    - 汇视威员工先知将赴河北出差，需协助：
      - 预订带网络和工作区的房间。
      - 准备洗漱用品、毛巾、床单。
      - 提供笔记本电脑和工作文档。
  - 批准。理由：出差需求合理，符合公司政策。
    - 审核并决定是否批准出差申请。
    - 如果批准，提供详细的批准理由；
    - 如果不批准，说明原因。
  - 邮件已经发送,准备出差
    - 主题：河北出差通知
    - 日期：2024-10-22~2024-12-22
    - 出差人员：先知
    - 目的地：河北
    - 出差岗位：AI大模型研发
    - 联系方式或者电话：176XXXX8801
    - 邮箱：123456@qq.com

### 3.1 邮件服务

```python
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib

def send_message():
    # 发件人
    name = "先知"
    # 发件邮箱
    user = "371900521@qq.com"
    # 发件邮箱授权码，注意不是QQ邮箱密码
    passwd  = "axnfiiqeefwqbgic"
    # 收件邮箱
    to_addr = "734846636@qq.com"
    # 邮件标题
    title = "关于加班"
    # 邮件正文
    # 书信路径
    message = r"尊敬的XXX，感谢您对我的信任，并考虑让我参与这个重要的工作任务。我非常理解这项工作的紧迫性，也希望为公司贡献更多力量。然而，由于个人安排，我今天可能无法加班完成任务。我会确保明天尽早投入到这项工作中，并努力在规定时间内完成。如果有其他的安排或替代方案，我愿意协助。非常抱歉给您带来不便，也感谢您的理解。祝您工作顺利！此致，XXX"

    # MIMEText三个主要参数
    # 1. 邮件内容
    # 2. MIME子类型，plain表示text类型
    # 3. 邮件编码格式，使用"utf-8"避免乱码
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr([name, user])
    # 邮件的标题
    msg['Subject'] = title
    # 接收方
    msg['To'] = to_addr

    try:
        # 不能直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
        # 使用加密过的SMTP_SSL来实例化，它负责让服务器做出具体操作，它有两个参数
        # 第一个是服务器地址，但它是bytes格式，所以需要编码
        # 第二个参数是服务器的接受访问端口，SMTP_SSL协议默认端口是465
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
        # 使用授权码登录QQ邮箱
        smtp.login(user, passwd)
        # 使用sendmail方法来发送邮件，它有三个参数
        # 第一个是发送地址
        # 第二个是接受地址，是list格式，可以同时发送给多个邮箱
        # 第三个是发送内容，作为字符串发送
        smtp.sendmail(user, [to_addr], msg.as_string())
        print('发送成功')
        # 无论发送成功还是失败都要退出你的QQ邮箱
        smtp.quit()
    except Exception as e:
        print('发送失败')

# 发送邮件
send_message()
```

- `@tool`在LangChain的环境下这个方法被作为工具使用
  - 其相当于智能体当中的一个自定义工具
  - 使用`tools`装饰器需要提供相关描述或文档字符串

### 3.2 trip_tools

- 自定义tools工具,提供给Agent调用

> 示例

```python
from langchain.tools import tool
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from typing import Any
import json

class email_tools:
    @tool("send_email")
    def send_message(message: Any) -> str:
        """
        接受一个任意数据类型
        """
        print("开始发送邮件+++++++++++++++++++++++++++++++++++++++++++++++==")
        print(message)
        print("开始发送邮件+++++++++++++++++++++++++++++++++++++++++++++++==")

        # 发件人信息
        name = "先知"
        user = "371900521@qq.com"
        passwd = "bgxxzdjqxlglbjdf"
        to_addr = "734846636@qq.com"
        title = "出差到河北的邮件发送"

        # 将 message 转换为字符串
        # if isinstance(message, dict):
        #     message_str = json.dumps(message, ensure_ascii=False)
        # elif isinstance(message, str):
        #     message_str = message
        # else:
        #     message_str = str(message)

        # 创建邮件对象
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr([name, user])
        msg['Subject'] = title
        msg['To'] = to_addr

        try:
            # 使用加密过的SMTP_SSL来实例化
            smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)
            # 登录QQ邮箱
            smtp.login(user, passwd)
            # 发送邮件
            smtp.sendmail(user, [to_addr], msg.as_string())
            return '发送成功'
            # 退出邮箱
            smtp.quit()
        except Exception as e:
            return f'发送失败: {e}'

# if __name__ == "__main__":
#     email_tool = email_tools()
#     result = email_tool.send_message("这是一封关于出差的通知邮件。")
#     print(result)
```

### 3.3 main

- Agent的整体任务与功能

> 示例

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from trip_tools import email_tools

client = ChatOpenAI(
    model="gpt-4o-mini"
)

leader_agent = Agent(
    role='经理:小刘',
    goal='安排出差工作，指定出差人员和任务。',
    backstory="""你是一位公司的高级管理人员，负责安排员工的出差工作。你需要提出具体的出差需求，包括出差人员、目的地、时间和任务。""",
    verbose=True,
    allow_delegation=False,
    llm=client,
)

hr_agent = Agent(
    role='人事:小张',
    goal='审核和批准出差申请。',
    backstory="""你是一位人事经理，负责审核和批准员工的出差申请。你需要仔细检查领导提出的出差需求，并决定是否批准。如果批准，提供详细的批准理由；如果不批准，说明原因。""",
    verbose=True,
    allow_delegation=False,
    llm=client,
)


emp_agent = Agent(
    role='出差:先知',
    goal='编写出差通知并准备出差，最终发送邮件。',
    backstory="""你是一位出差工作者，擅长AI大模型相关的研发工作。你需要根据领导和人事的批准，编写详细的出差通知，并准备出差所需的各项事宜。最后，将通知通过邮件发送给相关人员。""",
    verbose=True,
    allow_delegation=True,
    tools=[email_tools.send_message],
    llm=client,
)


# 定义任务期望输出
leader_task_expected_output = f"""\n
汇视威员工先知将赴河北出差，需协助：

预订带网络和工作区的房间。
准备洗漱用品、毛巾、床单。
提供笔记本电脑和工作文档。

感谢支持！"""
# 创建任务实例
leader_task = Task(
    description=f"先知出差至河北",
    agent=leader_agent,
    expected_output=leader_task_expected_output,
    output_file="leader.txt",
)

# 为人事实例化任务
hr_task = Task(
    description=f"""出差需求\n:审核并决定是否批准出差申请。\n如果批准，提供详细的批准理由；\n如果不批准，说明原因。""",
    agent=hr_agent,
    expected_output="""批准。理由：出差需求合理，符合公司政策。""",
    output_file="hr.txt",
)

# emp_name = input("请输入出差的姓名")
# emp_addr = input("请输入出差的地址")
# emp_time = input("请输入出差的时间")
# emp_work = input("请输入出差的岗位")
emp_name = "先知"
emp_addr = "河北"
emp_time = "2024-10-22~2024-12-22"
emp_work = "AI大模型研发"

emp_task_description = f"""
主题：河北出差通知
日期：{emp_time}
出差人员：{emp_name}
目的地：{emp_addr}
出差岗位：{emp_work}
联系方式或者电话：176XXXX8801
邮箱：123456@qq.com
... ...
"""
emp_task = Task(
    description=emp_task_description,
    agent=emp_agent,
    expected_output="""邮件已经发送,准备出差""",
    output_file="emp.txt",
)
# 实例化你的团队并使用顺序流程
crew = Crew(
    agents=[leader_agent,hr_agent,emp_agent],
    tasks=[leader_task,hr_task,emp_task],
    verbose=True,
    process=Process.sequential,
)
# 启动你的团队工作！
result = crew.kickoff()
print(result)
```

## 4. ollama运行crew

### 4.1 langchain中接入ollama

- ollama_base

> 示例

```python
import ollama
res=ollama.chat(
    model="qwen2:1.5b",
    stream=False,
    messages=[{"role": "user","content": "请背诵鹅鹅鹅"}],
    options={"temperature":0}
)
print(res["message"]["content"])
```

- ollama_langchain

> 示例

```python
from langchain_community.llms import Ollama
host="127.0.0.1"
port="11434" #默认的端口号为11434
llm = Ollama(
    base_url=f"http://{host}:{port}",
    model="llama3.1:8b",
    temperature=0
)
res=llm.invoke("请背诵鹅鹅鹅")
print(res)
```

- ollama_langchain_chat

> 示例

```python
from langchain_community.llms import Ollama
import json
# 定义 Ollama 文本生成模型的主机和端口
host = "127.0.0.1"
port = "11434"  # 默认的端口号为11434
# 初始化 Ollama 文本生成模型实例
llm = Ollama(
    base_url=f"http://{host}:{port}",
    model="llama3.1:8b",
    temperature=0
)
# 构建完整的消息列表
messages = [
    {"role": "system","content": "你是一个诗人"},
    {"role": "user", "content": "请背诵鹅鹅鹅"}
]
# 将消息列表转换为字符串，以便传递给模型
messages_str = json.dumps(messages, ensure_ascii=False)
# 如果不支持，则需要直接发送 prompt
response = llm.invoke(messages_str)
print(response)
```

### 4.2 crew框架接入ollama模型

> 示例

```python
import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_community.llms import Ollama
# 定义 Ollama 文本生成模型的主机和端口
host = "127.0.0.1"
port = "11434"  # 默认的端口号为11434
# 初始化 Ollama 文本生成模型实例
llm = Ollama(
    base_url=f"http://{host}:{port}",
    model="llama3.1:8b",
    temperature=0
)
# 初始化搜索工具，使用 SerperDevTool 实现一个搜索功能的工具实例。

os.environ["SERPAPI_API_KEY"] = "cfe4242ca57fac7a016555c8ea000e9a58def10692e08f7f8c5cddf6b79d5ae6"
search_tool = SerperDevTool()

# 定义第一个代理（chef），其角色为专业厨师，负责设计晚餐菜单。
# role: 代理的角色名称。
# goal: 代理的目标描述。
# backstory: 为代理创建背景故事，描述其经验和技能。
# verbose: 控制日志输出的详细程度。
# allow_delegation: 控制是否允许代理委派任务。
# tools: 定义代理使用的工具，这里传递了上面创建的 search_tool 工具。

chef = Agent(
  role='专业厨师',
  goal='设计创新且美味的晚餐菜单',
  backstory="""您是一位经验丰富的大厨，擅长将传统风味与现代烹饪技巧相结合。
  您总是寻找新的灵感来创造独特的菜品。""",
  verbose=True,
  allow_delegation=True,
  tools=[search_tool],  # 假设厨师可能需要搜索一些食材或食谱信息。
  llm=llm
)

# 定义第二个代理（prepper），其角色为厨房助手，负责准备食材。
# role: 代理的角色名称。
# goal: 代理的目标描述。
# backstory: 为代理创建背景故事，描述其经验和技能。
# verbose: 控制日志输出的详细程度。
# allow_delegation: 控制是否允许代理委派任务。
prepper = Agent(
  role='厨房助手',
  goal='高效准确地准备所需食材',
  backstory="""您是厨房的得力助手，确保所有食材都准备好，以便主厨能够顺利制作菜肴。
  您注重细节，效率高。""",
  verbose=True,
  allow_delegation=False,
  llm=llm
)

# 创建第一个任务（task1），该任务将分配给 chef 代理。
# description: 任务的详细描述，说明任务要求。
# expected_output: 期望的任务输出格式和内容。
# agent: 指定负责该任务的代理，这里是 chef。
task1 = Task(
  description="""设计一份秋季特色晚餐菜单。
  菜单应该包含前菜、主菜和甜点，
  并考虑季节性和食材的可获得性。""",
  expected_output="详细的晚餐菜单，包括每道菜的名称和简要描述",
  agent=chef
)

# 创建第二个任务（task2），该任务分配给 prepper 代理。
# description: 描述任务的要求。
# expected_output: 期望的输出为所有所需食材都已准备就绪。
# agent: 指定 prepper 代理负责该任务。
task2 = Task(
  description="""根据晚餐菜单准备所有需要的食材。
  清洗、切割蔬菜，解冻肉类，预处理海鲜等。
  确保所有食材都按照主厨的要求准备好。""",
  expected_output="所有晚餐菜单上的食材都已准备就绪",
  agent=prepper
)

# 创建一个团队（crew），并将之前创建的代理（chef 和 prepper）和任务（task1 和 task2）分配给它。
# agents: 团队的代理列表。
# tasks: 团队的任务列表。
# verbose: 设置日志输出详细程度（2 表示详细输出）。
# process: 定义任务处理的流程，这里设置为 sequential（顺序执行）。
crew = Crew(
  agents=[chef, prepper],
  tasks=[task1, task2],
  verbose=True,
  process=Process.sequential
)

# 启动团队的任务执行流程。
# kickoff(): 开始执行团队的任务，任务将按顺序执行，并返回最终的结果。
result = crew.kickoff()

# 输出团队执行任务的结果。
# 打印结果，查看任务执行的情况和最终成果。
print("######################")
print(result)
```







