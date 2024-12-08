# # uvicorn ttsApiTest:app --reload --port 8070
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import transformers
import torch
from typing import List

# 初始化FastAPI应用
app = FastAPI()

# 本地模型路径
model_id = "/root/autodl-tmp/Meta-Llama-3.1-8B-Instruct/"

# 加载模型和tokenizer
model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,  # 使用 float16 以减少内存消耗
    low_cpu_mem_usage=True,
    device_map="auto"  # 自动分配设备以优化内存使用
)

tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)

# 启用分块处理以减少 GPU 内存占用
model.gradient_checkpointing_enable()

# 定义请求体的数据模型
class Message(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: List[Message]  # 使用 typing.List 来替代

# 定义生成文本的路径
@app.post("/generate/")
def generate_text(messages: Messages):
    try:
        print("messages:")
        print(messages)
        # 提取系统提示和用户消息
        system_prompt = next((msg.content for msg in messages.messages if msg.role == "system"), None)
        user_message = next((msg.content for msg in messages.messages if msg.role == "user"), None)
        
        print("system_prompt:")
        print(system_prompt)
        print("user_message:")
        print(user_message)
        
        if user_message is None:
            raise HTTPException(status_code=400, detail="No user message found")
        if system_prompt is not None:
            # 将系统提示和用户消息合并为模型输入
            prompt = f"{system_prompt}\n{user_message}"
        prompt = user_message
        
        inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

        print("推理生成文本")
        # 推理生成文本
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=256,
                do_sample=True,
                top_p=0.95,
                top_k=60
            )

        print("解码生成的文本")
        # 解码生成的文本
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(generated_text)
        return {"generated_text": generated_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 运行服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8070)
