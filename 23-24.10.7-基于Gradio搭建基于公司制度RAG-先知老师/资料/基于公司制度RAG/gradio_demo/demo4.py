import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个滑块
    slider = gr.Slider(minimum=0, maximum=100, value=50, label="选择数值")

demo.launch()