from typing import Any
import argparse
from distutils.util import strtobool
import os
import time
from traceback import print_exc

import numpy as np
import pyaudio
import requests
from requests.exceptions import RequestException
import openwakeword as oww
from openwakeword.model import Model

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
COOLDOWN_SECS = 1.0
DEFAULT_CHUNK_LENGTH = 80
DEFAULT_MODEL = "hey_jarvis_v0.1"
DEFAULT_THRESHOLD = 0.5
DEFAULT_VAD_THRESHOLD = 0.5


def handle_detection(base_url: str):
    try:
        url = f"{base_url}/api/listen-for-command"
        resp = requests.post(url, timeout=30)
        if resp.status_code > 300:
            print(f"{resp.status_code} response from {url}")
    except RequestException:
        print_exc()


def main(model: Model, mic_stream: Any, threshold: float, rhasspy_url: str, chunk_samples: int):
    detected = False
    last_detection = 0
    while True:
        # Get audio
        audio = np.frombuffer(mic_stream.read(chunk_samples), dtype=np.int16)
        # Feed to openWakeWord model
        model.predict(audio)

        for mdl in model.prediction_buffer.keys():
            # Add scores in formatted table
            scores = list(model.prediction_buffer[mdl])
            if scores[-1] > threshold:
                if not detected and (time.time() - last_detection) > COOLDOWN_SECS:
                    detected = True
                    last_detection = time.time()
                    handle_detection(rhasspy_url)
            else:
                detected = False


def parse_argments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--list', '-l', action='store_true', help="List available models")
    parser.add_argument('--model', '-m', default=os.environ.get("MODEL", DEFAULT_MODEL), help="Wakeword model to use")
    parser.add_argument(
        '--chunk-length', '-c',
        default=os.environ.get("CHUNK_LENGTH", DEFAULT_CHUNK_LENGTH),
        type=int,
        help="Length of audio chunks in ms to pass to the model"
    )
    parser.add_argument(
        '--threshold', '-t',
        default=os.environ.get("THRESHOLD", DEFAULT_THRESHOLD),
        type=float,
        help="Detection threshold to use"
    )
    parser.add_argument(
        '--vad-threshold', '-v',
        default=os.environ.get("VAD_THRESHOLD", DEFAULT_VAD_THRESHOLD),
        type=float,
        help="vad_threshold between 0 and 1"
    )
    parser.add_argument(
        '--noise-suppression', '-n',
        action='store_true',
        default=strtobool(os.environ.get("NOISE_SUPPRESSION", 'f'))
    )
    parser.add_argument(
        '--rhasspy-url', '-r',
        default=os.environ.get("RHASSPY_URL", "http://localhost:12101"),
        help="Host of rhasspy"
    )
    return parser.parse_args()


def init(model_path: str, chunk_samples: int, vad_threshold: float, noise_suppression: bool) -> tuple[Model, Any]:
    # Get microphone stream
    audio = pyaudio.PyAudio()
    mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=chunk_samples)
    return (
        Model(wakeword_model_paths=[model_path], vad_threshold=vad_threshold, enable_speex_noise_suppression=noise_suppression), mic_stream
    )


if __name__ == "__main__":
    args = parse_argments()
    model_paths = oww.get_pretrained_model_paths()
    if args.list:
        for path in model_paths:
            print(os.path.splitext(os.path.split(path)[-1])[0])
    else:
        selected_model = None

        # Round to nearest 80ms
        cl = args.chunk_length - args.chunk_length % DEFAULT_CHUNK_LENGTH
        if cl < DEFAULT_CHUNK_LENGTH:
            cl = DEFAULT_CHUNK_LENGTH

        for path in model_paths:
            if path.find(args.model) != -1:
                selected_model = path
        if selected_model is None:
            print(f"No such model: {args.model}")
        else:
            main(
                *init(selected_model, chunk_samples=cl * RATE // 1000, vad_threshold=args.vad_threshold, noise_suppression=args.noise_suppression),
                threshold=args.threshold,
                rhasspy_url=args.rhasspy_url.rstrip("/"),
                chunk_samples=cl * RATE // 1000
            )
