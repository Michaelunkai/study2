const questions = [
    {
        question: "Which command is used to list files in a directory?",
        options: ["ls", "cd", "mkdir", "rm"],
        correct: 0,
        hint: "It stands for 'list'."
    },
    {
        question: "Which command is used to change directory?",
        options: ["ls", "cd", "mkdir", "rm"],
        correct: 1,
        hint: "It stands for 'change directory'."
    },
    {
        question: "Which command is used to create a new directory?",
        options: ["ls", "cd", "mkdir", "rm"],
        correct: 2,
        hint: "It stands for 'make directory'."
    },
    {
        question: "Which command is used to remove a file?",
        options: ["ls", "cd", "mkdir", "rm"],
        correct: 3,
        hint: "It stands for 'remove'."
    },
    {
        question: "Which command is used to display the current directory?",
        options: ["pwd", "ls", "cd", "mkdir"],
        correct: 0,
        hint: "It stands for 'print working directory'."
    },
    {
        question: "Which command is used to move or rename a file?",
        options: ["mv", "cp", "rm", "ls"],
        correct: 0,
        hint: "It stands for 'move'."
    },
    {
        question: "Which command is used to copy files?",
        options: ["mv", "cp", "rm", "ls"],
        correct: 1,
        hint: "It stands for 'copy'."
    },
    {
        question: "Which command is used to display the contents of a file?",
        options: ["cat", "ls", "cd", "rm"],
        correct: 0,
        hint: "It stands for 'concatenate'."
    },
    {
        question: "Which command is used to change file permissions?",
        options: ["chmod", "chown", "chgrp", "chperm"],
        correct: 0,
        hint: "It stands for 'change mode'."
    },
    {
        question: "Which command is used to search for a text pattern in a file?",
        options: ["grep", "find", "locate", "search"],
        correct: 0,
        hint: "It stands for 'global regular expression print'."
    }
];

function loadQuiz() {
    const quizDiv = document.getElementById('quiz');
    questions.forEach((q, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question';
        questionDiv.innerHTML = `
            <p>${q.question}</p>
            ${q.options.map((option, i) => `
                <label>
                    <input type="radio" name="question${index}" value="${i}">
                    ${option}
                </label>
            `).join('')}
            <button onclick="showHint(${index})">Hint</button>
            <button onclick="showAnswer(${index})">Answer</button>
            <p class="hint" id="hint${index}" style="display:none;">${q.hint}</p>
            <p class="answer" id="answer${index}" style="display:none;">Correct Answer: ${q.options[q.correct]}</p>
        `;
        quizDiv.appendChild(questionDiv);
    });
}

function showHint(index) {
    document.getElementById(`hint${index}`).style.display = 'block';
}

function showAnswer(index) {
    document.getElementById(`answer${index}`).style.display = 'block';
}

function finishQuiz() {
    let score = 0;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    questions.forEach((q, index) => {
        const selected = document.querySelector(`input[name="question${index}"]:checked`);
        if (selected && parseInt(selected.value) === q.correct) {
            score += 10; // Each question is worth 10 points
        } else if (selected) {
            const wrongAnswer = document.createElement('p');
            wrongAnswer.innerHTML = `Question: ${q.question} <br> Your Answer: ${q.options[selected.value]} <br> Correct Answer: ${q.options[q.correct]}`;
            wrongAnswer.style.color = 'red';
            resultDiv.appendChild(wrongAnswer);
        }
    });
    const scoreDiv = document.createElement('p');
    scoreDiv.innerText = `Your score: ${score}/100`;
    resultDiv.appendChild(scoreDiv);
}

document.getElementById('finishBtn').addEventListener('click', finishQuiz);

window.onload = loadQuiz;
