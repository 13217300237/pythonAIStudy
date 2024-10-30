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