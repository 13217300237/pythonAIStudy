import gradio as gr

def process_file(file_obj):
    # 获取文件名
    file_name = file_obj.name
    # 处理文件，这里只是简单地返回文件名
    return f"您上传的文件名为: {file_name}"

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    file_upload = gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])

    # 创建一个文本框用于显示结果
    output_text = gr.Textbox(label="输出")

    # 将文件上传事件与处理函数绑定
    file_upload.change(fn=process_file, inputs=file_upload, outputs=output_text)

# 启动应用
demo.launch()