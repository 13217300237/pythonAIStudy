# 导入Gradio库
import gradio as gr

# 定义下拉框的选项，使用表情符号表示不同的水果
choices = ["🍎🍎🍎", "🍌🍌🍌", "🍑🍑🍑"]

# 创建Gradio应用
with gr.Blocks() as demo:
    # 添加一个HTML元素，显示标题“选择你的水果”，居中显示
    gr.HTML("<h1 align='center'>选择你的水果</h1>")

    # 创建一个行布局，用于排列下拉框
    with gr.Row():
        # 创建一个下拉菜单，供用户选择水果
        fruit_dropdown = gr.Dropdown(
            choices=choices,  # 设置下拉框的选项为定义的水果列表
            label="请选择一种水果",  # 下拉框的标签
            interactive=True,  # 允许用户交互
            value=choices[2]  # 设置默认选择为第三个选项（🍑🍑🍑）
        )

    # 创建一个文本框，用于显示用户选择的水果
    output = gr.Textbox(label="你选择的水果是")  # 文本框的标签

    # 定义选择水果后的回调函数，接受用户选择的水果作为参数
    def display_choice(selected_fruit):
        # 返回一个格式化字符串，显示用户选择的水果
        return f"你选择的水果是: {selected_fruit}"

    # 绑定下拉框的变化事件，当用户选择不同的水果时调用回调函数
    fruit_dropdown.change(
        fn=display_choice,  # 当下拉框变化时调用的函数
        inputs=fruit_dropdown,  # 输入为当前选择的水果
        outputs=output  # 输出为显示选择结果的文本框
    )

# 启动Gradio应用，默认在本地服务器上运行
demo.launch()