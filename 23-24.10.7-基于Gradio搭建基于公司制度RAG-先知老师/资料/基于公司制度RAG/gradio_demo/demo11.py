import gradio as gr
import os

# 允许的文件扩展名列表
allowed_extensions = ['.pdf', '.txt', '.doc']

def process_file(file_obj):
    # 获取文件名和扩展名
    file_name = file_obj.name
    file_extension = os.path.splitext(file_name)[1].lower() # pdf
    print("文件上传的后缀名", file_extension)

    if file_extension in allowed_extensions:
        # 处理文件，这里只是简单地返回文件名
        return f"您上传的文件名为: {file_name}"
    else:
        # 如果文件扩展名不在允许的列表中，返回错误信息
        return "不允许的文件类型，请上传 PDF、TXT 或 DOC 文件。"

# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    # 创建一个文件上传控件
    file_upload = gr.File(label="上传文件------pdf', 'txt', 'doc'", file_types=allowed_extensions)

    # 创建一个文本框用于显示结果
    output_text = gr.Textbox(label="输出")

    # 将文件上传事件与处理函数绑定
    file_upload.change(fn=process_file, inputs=file_upload, outputs=output_text)
# 启动应用
demo.launch()