# # uvicorn ttsApiTest:app --reload --port 8090
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import whisper
from fastapi import Request
import io
# from pydantic import BaseModel

import numpy as np
import wave

app = FastAPI()

# Load Whisper model
# model = whisper.load_model("tiny")

## v1
# @app.post("/generate-text/")
# async def transcribe(audio_data: AudioData):
#     try:
#         # Decode the Base64 audio data to binary
#         audio_binary = base64.b64decode(audio_data.audio)

#         # Convert binary data to np.ndarray
#         audio_array = np.frombuffer(audio_binary, dtype=np.float32)

#         # Use Whisper model to transcribe the np.ndarray audio
#         result = model.transcribe(audio_array)

#         print("====================================")
#         print(result)
#         print("====================================")
        
#         # Return transcription text
#         return JSONResponse(content={"transcription": result["text"]})
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        
# @app.post("/generate-text/")
# async def transcribe(file: UploadFile = File(...)):
#     # Read uploaded file content
#     audio_data = await file.read()
    
#     # Save audio data to a temporary file
#     with open("temp.wav", "wb") as temp_file:
#         temp_file.write(audio_data)
    
#     # Transcribe audio using Whisper model
#     result = model.transcribe("temp.wav")
    
#     # Return transcription text
#     return JSONResponse(content={"transcription": result["text"]})

# @app.post("/generate-text/")
# async def generate_text(request: Request):
#     # 从请求体中读取二进制数据
#     audio_data = await request.body()
#     print(audio_data) # bytes data

#     # 将二进制数据转换为 NumPy 数组
#     audio_np = convert_audio_bytes_to_numpy(audio_data)
#     print(audio_np)
    
#     # 使用 Whisper 模型进行转录
#     result = model.transcribe(audio_np)
    
#     # print(result)

#     # 返回转录文本
#     return JSONResponse(content={"text": result["text"]})

# # # def convert_audio_bytes_to_numpy(audio_bytes: bytes) -> np.ndarray:
# # #     """将音频字节数据转换为 NumPy 数组"""
# # #     with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
# # #         n_channels = wf.getnchannels()
# # #         sampwidth = wf.getsampwidth()
# # #         framerate = wf.getframerate()
# # #         n_samples = wf.getnframes()
        
# # #         # 读取音频数据并转换为 NumPy 数组
# # #         frames = wf.readframes(n_samples)
# # #         audio_np = np.frombuffer(frames, dtype=np.int16)  # 假设音频为 16 位深度
        
# # #         # 如果是立体声，转换为单声道
# # #         if n_channels > 1:
# # #             audio_np = audio_np[::n_channels]
        
# # #         # 标准化数据
# # #         audio_np = audio_np.astype(np.float32) / (2**15)
        
# # #     return audio_np

# # # # 定义一个 Pydantic 模型来解析请求体
# # # class AudioData(BaseModel):
# # #     sample_rate: int
# # #     audio_data: np.ndarray  # 或者使用 list 或其他可序列化类型

# # @app.post("/generate-text/")
# # # async def generate_text(audio_data: AudioDat):
# # async def generate_text(audio_data):
# #     try:
# #         # 获取采样率和音频数据
# #         sample_rate = audio_data.sample_rate
# #         audio_np = audio_data.audio_data
        
# #         print("sample_rate:")
# #         print(sample_rate)
        
# #         # 使用 Whisper 模型进行转录
# #         result = model.transcribe(audio_np)
        
# #         # 返回转录文本
# #         return {"text": result["text"]}
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # # Run FastAPI app
# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="0.0.0.0", port=8090)


# from fastapi import FastAPI, HTTPException, Request, File, UploadFile
# import numpy as np
# import whisper
# import librosa

# app = FastAPI()

# model = whisper.load_model("tiny")

# @app.post("/generate-text/")
# # async def generate_text(request: Request):
# async def generate_text(file):
#     try:
# #         data = await request.json()
        
# #         sample_rate = data['sample_rate']
# #         audio_data = data['audio_data']
# #         audio_np = np.array(audio_data, dtype=np.float32)  # 确保音频数据为浮点数类型
        
# #         print("audio_np:")
# #         print(audio_np)
# #         print("sample_rate:")
# #         print(sample_rate)
        
# #         # 如果采样率不是 16000 Hz，重新采样音频数据
# #         if sample_rate != 16000:
# #             audio_np = librosa.resample(audio_np, orig_sr=sample_rate, target_sr=16000)
# #             sample_rate = 16000
        
#         # # 使用 Whisper 模型进行转录
#         # result = model.transcribe(audio_np)
        
#         result = model.transcribe(file)
        
#         # 返回转录文本
#         return {"text": result["text"]}
#     except Exception as e:
#         import traceback
#         print("Error during transcription:", traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))

# # Run FastAPI app
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8090)



from fastapi import FastAPI, UploadFile, File
from fastapi import Request
import whisper
import soundfile as sf
import numpy as np
import io
import tempfile

# 加载 Whisper 模型
model = whisper.load_model("turbo")

def process_audio(audio_file):
    # 使用 Whisper 模型进行转录
    result = model.transcribe(audio_file)
    
    # 获取转录文本
    transcription = result["text"]
    return transcription

@app.post("/generate-text/")
async def transcribe_audio(filename: Request):
    
    # 从请求体中解析 JSON 数据
    item = await filename.json()
    
    audio_filename = item.get("audio_filename")
    print(audio_filename)
    
    # 转录音频
    transcription = process_audio(audio_filename)

    return {"transcription": transcription}


