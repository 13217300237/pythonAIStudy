import gradio as gr

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个聊天机器人界面
    gr.Chatbot(label="聊天窗口")

demo.launch()