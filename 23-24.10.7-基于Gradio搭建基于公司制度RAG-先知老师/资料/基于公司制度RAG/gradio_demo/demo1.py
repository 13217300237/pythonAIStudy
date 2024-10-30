import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文本框
    gr.Textbox(label="输入框", placeholder="请输入内容")

demo.launch()