import pyaudio
import array
import subprocess
import time
import os

# --- НАСТРОЙКИ ---
TAP_X = 500
TAP_Y = 1000
THRESHOLD = 15000 
CHUNK = 512
RATE = 48000
RISH_PATH = "/data/data/com.termux/files/home/rish_home/rish"
# -----------------

def main():
    proc = subprocess.Popen(
        [RISH_PATH], 
        stdin=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        bufsize=0 
    )

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("⚡ ГИПЕР-РЕЖИМ АКТИВИРОВАН ⚡")
    print("Задержка должна быть минимальной. Слушаю...")

    try:
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            data_chunk = array.array('h', data)
            volume = max(data_chunk)

            if volume > THRESHOLD:
                proc.stdin.write(f"input tap {TAP_X} {TAP_Y}\n")
                
                print(f"[*] Хлопок! ({volume}) -> Клик!")
                
 
                time.sleep(0.2)
            
                stream.read(stream.get_read_available(), exception_on_overflow=False)

    except KeyboardInterrupt:
        print("\nВыключение...")
    finally:
        proc.stdin.write("exit\n")
        proc.terminate()
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()
