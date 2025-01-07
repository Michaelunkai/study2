import GPUtil
import time

def get_gpu_temperature():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            temperature = gpus[0].temperature
            return f'GPU Temperature: {temperature}°C'
        else:
            return 'No GPU found.'
    except Exception as e:
        return f'Unable to fetch GPU temperature: {e}'

def main():
    try:
        while True:
            gpu_temp = get_gpu_temperature()
            print(gpu_temp)
            print('-' * 30)

            time.sleep(1)  # Update every 1 second

    except KeyboardInterrupt:
        print('Exiting...')

if __name__ == "__main__":
    main()
