from pydub import AudioSegment
import pygame.mixer
import simpleaudio as sa
import time

#audio = AudioSegment.from_file("SMNS.mp3")
#raw_audio_data = audio.raw_data

#wave_obj = sa.WaveObject(raw_audio_data,num_channels=audio.channels, bytes_per_sample=audio.sample_width,sample_rate=audio.frame_rate)
#play_obj = wave_obj.play()

pygame.mixer.init()

def start_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def stop_audio():
    pygame.mixer.music.stop()


start_audio("SMNS.mp3")
for i in range(5):
    time.sleep(2)
stop_audio()
time.sleep(5)
start_audio("New.mp3")
for i in range(10):
    time.sleep(2)

#play_obj.wait_done()
