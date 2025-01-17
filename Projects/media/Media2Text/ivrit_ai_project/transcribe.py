from time import time
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32,garbage_collection_threshold:0.8"
import torch
from faster_whisper import WhisperModel
import gradio as gr

device = "cuda" if torch.cuda.is_available() else "cpu"
compute_type = "float16" if torch.cuda.is_available() else "int8"

model = WhisperModel("ivrit-ai/faster-whisper-v2-d3-e3", device=device, compute_type=compute_type, cpu_threads=os.cpu_count())

def transcribe(audio):
    segments, _ = model.transcribe(audio, language="he", max_new_tokens=128)
    return "\n".join([segment.text for segment in segments])

demo = gr.Interface(transcribe, gr.File(file_types=["audio"]), "text")
demo.launch(share=False)
