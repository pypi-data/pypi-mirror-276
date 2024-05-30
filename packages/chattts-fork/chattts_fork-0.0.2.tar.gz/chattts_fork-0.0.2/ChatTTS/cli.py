import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

from .core import Chat
import argparse
import numpy as np
import wave


def main():
    # cli args
    ap = argparse.ArgumentParser(description="Your text to tts")
    ap.add_argument("text", type=str, help="Your text")
    ap.add_argument(
        "-o", "--out-file", help="out file name", default="tts.wav", dest="out_file"
    )
    ap.add_argument("--use-seed", help="use seed", action="store_true", dest="use_seed")
    ap.add_argument(
        "-s", "--seed", help="out file name", default=None, dest="seed"
    )

    args = ap.parse_args()
    out_file = args.out_file
    text = args.text
    if not text:
        raise ValueError("text is empty")

    chat = Chat()
    try:
        chat.load_models()
    except Exception as e:
        # this is a tricky for most newbies do not now the args for cli
        print("The model maybe broke will load again")
        chat.load_models(force_redownload=True)
    texts = [
        text,
    ]

    wavs = chat.infer(texts, use_decoder=True)
    audio_data = np.array(wavs[0], dtype=np.float32)
    sample_rate = 24000
    audio_data = (audio_data * 32767).astype(np.int16)

    with wave.open(out_file, "w") as wf:
        wf.setnchannels(1)  # Mono channel
        wf.setsampwidth(2)  # 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())
    print(f"Generate Done for file {out_file}")
