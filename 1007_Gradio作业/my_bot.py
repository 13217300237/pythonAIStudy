import os
import shutil
import gradio as gr
from my_knowledge_base import KNOWLEDGE_DIR, LLM_MODELS
from my_llm import MyLLM


# 实例化MyLLM类，用于后续的模型调用和处理
llm = MyLLM()

# 创建文件存储目录（如果不存在）
if not os.path.exists(KNOWLEDGE_DIR):
    os.makedirs(KNOWLEDGE_DIR)


def user_send(history, user_message):
    print("history:", history)
    print("user_message:", user_message)
    """
    将用户的消息添加到历史记录中，显示用户头像
    :param history: 聊天记录
    :param user_message: 用户消息
    :return: 更新后的聊天记录
    """
    formatted_user_message = f"{user_message}"
    formatted_ai_response = f"AI思考中..."
    history.append((formatted_user_message, formatted_ai_response))
    return history, ""  # 第二个空字符串是为了清空输入框


def process_send(user_message, history):
    """
    发送按钮的点击事件处理函数
    :param user_message: 用户消息
    :param history: 聊天记录
    :return: 更新后的聊天记录和清空的文本框
    """
    if user_message.strip():
        return user_send(history, user_message)
    else:
        return history, ""


def enable_send_button(user_message):
    """
    根据输入内容启用或禁用发送按钮
    :param user_message: 用户消息
    :return: 更新后的按钮状态
    """
    return gr.update(interactive=user_message.strip() != "")


def enable_upload_button(file_paths):
    """
    根据输入内容启用或禁用发送按钮
    :param user_message: 用户消息
    :return: 更新后的按钮状态
    """
    return gr.update(interactive=bool(file_paths))


def enable_clear_button(history):
    """
    根据聊天记录启用或禁用清除按钮
    :param history: 聊天记录
    :return: 更新后的按钮状态
    """
    return gr.update(interactive=bool(history))


def clear_chatbot(msg):
    """
    清除聊天记录
    :param msg: 聊天记录
    :return: 清空后的聊天记录
    """
    return []


# 提交 知识库
# 两个步骤，
# 1，拷贝源文件到项目内
# 2，使用本地模型对项目内刚刚传来的文件向量化，得到向量化后的成果文件
# 3. 把已经向量化的知识库文件展示在UI中
def upload_knowledge_base(file_paths):
    """
    复制指定路径的文件到目标目录

    :param file_paths: 文件路径的数组
    :param target_directory: 文件复制后的目标目录
    """
    unsupported_files = []
    # 在这里判断支持上传的文件类型
    allowed_extensions = [".pdf", ".txt", ".doc"]
    # 如果发现不支持的文件格式，则直接提醒
    for file_path in file_paths:
        # 获取文件扩展名
        _, ext = os.path.splitext(file_path)

        # 检查扩展名是否支持
        if ext.lower() not in allowed_extensions:
            unsupported_files.append(file_path)

    if unsupported_files:
        print("发现不支持的文件格式:")
        for file in unsupported_files:
            print(file)
        s = "\n".join(unsupported_files)
        return (
            None,
            gr.update(
                choices=llm.knowledge_file_embedding(),
                value=[],
            ),
            f"发现不支持的文件 {s}",
        )
    else:
        print("所有文件格式均支持。")

    # 创建目标目录（如果不存在）
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)

    # 遍历文件路径，将文件复制到目标目录
    for file_path in file_paths:
        # 获取文件名
        file_name = os.path.basename(file_path)
        # 目标路径
        target_path = os.path.join(KNOWLEDGE_DIR, file_name)
        try:
            # 复制文件到目标路径
            shutil.copy(file_path, target_path)
            print(f"已复制文件: {file_name} 到 {KNOWLEDGE_DIR}")
        except Exception as e:
            print(f"复制文件 {file_name} 失败: {e}")

    return (
        None,
        gr.update(
            choices=llm.knowledge_file_embedding(),
            value=llm.collections[:1],
        ),
        "",
    )  # copy过来之后直接进行向量化


retrievers = {}  # 已经向量化的文件 这是一个字典，也就是映射


def onTempatureSliderChanged(value):
    return "温度值:" + str(value)


def onTokenCountSliderChanged(value):
    return "token数:" + str(value)


# 直接调用openAI拿AI的回复
# [chat_history] 聊天记录（成对出现的，总是UserMessage，AIMessage）
# [model] 选择的模型
# [temperature] 模型的温度，决定Ai回答的随机性
# [max_length] 模型回复的最大长度
def llm_reply(collections, chat_history, model, temperature, max_length):
    # 获得用户提的最后一个问题
    question = chat_history[-1][0]  # 倒数第一对记录，取0位置，也就是用户发送的内容
    # 使用问答链进行回复
    print("---question:", question)
    print("---model:", model)
    print("---max_length:", max_length)
    print("temperature:", temperature)
    response = llm.stream(collections, question, model, max_length, temperature)
    print("response:", response)
    chat_history[-1][1] = ""  # 先把AI的回复清空
    print("chat_history:", chat_history)

    for chunk in response:
        # print("chunk:", chunk)
        if "context" in chunk:
            for doc in chunk["context"]:
                print("doc:", doc)
        if "answer" in chunk:
            chunk_content = chunk["answer"]
            # print("chunk_content", chunk_content)
            if chunk_content is not None:
                chat_history[-1][1] += chunk_content
                yield chat_history
    print("chat_history")


with gr.Blocks() as demo:
    gr.HTML("<h3 align='left'>欢迎使用聊天机器人</h3>")
    with gr.Row():
        with gr.Column(elem_id="contain_area", elem_classes="contain", scale=4):
            with gr.Row():
                tempatureSlider = gr.Slider(
                    minimum=0, maximum=3, step=0.2, label="温度值"
                )
                replyMaxCountSlider = gr.Slider(
                    minimum=256, maximum=3000, step=5, label="回复的最大长度", value=256
                )
            chatbot_box = gr.Chatbot(
                elem_id="chatbot",
                show_copy_all_button=False,
                show_copy_button=True,
                label="聊天机器人BOT",
                show_share_button=False,
            )
            with gr.Row():
                msg_textbox = gr.Textbox(
                    label="请输入内容",
                    interactive=True,
                    elem_id="input-textbox",
                    scale=3,
                )  # 输入框
                with gr.Column(scale=1):
                    clear_btn = gr.Button("清除历史记录", interactive=False)  # 清除按钮
                    send_btn = gr.Button(
                        "发送", interactive=False, elem_id="send-button"
                    )  # 发送按钮
                    clear_btn.click(
                        fn=clear_chatbot, inputs=None, outputs=[chatbot_box]
                    )
        msg_textbox.change(fn=enable_send_button, inputs=msg_textbox, outputs=send_btn)
        chatbot_box.change(
            fn=enable_clear_button, inputs=chatbot_box, outputs=clear_btn
        )

        with gr.Column(scale=1):
            model_select = gr.Dropdown(
                choices=LLM_MODELS,
                value=LLM_MODELS[0],
                label="大模型选择",
                interactive=True,
                scale=1,
            )
            gr.Markdown("### 知识库")
            konwledge_select = gr.Dropdown(
                choices=llm.knowledge_file_embedding(),
                value=llm.collections,
                label="选择知识库",
                interactive=True,
                scale=1,
                multiselect=True,
            )
            file_upload = gr.File(
                label="选择知识库文件，仅支持 pdf,txt,doc",
                type="filepath",
                file_count="multiple",
            )
            # 处理按钮
            submit_btn = gr.Button("上传知识库", interactive=False)
            err_text = gr.Markdown()
            submit_btn.click(
                fn=upload_knowledge_base,
                inputs=file_upload,
                outputs=[file_upload, konwledge_select, err_text],
            )
            file_upload.change(
                fn=enable_upload_button, inputs=file_upload, outputs=submit_btn
            )
    msg_textbox.submit(
        fn=process_send,
        inputs=[msg_textbox, chatbot_box],
        outputs=[chatbot_box, msg_textbox],
    ).then(
        fn=llm_reply,  # AI回复
        inputs=[
            konwledge_select,
            chatbot_box,
            model_select,
            tempatureSlider,
            replyMaxCountSlider,
        ],  # 输入组件 chatBox聊天历史， model_select 模型选择,tempatureSlider温度选择， replyMaxCountSlider 回复最大长度
        outputs=[chatbot_box],
    )
    send_btn.click(
        fn=process_send,
        inputs=[msg_textbox, chatbot_box],
        outputs=[chatbot_box, msg_textbox],
    ).then(
        fn=llm_reply,  # AI回复
        inputs=[
            konwledge_select,
            chatbot_box,
            model_select,
            tempatureSlider,
            replyMaxCountSlider,
        ],  # 输入组件 chatBox聊天历史， model_select 模型选择,tempatureSlider温度选择， replyMaxCountSlider 回复最大长度
        outputs=[chatbot_box],
    )

# 启动 Gradio 应用
demo.launch(inbrowser=True, server_name="0.0.0.0", server_port=5001)
