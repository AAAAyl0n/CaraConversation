import pyaudio
import wave
import numpy as np

def get_volume(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean()

def record_audio(filename, sample_rate=44100, channels=1, chunk_size=2048, threshold=500, silence_duration=0.5):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("输入'r'以开始录音...")
    command = input()
    if command.lower() != 'r':
        print("未输入'r'，录音取消。")
        return

    print("录音开始...")

    frames = []
    silence_count = 0
    recording = True

    while recording:
        try:
            data = stream.read(chunk_size, exception_on_overflow=False)
            frames.append(data)

            volume = get_volume(data)
            if volume < threshold:
                silence_count += 1
            else:
                silence_count = 0

            if silence_count >= int(silence_duration * sample_rate / chunk_size):
                recording = False
        except IOError as e:
            print(f"错误: {e}")
            continue

    print("录音结束...")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

record_audio("input.wav")
