import vosk
import json
import pyaudio

model = vosk.Model("model")  # Load pre-trained speech model
rec = vosk.KaldiRecognizer(model, 16000)  # Initialize recognizer

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

while True:
    data = stream.read(4096)
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        print("Command Received:", result["text"])
