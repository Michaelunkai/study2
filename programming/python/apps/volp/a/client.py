import socket
import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def get_input_device_index(p):
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            return i
    return None

def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8000))

    p = pyaudio.PyAudio()

    # Find input device index
    input_device_index = get_input_device_index(p)
    if input_device_index is None:
        print("No input devices found.")
        return

    # List available output devices
    print("Available output devices:")
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxOutputChannels"] > 0:
            print(f"Output Device {i}: {info['name']}")

    # Choose the first available output device
    output_device_index = None
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if info["maxOutputChannels"] > 0:
            output_device_index = i
            break

    if output_device_index is None:
        print("No output devices found.")
        return

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    input_device_index=input_device_index,
                    output_device_index=output_device_index,
                    frames_per_buffer=CHUNK)

    print("Streaming audio...")

    while True:
        try:
            data = stream.read(CHUNK)
            client_socket.sendall(data)
        except KeyboardInterrupt:
            break

    print("Closing connection...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    client_socket.close()

if __name__ == "__main__":
    client()
