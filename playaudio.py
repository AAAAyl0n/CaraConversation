import pygame
def play_audio(file_path):
    # 初始化 pygame mixer
    pygame.mixer.init()
    
    # 加载音频文件
    pygame.mixer.music.load(file_path)
    
    # 播放音频文件
    pygame.mixer.music.play()
    
    # 等待音频播放完成
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

play_audio("output.mp3")