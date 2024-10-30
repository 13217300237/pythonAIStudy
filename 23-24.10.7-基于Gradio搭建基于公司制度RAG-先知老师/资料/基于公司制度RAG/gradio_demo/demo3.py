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