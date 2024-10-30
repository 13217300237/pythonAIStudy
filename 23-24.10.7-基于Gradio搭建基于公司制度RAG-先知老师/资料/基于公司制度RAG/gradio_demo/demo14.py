# 导入Gradio库
import gradio as gr

# 创建Gradio应用
with gr.Blocks() as demo:
    # 添加一个HTML元素，显示标题“聊天机器人”，居中显示
    gr.HTML("<h1 align='center'>欢迎使用聊天机器人</h1>")

    # 创建一个聊天机器人界面，设置不显示标签，设置比例为3，并启用复制按钮
    chatbot = gr.Chatbot(show_label=False, scale=3, show_copy_button=True)

    # 创建一个文本框，用于用户输入消息
    user_input = gr.Textbox(placeholder="在这里输入你的消息...", show_label=False)

    # 定义用户输入后返回的响应
    def respond(message):
        # 返回一个包含用户输入和机器人的回复的列表
        return [["我:"+message, f"你: {message}"]]  # 确保返回格式为 [[用户消息, 机器人回复]]

    # 绑定用户输入文本框的提交事件，更新聊天机器人界面
    user_input.submit(fn=respond, inputs=user_input, outputs=chatbot)

# 启动Gradio应用
demo.launch()