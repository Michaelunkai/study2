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

    recognition.onresult = (event) => {
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        textArea.innerHTML = finalTranscript + '<span class="interim">' + interimTranscript + '</span>';
    };

    recognition.onend = () => {
        if (isRecording) {
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
        // Only clear the text area if we're starting a new session after stopping
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

// Initialize microphone access on page load to improve responsiveness
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        console.log('Microphone access granted');
    })
    .catch(function(err) {
        console.log('Error accessing microphone', err);
    });