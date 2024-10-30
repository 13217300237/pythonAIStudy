import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个下拉框
    dropdown = gr.Dropdown(choices=["选项1", "选项2", "选项3"], label="选择一个选项")

demo.launch()