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