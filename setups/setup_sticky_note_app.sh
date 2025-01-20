#!/bin/ 
mkdir -p sticky_note_app/templates sticky_note_app/static
cd sticky_note_app

cat > app.py << EOL
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import  ite3

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = " ite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

def init_db():
    db_path = os.path.join(app.instance_path, "notes.db")
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))
    conn =  ite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT NOT NULL)")
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save", methods=["POST"])
def save():
    content = request.form["content"]
    if content:
        try:
            new_note = Notes(content=content)
            db.session.add(new_note)
            db.session.commit()
            return jsonify({"status": "success", "message": "Note saved successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"Error saving note: {str(e)}"})
    else:
        return jsonify({"status": "error", "message": "Cannot save an empty note."})

@app.route("/clear", methods=["POST"])
def clear():
    try:
        Notes.query.delete()
        db.session.commit()
        return jsonify({"status": "success", "message": "All notes cleared successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error clearing notes: {str(e)}"})

@app.route("/load", methods=["GET"])
def load():
    try:
        note = Notes.query.order_by(Notes.id.desc()).first()
        content = note.content if note else ""
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error loading note: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4444))
    app.run(host="0.0.0.0", port=port, debug=True)
EOL

cat > templates/index.html << EOL
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sticky Note App with Speech-to-Text</title>
    <style>
        body {
            background-color: rgb(255, 215, 0);
            font-family: "Arial", sans-serif;
            font-size: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        #note {
            width: 100%;
            height: 300px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        button {
            font-size: 18px;
            margin: 5px;
            padding: 10px 20px;
            cursor: pointer;
        }
        #waveform {
            border: 1px solid black;
            margin: 20px 0;
        }
        #language {
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <textarea id="note"></textarea><br>
    <button id="saveNote">Save</button>
    <button id="clearNote">Clear</button>
    <button id="startSpeech">Start Speech-to-Text</button>
    <button id="stopSpeech" disabled>Stop Speech-to-Text</button>
    <button id=" Note"> </button>
    <canvas id="waveform" width="800" height="200"></canvas>
    <p id="language"></p>

    <script src="{{ url_for("static", filename="app.js") }}"></script>
</body>
</html>
EOL

cat > static/app.js << EOL
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

function  Note() {
    noteTextarea.select();
    document.execCommand(" ");
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
 Button.addEventListener("click",  Note);

window.onload = loadNote;

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(function(stream) {
        console.log("Microphone access granted");
    })
    .catch(function(err) {
        console.log("Error accessing microphone", err);
    });
EOL

echo "Project setup complete. To run the app:
1. Install required packages: pip install flask flask-sqlalchemy
2. Run the app: python app.py
3. Open a web browser and go to http://localhost:4444"

