import sounddevice as sd
import numpy as np
import time
import pyautogui
from scipy.signal import butter, filtfilt

# Parameters for clap detection
FS = 44100           # Sample rate
BLOCK_SIZE = 1024    # Block size for audio input stream
THRESHOLD = 0.7      # Amplitude threshold (increased for more specificity)
CLAP_INTERVAL = 0.5  # Maximum time between two claps
MIN_CLAP_DURATION = 0.02  # Minimum duration of a clap in seconds
MAX_CLAP_DURATION = 0.15  # Maximum duration of a clap in seconds

# Frequency bands specifically for hand claps
CLAP_FREQ_BANDS = [
    (2000, 2500),  # Primary hand clap frequency range
    (3000, 4000)   # Secondary hand clap frequency range
]

# State variables
last_clap_time = 0
clap_count = 0
last_audio_buffer = np.zeros(int(FS * MAX_CLAP_DURATION))

# Track which desktop we're currently on
current_desktop = 1  # Assume we start on Desktop 1

def butter_bandpass(lowcut, highcut, fs, order=4):
    """Create a bandpass filter."""
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def analyze_frequency_content(audio_data, fs):
    """Analyze if the frequency content matches hand clap characteristics."""
    # Apply bandpass filters for each frequency band
    total_energy = 0
    for low_freq, high_freq in CLAP_FREQ_BANDS:
        b, a = butter_bandpass(low_freq, high_freq, fs)
        filtered = filtfilt(b, a, audio_data)
        total_energy += np.sum(filtered ** 2)

    return total_energy > THRESHOLD

def analyze_envelope(audio_data):
    """Analyze the envelope shape characteristic of hand claps."""
    envelope = np.abs(audio_data)
    # Check for sharp attack and quick decay characteristic of hand claps
    max_idx = np.argmax(envelope)
    if max_idx == 0 or max_idx == len(envelope) - 1:
        return False

    attack_time = max_idx / FS
    decay_ratio = envelope[max_idx:].mean() / envelope[max_idx]

    return (MIN_CLAP_DURATION <= attack_time <= MAX_CLAP_DURATION and
            decay_ratio < 0.5)  # Quick decay characteristic

def is_hand_clap(audio_data):
    """Determine if the audio data corresponds specifically to a hand clap."""
    # Check both frequency content and envelope shape
    return (analyze_frequency_content(audio_data, FS) and
            analyze_envelope(audio_data))

def switch_desktop():
    """
    Toggle between Desktop 1 and Desktop 2:
      - If on Desktop 1, switch to Desktop 2
      - If on Desktop 2, switch to Desktop 1
    """
    global current_desktop

    if current_desktop == 1:
        # Switch to Desktop 2
        pyautogui.hotkey('win', 'ctrl', 'right')
        current_desktop = 2
        print("Switched to Desktop 2.")
    else:
        # Switch to Desktop 1
        pyautogui.hotkey('win', 'ctrl', 'left')
        current_desktop = 1
        print("Switched to Desktop 1.")

def audio_callback(indata, frames, time_info, status):
    """Process audio input to detect double hand claps."""
    global last_clap_time, clap_count, last_audio_buffer

    if status:
        print(f"Stream status: {status}")

    # Update audio buffer
    audio_data = indata.flatten()
    last_audio_buffer = np.roll(last_audio_buffer, -len(audio_data))
    last_audio_buffer[-len(audio_data):] = audio_data

    if is_hand_clap(last_audio_buffer):
        current_time = time.time()
        time_diff = current_time - last_clap_time

        # Only consider a new clap if it's at least 0.1 seconds
        if 0.1 <= time_diff <= CLAP_INTERVAL:
            clap_count += 1
            if clap_count == 2:
                print("Double hand clap detected!")
                switch_desktop()
                clap_count = 0
        else:
            clap_count = 1

        last_clap_time = current_time

def main():
    """Main function to run the clap detection."""
    print("Listening for double hand claps...")
    try:
        with sd.InputStream(callback=audio_callback,
                            channels=1,
                            samplerate=FS,
                            blocksize=BLOCK_SIZE):
            while True:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping clap detection...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
