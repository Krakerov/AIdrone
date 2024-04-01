import pygame
import numpy as np

# Инициализация pygame
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Параметры квадратного импульса
frequency = 440  # Частота в Гц
sample_rate = 22050  # Частота дискретизации
pulslen = 0.3
Sumlen = 22.5
koef = sample_rate/1000
#ChanelsVelu = [0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4]
ChanelsVelu = [1, 1, 1, 1, 1, 1, 1, 1]
# Список продолжительностей импульсов
def PrintSaund(Chanels):
    
    durations = [x+1 for x in Chanels] # Продолжительности в mcсекундах


    SumDuration = np.sum(durations) + pulslen



    WaweList = []

    WaweList.extend(np.zeros(int((Sumlen - SumDuration)*koef)))
    WaweList.extend(np.ones(int(pulslen*koef)))

    # Генерация и воспроизведение серии квадратных импульсов
    for duration in durations:
        WaweList.extend(np.zeros(int((duration - pulslen)*koef)))
        WaweList.extend(np.ones(int(pulslen*koef)))



        #t = np.linspace(0, duration, sample_rate, False)
        #square_wave = 0.5 * (np.sign(np.sin(2 * np.pi * frequency * t)) + 1)
        #for i in square_wave:
            #print(i)
    #WaweListFix =  np.zeros(sample_rate - len(WaweList))
    #WaweListFix = np.concatenate ((WaweListFix, WaweList))
    WaweList.extend(np.zeros(sample_rate - len(WaweList)))
    sound = pygame.sndarray.make_sound(np.repeat(np.int16(WaweList * 32767).reshape(22050, 1), 2, axis = 1))
    sound.play()
    pygame.time.wait(int(50))
    
while True: # ЗАПУСКАТЬ ТОЛЬКО В РЕЖИМЕ ОТЛАДКИ
    PrintSaund(ChanelsVelu)