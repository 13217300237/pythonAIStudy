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