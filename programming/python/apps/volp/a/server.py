import socket
import pyaudio
import wave  # Import the wave module for writing WAV files

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(1)
    print("Server listening on port 8000...")

    conn, addr = server_socket.accept()
    print("Connected to:", addr)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

    print("Streaming audio...")

    # Create a wave file for writing
    audio_file = wave.open("received_audio.wav", "wb")
    audio_file.setnchannels(CHANNELS)
    audio_file.setsampwidth(p.get_sample_size(FORMAT))
    audio_file.setframerate(RATE)

    try:
        while True:
            data = conn.recv(CHUNK)
            if not data:
                break
            stream.write(data)
            audio_file.writeframes(data)  # Write audio frames to the wave file
    except KeyboardInterrupt:
        pass

    print("Closing connection and saving audio...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()

    audio_file.close()  # Close the wave file after writing

if __name__ == "__main__":
    server()
