import gradio as gr
import os
import shutil
from pathlib import Path

# 指定保存文件的目录，使用相对路径
SAVE_DIR = "./uploaded_files"

# 确保保存目录存在
Path(SAVE_DIR).mkdir(parents=True, exist_ok=True)


def process_file(file_obj):
    if file_obj is None:
        return "未上传文件，请选择一个文件上传。"

    # 获取文件的保存路径
    file_path = file_obj.name  # 使用 .name 获取文件的保存路径

    # 获取原始文件名和扩展名
    original_file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(original_file_name)[1].lower()

    # 允许的文件扩展名列表
    allowed_extensions = ['.pdf', '.txt', '.doc']

    if file_extension in allowed_extensions:
        # 构建新的保存路径
        save_path = os.path.join(SAVE_DIR, original_file_name)

        # 移动文件到指定目录
        shutil.move(file_path, save_path)  # 使用 shutil.move 支持跨磁盘分区移动

        # 返回成功信息
        return f"文件已成功上传并保存到: {save_path}"
    else:
        return "不允许的文件类型，请上传 PDF、TXT 或 DOC 文件。"


# 创建Gradio Blocks应用
with gr.Blocks() as demo:
    file_upload = gr.File(label="上传文件", file_types=['pdf', 'txt', 'doc'])
    output_text = gr.Textbox(label="输出")

    file_upload.change(fn=process_file, inputs=[file_upload], outputs=output_text)

demo.launch()