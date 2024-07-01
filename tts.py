import io
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from scipy.io.wavfile import write
import torch

config = XttsConfig()
config.load_json("./XTTS-v2/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="XTTS-v2", eval=True)
if torch.cuda.is_available():
    model.cuda()
    print("模型已移至GPU。")
else:
    print("GPU 不可用，模型將在CPU上運行。")

def text_to_wav(text,language="en",samples="./XTTS-v2/samples/en_sample.wav"):
    outputs = model.synthesize(
        text,
        config,
        speaker_wav=samples,
        gpt_cond_len=3,
        language=language,
    )
    # 设置输出文件的采样率，通常为22050 Hz
    sample_rate = 22050
    return get_wav_binary(sample_rate, outputs['wav'])

def get_wav_binary(sample_rate, audio_data):
    # 创建一个内存文件
    mem_file = io.BytesIO()
    # 将音频数据写入内存文件
    write(mem_file, sample_rate, audio_data)
    # 将文件指针移动到开始位置
    mem_file.seek(0)
    # 返回二进制数据
    return mem_file