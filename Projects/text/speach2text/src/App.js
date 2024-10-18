import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [interimText, setInterimText] = useState('');
  const [finalText, setFinalText] = useState('');
  const [language, setLanguage] = useState('');
  const canvasRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const dataArrayRef = useRef(null);

  useEffect(() => {
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcript + ' ';
        } else {
          interimTranscript += transcript;
        }
      }

      setFinalText(prevText => prevText + finalTranscript);
      setInterimText(interimTranscript);
    };

    recognition.onlanguagechange = (event) => {
      setLanguage(event.language === 'en-US' ? 'English' : 'Hebrew');
    };

    return () => {
      recognition.stop();
    };
  }, []);

  useEffect(() => {
    if (isRecording) {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      const analyser = audioContext.createAnalyser();
      analyser.fftSize = 2048;
      const bufferLength = analyser.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const source = audioContext.createMediaStreamSource(stream);
          source.connect(analyser);
        });

      audioContextRef.current = audioContext;
      analyserRef.current = analyser;
      dataArrayRef.current = dataArray;

      drawWaveform();
    } else if (audioContextRef.current) {
      audioContextRef.current.close();
    }
  }, [isRecording]);

  const toggleRecording = () => {
    if (isRecording) {
      recognition.stop();
      setFinalText(prevText => prevText + interimText);
      setInterimText('');
    } else {
      setFinalText('');
      setInterimText('');
      setLanguage('');
      recognition.start();
    }
    setIsRecording(!isRecording);
  };

  const drawWaveform = () => {
    const canvas = canvasRef.current;
    const canvasCtx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;

    const draw = () => {
      requestAnimationFrame(draw);

      analyserRef.current.getByteTimeDomainData(dataArrayRef.current);

      canvasCtx.fillStyle = 'rgb(0, 0, 0)';
      canvasCtx.fillRect(0, 0, width, height);

      canvasCtx.lineWidth = 2;
      canvasCtx.strokeStyle = 'rgb(255, 255, 255)';

      canvasCtx.beginPath();

      const sliceWidth = width * 1.0 / dataArrayRef.current.length;
      let x = 0;

      for (let i = 0; i < dataArrayRef.current.length; i++) {
        const v = dataArrayRef.current[i] / 128.0;
        const y = v * height / 2;

        if (i === 0) {
          canvasCtx.moveTo(x, y);
        } else {
          canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      canvasCtx.lineTo(canvas.width, canvas.height / 2);
      canvasCtx.stroke();
    };

    draw();
  };

  return (
    <div className="App">
      <button onClick={toggleRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      <canvas ref={canvasRef} width="800" height="200" />
      {language && <p>Detected Language: {language}</p>}
      <div className="text-area">
        {finalText}
        <span className="interim">{interimText}</span>
      </div>
    </div>
  );
}

export default App;
