# 使用官方的 Python 基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝必要的系統依賴和 Rust 編譯器
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y build-essential libssl-dev libffi-dev python3-dev curl gcc cmake \
    && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y \
    && . $HOME/.cargo/env \
    && python -m pip install --upgrade pip \
    && pip install sudachipy --no-binary :all: \
    && apt-get install libsndfile1 -y \
    && apt-get install git-all -y
RUN pip install TTS
RUN git lfs install
RUN git clone https://huggingface.co/coqui/XTTS-v2

# 安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製當前目錄的內容到容器的工作目錄中
COPY . /app

# samples掛載外部資料夾
VOLUME /app/samples

# 暴露端口
EXPOSE 8000

# 運行 FastAPI 應用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]