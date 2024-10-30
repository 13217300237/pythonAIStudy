# Gradio

[官网](https://www.gradio.app/docs/gradio/interface)

## 1. 认识Gradio

Gradio 是一个开源 Python 库，用于轻松构建和分享机器学习应用。通过它，开发者能够快速为机器学习模型创建用户界面，并将模型部署为 Web 应用。Gradio 不仅适用于机器学习模型，也可以用来创建其他与 Python 相关的交互式应用程序。

## 2. Gradio 基本组件

### 2.1 gr.Textbox：文本输入框

- `gr.Textbox()`：创建一个文本输入框，可以设置标签和占位符。


> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文本框
    gr.Textbox(label="输入框", placeholder="请输入内容")

demo.launch()
```

### 2.2 gr.Button：按钮

- `gr.Button()`：创建一个按钮，可以用于绑定点击事件。

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个按钮
    gr.Button("提交")

demo.launch()
```

- 点击事件

> 示例

```python
import gradio as gr

def on_button_click(value):
    # 返回按钮点击后的反馈信息，这里包含了输入的值
    return "您输入的是：" + value

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文本框用于接收用户的输入
    input_text = gr.Textbox(label="输入")
    # 创建一个按钮
    submit_button = gr.Button("提交")
    # 创建一个文本框用于显示结果
    output_text = gr.Textbox(label="输出")
    # 将按钮点击事件与处理函数绑定
    submit_button.click(fn=on_button_click, inputs=input_text, outputs=output_text)
# 启动应用
demo.launch()
```

### 2.3 gr.Slider：滑块

- `gr.Slider(minimum, maximum, value)`：允许用户在最小值和最大值之间选择数值，并提供默认值。

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个滑块
    slider = gr.Slider(minimum=0, maximum=100, value=50, label="选择数值")

demo.launch()
```

- change事件
  - change => 当滑块移动的时候
  - `interactive=True` 使得该组件（如滑块、按钮等）能够接收用户的交互操作。

> 示例

```python
import gradio as gr

# 定义处理函数，接收滑块的值并返回
def get_slider_value(value):
    return f"你选择的数值是：{value}"

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个滑块
    slider = gr.Slider(minimum=0, maximum=100, value=50, label="选择数值", interactive=True)
    # 创建一个文本框用于显示结果
    output = gr.Textbox(label="结果")
    # 通过滑块值更新文本框
    slider.change(fn=get_slider_value, inputs=slider, outputs=output)

# 启动应用
demo.launch()
```

- 文本框和滑块的简单交互

> 示例

```python
# 导入Gradio库，用于创建Web应用程序
import gradio as gr

# 定义一个处理输入的函数，接受一个名字和一个数字，返回格式化的字符串
def greet(name, age):
    return f"你好, {name}！你 {age} 岁了。"

# 使用Gradio的Blocks创建界面
with gr.Blocks() as demo:
    # 创建一行，用于放置输入组件
    with gr.Row():
        name_input = gr.Textbox(label="请输入你的名字")  # 文本框输入组件
        age_input = gr.Slider(minimum=0, maximum=120, label="选择你的年龄",interactive=True)  # 滑块输入组件

    # 创建输出组件
    output = gr.Textbox(label="输出结果")  # 输出文本框

    # 添加一个按钮，用户点击后调用greet函数
    btn = gr.Button("提交")  # 创建一个提交按钮

    # 绑定按钮点击事件
    btn.click(greet, inputs=[name_input, age_input], outputs=output)  # 设置点击按钮后调用的函数及其输入输出

# 启动Gradio应用程序
demo.launch()
```

### 2.4 gr.Dropdown：下拉框

- `gr.Dropdown(choices)`：创建下拉框，`choices`定义可选项列表

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个下拉框
    dropdown = gr.Dropdown(choices=["选项1", "选项2", "选项3"], label="选择一个选项")

demo.launch()
```

- 下拉框案例

> 示例

```python
# 导入Gradio库
import gradio as gr

# 定义下拉框的选项，使用表情符号表示不同的水果
choices = ["🍎🍎🍎", "🍌🍌🍌", "🍑🍑🍑"]

# 创建Gradio应用
with gr.Blocks() as demo:
    # 添加一个HTML元素，显示标题“选择你的水果”，居中显示
    gr.HTML("<h1 align='center'>选择你的水果</h1>")

    # 创建一个行布局，用于排列下拉框
    with gr.Row():
        # 创建一个下拉菜单，供用户选择水果
        fruit_dropdown = gr.Dropdown(
            choices=choices,  # 设置下拉框的选项为定义的水果列表
            label="请选择一种水果",  # 下拉框的标签
            interactive=True,  # 允许用户交互
            value=choices[2]  # 设置默认选择为第三个选项（🍑🍑🍑）
        )

    # 创建一个文本框，用于显示用户选择的水果
    output = gr.Textbox(label="你选择的水果是")  # 文本框的标签

    # 定义选择水果后的回调函数，接受用户选择的水果作为参数
    def display_choice(selected_fruit):
        # 返回一个格式化字符串，显示用户选择的水果
        return f"你选择的水果是: {selected_fruit}"

    # 绑定下拉框的变化事件，当用户选择不同的水果时调用回调函数
    fruit_dropdown.change(
        fn=display_choice,  # 当下拉框变化时调用的函数
        inputs=fruit_dropdown,  # 输入为当前选择的水果
        outputs=output  # 输出为显示选择结果的文本框
    )

# 启动Gradio应用，默认在本地服务器上运行
demo.launch()
```

### 2.5 gr.File：文件上传

- `gr.File()`：允许用户上传文件，可以设置允许的文件类型。
- `file_types`：允许上传的文件类型列表

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])

demo.launch()
```

- 获取上传的文件

> 示例

```python
import gradio as gr

def process_file(file_obj):
    # 获取文件名
    file_name = file_obj.name
    # 处理文件，这里只是简单地返回文件名
    return f"您上传的文件名为: {file_name}"

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    file_upload = gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])

    # 创建一个文本框用于显示结果
    output_text = gr.Textbox(label="输出")

    # 将文件上传事件与处理函数绑定
    file_upload.change(fn=process_file, inputs=file_upload, outputs=output_text)

# 启动应用
demo.launch()
```

- 上传文件校验

> 示例

```python
import gradio as gr
import os

# 允许的文件扩展名列表
allowed_extensions = ['.pdf', '.txt', '.doc']

def process_file(file_obj):
    # 获取文件名和扩展名
    file_name = file_obj.name
    file_extension = os.path.splitext(file_name)[1].lower()
    print("文件上传的后缀名", file_extension)

    if file_extension in allowed_extensions:
        # 处理文件，这里只是简单地返回文件名
        return f"您上传的文件名为: {file_name}"
    else:
        # 如果文件扩展名不在允许的列表中，返回错误信息
        return "不允许的文件类型，请上传 PDF、TXT 或 DOC 文件。"

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    file_upload = gr.File(label="上传文件------pdf', 'txt', 'doc'", file_types=allowed_extensions)

    # 创建一个文本框用于显示结果
    output_text = gr.Textbox(label="输出")

    # 将文件上传事件与处理函数绑定
    file_upload.change(fn=process_file, inputs=file_upload, outputs=output_text)
# 启动应用
demo.launch()
```

- 文件上传保存
  - 使用 `os.getcwd()` 获取当前工作目录。
  - `SAVE_DIR = os.path.join(current_dir, "uploaded_files")` 指定了文件保存的目录，使用当前工作目录下的 `uploaded_files` 子目录。

> 示例

```python
import gradio as gr
import os
import shutil
from pathlib import Path

# 指定保存文件的目录，使用相对路径
SAVE_DIR = "./uploaded_files"

# 确保保存目录存在
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)


def process_file(file_obj):
    if file_obj is None:
        return "未上传文件，请选择一个文件上传。"

    # 获取文件的保存路径
    file_path = file_obj.name  # 使用 .name 获取文件的保存路径

    # 获取原始文件名和扩展名
    original_file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(original_file_name)[1].lower()

    # 允许的文件扩展名列表
    allowed_extensions = ['.pdf', '.txt', '.doc']

    if file_extension in allowed_extensions:
        # 构建新的保存路径
        save_path = os.path.join(SAVE_DIR, original_file_name)

        # 移动文件到指定目录
        shutil.move(file_path, save_path)  # 使用 shutil.move 支持跨磁盘分区移动

        # 返回成功信息
        return f"文件已成功上传并保存到: {save_path}"
    else:
        return "不允许的文件类型，请上传 PDF、TXT 或 DOC 文件。"


# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    file_upload = gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])
    output_text = gr.Textbox(label="输出")

    file_upload.change(fn=process_file, inputs=[file_upload], outputs=output_text)

demo.launch()
```

### 2.6 gr.Chatbot：聊天机器人界面

- `gr.Chatbot`组件用于实现对话型界面，适合聊天机器人或交互式应用。

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个聊天机器人界面
    gr.Chatbot(label="聊天窗口")

demo.launch()
```

- 简单的聊天实现

> 示例

```python
# 导入Gradio库
import gradio as gr

# 创建Gradio应用
with gr.Blocks() as demo:
    # 添加一个HTML元素，显示标题“聊天机器人”，居中显示
    gr.HTML("<h1 align='center'>欢迎使用聊天机器人</h1>")

    # 创建一个聊天机器人界面，设置不显示标签，设置比例为3，并启用复制按钮
    chatbot = gr.Chatbot(show_label=False, scale=3, show_copy_button=True)

    # 创建一个文本框，用于用户输入消息
    user_input = gr.Textbox(placeholder="在这里输入你的消息...", show_label=False)

    # 定义用户输入后返回的响应
    def respond(message):
        # 返回一个包含用户输入和机器人的回复的列表
        return [["我:"+message, f"你: {message}"]]  # 确保返回格式为 [[用户消息, 机器人回复]]

    # 绑定用户输入文本框的提交事件，更新聊天机器人界面
    user_input.submit(fn=respond, inputs=user_input, outputs=chatbot)

# 启动Gradio应用
demo.launch()
```

### 2.7 gr.Row 和 gr.Column：布局管理

- 通过`gr.Row`和`gr.Column`来组织页面上的组件，控制它们的排列方式。
  - `gr.Row()`：用于创建一行，并在其中安排多个组件。
  - `gr.Column(scale)`：用于设置列在行中的占比。

> 示例

```python
import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个行布局
    with gr.Row():
        # 左边的列，占4比重
        with gr.Column(scale=4):
            gr.Textbox(label="左边输入框")
        
        # 右边的列，占1比重
        with gr.Column(scale=1):
            gr.Slider(minimum=0, maximum=100, value=50, label="右边滑块")

demo.launch()
```

### 2.8 多选框选择器

> 示例

```python
import gradio as gr

# 定义处理函数，返回用户选择的结果
def show_choices(choices):
    return f"你选择了: {', '.join(choices)}"

# 创建Gradio应用
with gr.Blocks() as demo:
    # 创建多选框组件
    checkbox_group = gr.CheckboxGroup(
        choices=["苹果", "香蕉", "桃子", "橘子"],
        label="请选择你喜欢的水果"
    )

    # 创建输出文本框
    output = gr.Textbox(label="选择结果")

    # 绑定多选框变化事件，更新输出结果
    checkbox_group.change(fn=show_choices, inputs=checkbox_group, outputs=output)

# 启动Gradio应用
demo.launch()
```

### 2.9 嵌套布局的综合应用

> 示例

```python
import gradio as gr
import matplotlib
matplotlib.use('TkAgg')

# 定义处理函数，返回用户选择的组合结果
def show_choices(fruit, drink):
    return f"你选择了: {fruit} 和 {drink}"

# 创建Gradio应用
with gr.Blocks() as demo:
    # 创建标题
    gr.HTML("<h1 align='center'>选择你的水果和饮料</h1>")

    # 创建嵌套布局
    with gr.Row():
        with gr.Column(scale=2):
            fruit_input = gr.Dropdown(choices=["🍎苹果", "🍌香蕉", "🍑桃子"], label="选择水果")
        with gr.Column(scale=1):
            drink_input = gr.Radio(choices=["咖啡", "茶", "果汁"], label="选择饮料")

    # 创建输出文本框
    output = gr.Textbox(label="你的选择是")

    # 创建按钮，点击后显示选择的结果
    submit_button = gr.Button("提交")
    submit_button.click(fn=show_choices, inputs=[fruit_input, drink_input], outputs=output)

# 启动Gradio应用
demo.launch()
```