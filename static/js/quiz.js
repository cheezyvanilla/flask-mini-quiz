let currentScore = parseInt(document.getElementById('total-score').innerText || 0);
const questionBox = document.getElementById('question-box');
const questionText = document.getElementById('question-text');
const choicesBox = document.getElementById('choices');
const feedback = document.getElementById('feedback');
const nextBtn = document.getElementById('next-button');

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
            console.log(data);
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

    console.log(selected, answer)
    if (selected === answer) {
        feedback.textContent = '✅ Correct!';
        feedback.style.color = 'green';
        currentScore += 10;
        document.getElementById('total-score').textContent = currentScore;

        fetch('/api/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: currentScore })
        });

        buttons.forEach(btn => {
            if (btn.textContent === selected) btn.classList.add('correct');
        });

    } else {
        feedback.textContent = '❌ Incorrect!';
        feedback.style.color = 'red';

        buttons.forEach(btn => {
            if (btn.textContent === selected) btn.classList.add('incorrect');
            if (btn.textContent === currentQuestion.answer) btn.classList.add('correct');
        });
    }

    nextBtn.style.display = 'block';
}

nextBtn.onclick = () => loadQuestion(questionText.textContent);

window.onload = loadQuestion;
