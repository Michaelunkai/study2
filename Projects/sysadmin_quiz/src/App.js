import React, { useState } from 'react';
import '@fontsource/lobster';
import './App.css';

const questions = [
  {
    question: "Which command is used to see the disk usage of a directory?",
    options: ["du", "df", "ls", "diskusage"],
    correct: 0,
    hint: "It stands for 'disk usage'."
  },
  {
    question: "Which command is used to see the space available on a filesystem?",
    options: ["du", "df", "ls", "filesystem"],
    correct: 1,
    hint: "It stands for 'disk free'."
  },
  {
    question: "Which command is used to terminate a process by its PID?",
    options: ["kill", "terminate", "stop", "end"],
    correct: 0,
    hint: "It is a strong word."
  },
  {
    question: "Which command is used to find the location of a file?",
    options: ["find", "locate", "search", "grep"],
    correct: 1,
    hint: "It has a database of filenames and locations."
  },
  {
    question: "Which command is used to change the owner of a file?",
    options: ["chmod", "chown", "chgrp", "chuser"],
    correct: 1,
    hint: "It stands for 'change owner'."
  },
  {
    question: "Which command is used to view the last few lines of a file?",
    options: ["head", "tail", "cat", "less"],
    correct: 1,
    hint: "It is the opposite of 'head'."
  },
  {
    question: "Which command is used to archive files?",
    options: ["tar", "zip", "gzip", "ar"],
    correct: 0,
    hint: "It stands for 'tape archive'."
  },
  {
    question: "Which command is used to display network interfaces?",
    options: ["ifconfig", "netstat", "ipconfig", "network"],
    correct: 0,
    hint: "It is specific to Unix/Linux."
  },
  {
    question: "Which command is used to display routing tables?",
    options: ["route", "netstat", "ip route", "routing"],
    correct: 0,
    hint: "It is also a common English word."
  },
  {
    question: "Which command is used to edit a file in the terminal?",
    options: ["vim", "edit", "nano", "vi"],
    correct: 0,
    hint: "It is an improved version of 'vi'."
  }
];

function App() {
  const [answers, setAnswers] = useState(Array(questions.length).fill(null));
  const [showResults, setShowResults] = useState(false);

  const handleSelect = (index, optionIndex) => {
    const newAnswers = [...answers];
    newAnswers[index] = optionIndex;
    setAnswers(newAnswers);
  };

  const handleSubmit = () => {
    setShowResults(true);
  };

  return (
    <div className="container">
      <h1>Junior Sys Admin Exam</h1>
      <div id="quiz">
        {questions.map((q, index) => (
          <div key={index} className="question">
            <p>{q.question}</p>
            {q.options.map((option, i) => (
              <label key={i}>
                <input
                  type="radio"
                  name={`question${index}`}
                  value={i}
                  checked={answers[index] === i}
                  onChange={() => handleSelect(index, i)}
                />
                {option}
              </label>
            ))}
            <button onClick={() => alert(q.hint)}>Hint</button>
          </div>
        ))}
      </div>
      <button id="finishBtn" onClick={handleSubmit}>Finish & Test</button>
      {showResults && (
        <div id="result">
          {questions.map((q, index) => {
            const correct = answers[index] === q.correct;
            return (
              <div key={index}>
                {!correct && (
                  <p style={{ color: 'red' }}>
                    Question: {q.question} <br />
                    Your Answer: {q.options[answers[index]]} <br />
                    Correct Answer: {q.options[q.correct]}
                  </p>
                )}
              </div>
            );
          })}
          <p>Your score: {answers.filter((a, i) => a === questions[i].correct).length * 10}/100</p>
        </div>
      )}
    </div>
  );
}

export default App;
