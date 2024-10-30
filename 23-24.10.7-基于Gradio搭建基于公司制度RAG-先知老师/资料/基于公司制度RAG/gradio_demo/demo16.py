import gradio as gr

# 定义处理函数，返回用户选择的结果
def show_choices(choices):
    return f"你选择了: {', '.join(choices)}"

# 创建Gradio应用
with gr.Blocks() as demo:
    # 创建多选框组件
    checkbox_group = gr.CheckboxGroup(
        choices=["苹果", "香蕉", "桃子", "橘子"],
        label="请选择你喜欢的水果"
    )

    # 创建输出文本框
    output = gr.Textbox(label="选择结果")

    # 绑定多选框变化事件，更新输出结果
    checkbox_group.change(fn=show_choices, inputs=checkbox_group, outputs=output)

# 启动Gradio应用
demo.launch()