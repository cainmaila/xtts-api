from fastapi import FastAPI, HTTPException
from fastapi.responses import  StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from tts import text_to_wav
from pydantic import BaseModel

app = FastAPI()

# 添加CORS中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有標頭
)


@app.get("/")
def read_root():
    return 'TTS Service is running.'

class TTSRequest(BaseModel):
    text: str
    language: str = "en"
    samples: str = "./XTTS-v2/samples/en_sample.wav"

@app.post("/tts/")
def generate_tts(request_body: TTSRequest):
    text = request_body.text
    language = request_body.language
    samples = request_body.samples
    try:
        wav_binary = text_to_wav(text,language,samples)
        return StreamingResponse(wav_binary, media_type="audio/wav")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))