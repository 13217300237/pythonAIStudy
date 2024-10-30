import gradio as gr

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