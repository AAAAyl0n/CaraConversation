from openai import OpenAI
import pygame
import time
client = OpenAI()

  
def chat_with_ai():
    pygame.mixer.init()
    messages = [
        {"role": "system", "content": "You are my best firent. Try to chat with me instead of sending me back large blocks of text. Please speak more everyday.Don't reply to too many words at once."}
    ]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Ending the chat. Goodbye!")
            break

        messages.append({"role": "user", "content": user_input})

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
    
