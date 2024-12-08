# # uvicorn ttsApiTest:app --reload --port 8080
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, VitsModel
import torch

app = FastAPI()

# Load the pre-trained model and tokenizer
model = VitsModel.from_pretrained("mms-tts-eng")
tokenizer = AutoTokenizer.from_pretrained("mms-tts-eng")

class TextInput(BaseModel):
    text: str

@app.post("/generate-audio/")
def generate_audio(text_input: TextInput):
    try:
        print("=====================")
        print("tts text:")
        print(text_input)
        print("=====================")
        
        inputs = tokenizer(text_input.text, return_tensors="pt")
        
        with torch.no_grad():
            output = model(**inputs)
        waveform = output.waveform.squeeze().tolist()  # Convert tensor to list for JSON serialization
        return {"waveform": waveform}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
