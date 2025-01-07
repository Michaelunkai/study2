import React, { useState } from 'react';
import '@fontsource/lobster';
import { Container, Typography, RadioGroup, FormControlLabel, Radio, Button, Box, Alert } from '@mui/material';
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
    <Container className="container">
      <Typography variant="h3" className="title" gutterBottom>
        Junior Sys Admin Exam
      </Typography>
      <Box id="quiz">
        {questions.map((q, index) => (
          <Box key={index} className="question">
            <Typography variant="h6" component="p">{q.question}</Typography>
            <RadioGroup
              name={`question${index}`}
              value={answers[index]}
              onChange={(e) => handleSelect(index, parseInt(e.target.value))}
            >
              {q.options.map((option, i) => (
                <FormControlLabel key={i} value={i} control={<Radio />} label={option} />
              ))}
            </RadioGroup>
            <Button variant="contained" color="info" onClick={() => alert(q.hint)}>Hint</Button>
          </Box>
        ))}
      </Box>
      <Button variant="contained" color="primary" id="finishBtn" onClick={handleSubmit}>
        Finish & Test
      </Button>
      {showResults && (
        <Box id="result" mt={3}>
          {questions.map((q, index) => {
            const correct = answers[index] === q.correct;
            return (
              <Box key={index} mb={2}>
                {!correct && (
                  <Alert severity="error">
                    <Typography>Question: {q.question}</Typography>
                    <Typography>Your Answer: {q.options[answers[index]]}</Typography>
                    <Typography>Correct Answer: {q.options[q.correct]}</Typography>
                  </Alert>
                )}
              </Box>
            );
          })}
          <Alert severity="success">
            <Typography>Your score: {answers.filter((a, i) => a === questions[i].correct).length * 10}/100</Typography>
          </Alert>
        </Box>
      )}
    </Container>
  );
}

export default App;
