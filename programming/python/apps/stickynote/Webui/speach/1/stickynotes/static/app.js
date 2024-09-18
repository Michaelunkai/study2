let isRecording = false;
const noteTextarea = document.getElementById("note");
const saveButton = document.getElementById("saveNote");
const clearButton = document.getElementById("clearNote");
const startSpeechButton = document.getElementById("startSpeech");
const stopSpeechButton = document.getElementById("stopSpeech");
const copyButton = document.getElementById("copyNote");
const languageDisplay = document.getElementById("language");
const canvas = document.getElementById("waveform");
const canvasCtx = canvas.getContext("2d");

let recognition;
let audioContext;
let analyser;
let dataArray;

if ("webkitSpeechRecognition" in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
        let finalTranscript = "";

        for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript;
            }
        }

        noteTextarea.value += finalTranscript;
    };

    recognition.onend = () => {
        if (isRecording) {
            recognition.start();
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        if (event.error === "no-speech") {
            console.log("No speech was detected. Restarting...");
            recognition.stop();
            recognition.start();
        }
    };

    recognition.onlanguagechange = (event) => {
        languageDisplay.textContent = "Detected Language: " + (event.language === "en-US" ? "English" : "Other");
    };
}

function saveNote() {
    const content = noteTextarea.value;
    fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: "content=" + encodeURIComponent(content)
    }).then(response => response.json())
    .then(data => alert(data.message));
}

function clearNote() {
    fetch("/clear", {
        method: "POST"
    }).then(response => response.json())
    .then(data => {
        noteTextarea.value = "";
        alert(data.message);
    });
}

function loadNote() {
    fetch("/load")
    .then(response => response.json())
    .then(data => {
        if (data.content) {
            noteTextarea.value = data.content;
        } else if (data.message) {
            console.error(data.message);
        }
    });
}

function copyNote() {
    noteTextarea.select();
    document.execCommand("copy");
    alert("Note copied to clipboard!");
}

function startRecording() {
    if (!recognition) {
        alert("Speech recognition is not supported in your browser.");
        return;
    }

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

    recognition.start();
    isRecording = true;
    startSpeechButton.disabled = true;
    stopSpeechButton.disabled = false;
}

function stopRecording() {
    recognition.stop();
    if (audioContext) {
        audioContext.close();
    }
    isRecording = false;
    startSpeechButton.disabled = false;
    stopSpeechButton.disabled = true;
}

function drawWaveform() {
    if (!isRecording) return;

    requestAnimationFrame(drawWaveform);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = "rgb(255, 255, 255)";
    canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = "rgb(0, 0, 0)";

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

saveButton.addEventListener("click", saveNote);
clearButton.addEventListener("click", clearNote);
startSpeechButton.addEventListener("click", startRecording);
stopSpeechButton.addEventListener("click", stopRecording);
copyButton.addEventListener("click", copyNote);

window.onload = loadNote;

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        console.log("Microphone access granted");
    })
    .catch(function(err) {
        console.log("Error accessing microphone", err);
    });
