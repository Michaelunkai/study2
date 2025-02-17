from bottle import Bottle, run, response
import sys

app = Bottle()

@app.route('/')
def index():
    response.content_type = 'text/html'
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech to Text</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .App {
            text-align: center;
            background-color: black;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            padding: 20px;
            color: white;
        }
        button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            transition-duration: 0.4s;
        }
        button:hover {
            background-color: #45a049;
        }
        button:disabled {
            background-color: #cccccc;
            color: #666666;
            cursor: not-allowed;
        }
        #stopRecording {
            background-color: #f44336;
        }
        #stopRecording:hover {
            background-color: #d32f2f;
        }
        #copyText {
            background-color: #008CBA;
        }
        #copyText:hover {
            background-color: #007B9A;
        }
        canvas {
            border: 1px solid white;
            margin: 20px 0;
        }
        .text-area {
            width: 80%;
            min-height: 200px;
            border: 1px solid white;
            padding: 10px;
            margin-top: 20px;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .interim {
            color: gray;
        }
        .success-message {
            color: #4CAF50;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="App">
        <button id="startRecording">Start Recording</button>
        <button id="stopRecording" disabled>Stop Recording</button>
        <button id="copyText">Copy Text</button>
        <canvas id="waveform" width="800" height="200"></canvas>
        <p id="language"></p>
        <div id="textArea" class="text-area"></div>
    </div>
    <script>
        let isRecording = false;
        const startButton = document.getElementById('startRecording');
        const stopButton = document.getElementById('stopRecording');
        const copyButton = document.getElementById('copyText');
        const textArea = document.getElementById('textArea');
        const languageDisplay = document.getElementById('language');
        const canvas = document.getElementById('waveform');
        const canvasCtx = canvas.getContext('2d');

        let recognition;
        let audioContext;
        let analyser;
        let dataArray;

        if ('webkitSpeechRecognition' in window) {
            recognition = new webkitSpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.lang = 'en-US';

            let finalTranscript = '';
            let interimTranscript = '';

            recognition.onresult = (event) => {
                interimTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    const transcript = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += transcript + ' ';
                    } else {
                        interimTranscript += transcript;
                    }
                }

                const finalWords = finalTranscript.trim().split(' ');
                const interimWords = interimTranscript.trim().split(' ');
                while (interimWords.length > 0 && finalWords[finalWords.length - 1] === interimWords[0]) {
                    interimWords.shift();
                }
                interimTranscript = interimWords.join(' ');

                textArea.innerHTML = finalTranscript + '<span class="interim">' + interimTranscript + '</span>';
            };

            recognition.onend = () => {
                if (isRecording) {
                    recognition.start();
                }
            };

            recognition.onerror = (event) => {
                console.error('Speech recognition error', event.error);
                if (event.error === 'no-speech') {
                    console.log('No speech was detected. Restarting...');
                    recognition.stop();
                    recognition.start();
                }
            };

            recognition.onlanguagechange = (event) => {
                languageDisplay.textContent = 'Detected Language: ' + (event.language === 'en-US' ? 'English' : 'Hebrew');
            };
        }

        startButton.addEventListener('click', () => {
            if (!recognition) {
                alert('Speech recognition is not supported in your browser.');
                return;
            }

            if (!isRecording) {
                textArea.innerHTML = '';
                finalTranscript = '';
            }

            recognition.start();
            startRecording();
            isRecording = true;
            startButton.disabled = true;
            stopButton.disabled = false;
        });

        stopButton.addEventListener('click', () => {
            recognition.stop();
            stopRecording();
            isRecording = false;
            startButton.disabled = false;
            stopButton.disabled = true;
        });

        copyButton.addEventListener('click', () => {
            const textToCopy = textArea.innerText;
            navigator.clipboard.writeText(textToCopy).then(() => {
                const successMessage = document.createElement('div');
                successMessage.textContent = 'Text copied successfully!';
                successMessage.className = 'success-message';
                textArea.parentNode.insertBefore(successMessage, textArea.nextSibling);

                setTimeout(() => {
                    successMessage.remove();
                }, 3000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });

        function startRecording() {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 2048;
            dataArray = new Uint8Array(analyser.frequencyBinCount);

            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    const source = audioContext.createMediaStreamSource(stream);
                    source.connect(analyser);
                    drawWaveform();
                });
        }

        function stopRecording() {
            if (audioContext) {
                audioContext.close();
            }
        }

        function drawWaveform() {
            if (!isRecording) return;

            requestAnimationFrame(drawWaveform);

            analyser.getByteTimeDomainData(dataArray);

            canvasCtx.fillStyle = 'rgb(0, 0, 0)';
            canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

            canvasCtx.lineWidth = 2;
            canvasCtx.strokeStyle = 'rgb(255, 255, 255)';

            canvasCtx.beginPath();

            const sliceWidth = canvas.width * 1.0 / dataArray.length;
            let x = 0;

            for (let i = 0; i < dataArray.length; i++) {
                const v = dataArray[i] / 128.0;
                const y = v * canvas.height / 2;

                if (i === 0) {
                    canvasCtx.moveTo(x, y);
                } else {
                    canvasCtx.lineTo(x, y);
                }

                x += sliceWidth;
            }

            canvasCtx.lineTo(canvas.width, canvas.height / 2);
            canvasCtx.stroke();
        }

        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(function(stream) {
                console.log('Microphone access granted');
            })
            .catch(function(err) {
                console.log('Error accessing microphone', err);
            });
    </script>
</body>
</html>
'''

if __name__ == "__main__":
    try:
        run(app, host="localhost", port=8080, debug=True)
    except Exception as e:
        print(f"An error occurred while starting the server: {e}", file=sys.stderr)
        sys.exit(1)
