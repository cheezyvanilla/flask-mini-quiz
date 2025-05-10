let currentScore = parseInt(document.getElementById('total-score').innerText || 0);
const questionBox = document.getElementById('question-box');
const questionText = document.getElementById('question-text');
const choicesBox = document.getElementById('choices');
const feedback = document.getElementById('feedback');
const nextBtn = document.getElementById('next-button');
const scoreboardList = document.getElementById('scoreboard-list');

let currentQuestion = null;

function loadQuestion(prev_question = '') {
    feedback.textContent = 'Loading...';
    nextBtn.style.display = 'none';
    const encodedPrev = encodeURIComponent(prev_question);

    fetch(`/api/quiz?prev_question=${encodedPrev}`)
        .then(res => res.json())
        .then(data => {
            currentQuestion = data;
            questionText.textContent = data.question;
            feedback.textContent = '';
            choicesBox.innerHTML = '';

            data.choices.forEach((choice, idx) => {
                const btn = document.createElement('button');
                btn.classList.add('choice-btn');
                btn.textContent = choice;
                btn.onclick = () => handleAnswer(idx, data.answer);
                choicesBox.appendChild(btn);
            });
        });
}

function handleAnswer(selected, answer) {
    const buttons = document.querySelectorAll('.choice-btn');
    buttons.forEach(btn => btn.disabled = true);

    const selectedText = currentQuestion.choices[selected];
    const correctText = currentQuestion.choices[answer];

    if (selected === answer) {
        feedback.textContent = '✅ Correct!';
        feedback.style.color = 'green';
        currentScore += 10;
        document.getElementById('total-score').textContent = currentScore;

        // Update score
        fetch('/api/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: currentScore })
        }).then(loadScoreboard);

        // Highlight correct button
        buttons.forEach(btn => {
            if (btn.textContent === correctText) btn.classList.add('correct');
        });

    } else {
        feedback.textContent = '❌ Incorrect!';
        feedback.style.color = 'red';

        buttons.forEach(btn => {
            if (btn.textContent === selectedText) btn.classList.add('incorrect');
            if (btn.textContent === correctText) btn.classList.add('correct');
        });
    }

    nextBtn.style.display = 'block';
}

function loadScoreboard() {
    fetch('/api/scoreboard')
        .then(res => res.json())
        .then(data => {
            scoreboardList.innerHTML = '';
            data.forEach(user => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${user.username}</span> <span>${user.score}</span>`;
                scoreboardList.appendChild(li);
            });
        });
}

nextBtn.onclick = () => loadQuestion(questionText.textContent);

window.onload = () => {
    loadQuestion("Apa itu AI dalam konteks pemrograman Python? and Apa yang dimaksud dengan AI (Artificial Intelligence)?");
    loadScoreboard();
};
