from openai import OpenAI
import pygame
import time
import pyaudio
import wave
import numpy as np
client = OpenAI()

def get_volume(data):
    audio_data = np.frombuffer(data, dtype=np.int16)
    return np.abs(audio_data).mean()

def record_audio(filename, sample_rate=44100, channels=1, chunk_size=2048, threshold=500, silence_duration=2):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=sample_rate,
                        input=True,
                        frames_per_buffer=chunk_size)

    print("输入'r'开始对话")
    command = input()
    if command.lower() != 'r':
        print("未输入'r'，录音取消。")
        return

    print("listening...")

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

    print("thinking")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
  
def chat_with_ai():
    pygame.mixer.init()
    messages = [
        {"role": "system", "content": "You are my best firend. Your name is Cara. Try to chat with me instead of sending me back large blocks of text. Please speak more everyday.Don't reply to too many words at once."}
    ]
    
    while True:
        record_audio("input.wav")

        audio_file= open("input.wav", "rb")
        transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
        )#transcription.text is the text of the audio

        #user_input = input("You: ")
        #if user_input.lower() in ["exit", "quit"]:
        #    print("Ending the chat. Goodbye!")
        #    break

        #messages.append({"role": "user", "content": user_input})
        messages.append({"role": "user", "content": transcription.text})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        ai_message = response.choices[0].message.content
        print(f"AI: {ai_message}")

        messages.append({"role": "assistant", "content": ai_message})

        response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=ai_message,
        )

        response.stream_to_file("output.mp3")
        time.sleep(0.1);
        # 加载音频文件
        pygame.mixer.music.load("output.mp3")
        
        # 播放音频文件
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)



if __name__ == "__main__":
    chat_with_ai()
    
