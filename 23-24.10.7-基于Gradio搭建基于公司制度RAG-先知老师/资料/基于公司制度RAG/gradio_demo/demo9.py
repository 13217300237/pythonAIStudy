import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])

demo.launch()