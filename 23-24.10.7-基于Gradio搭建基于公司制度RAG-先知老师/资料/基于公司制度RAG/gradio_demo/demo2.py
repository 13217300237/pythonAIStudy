import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个按钮
    gr.Button("提交")

demo.launch()