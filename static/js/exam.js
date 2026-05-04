// Exam Timer and Navigation Logic

let timeRemaining = 0;
let timerInterval = null;

function initExamTimer(totalSeconds) {
    timeRemaining = totalSeconds;
    updateTimerDisplay();
    
    // Start countdown
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();
        
        // Warning when less than 60 seconds
        if (timeRemaining <= 60) {
            document.getElementById('timer').classList.add('timer-warning');
        }
        
        // Auto-submit when time runs out
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            autoSubmitExam();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    const display = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    document.getElementById('timer-display').textContent = display;
}

function autoSubmitExam() {
    showToast('Time is up! Submitting exam...', 'warning');
    
    // Save current answer
    saveCurrentAnswer('submit');
    
    // Redirect to submit
    setTimeout(() => {
        window.location.href = '/exam/submit';
    }, 1000);
}

function saveCurrentAnswer(action) {
    const questionId = document.getElementById('question_id').value;
    let answer = '';
    
    // Get answer based on question type
    const radioAnswer = document.querySelector('input[name="answer"]:checked');
    if (radioAnswer) {
        answer = radioAnswer.value;
    } else {
        const textAnswer = document.getElementById('answer_text');
        if (textAnswer) {
            answer = textAnswer.value;
        }
    }
    
    // Send to server
    return fetch('/exam/answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_id: questionId,
            answer: answer,
            action: action
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        return data;
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error saving answer', 'danger');
    });
}

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    
    if (type === 'warning') {
        toast.style.backgroundColor = '#ffc107';
        toast.style.color = '#000';
    } else if (type === 'danger') {
        toast.style.backgroundColor = '#dc3545';
    }
    
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Next button
    const nextBtn = document.getElementById('next-btn');
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            const action = this.textContent.includes('Submit') ? 'submit' : 'next';
            
            // Show toast on answer selection
            const radioAnswer = document.querySelector('input[name="answer"]:checked');
            const textAnswer = document.getElementById('answer_text');
            
            if (radioAnswer || (textAnswer && textAnswer.value.trim())) {
                showToast('Answer saved!');
            }
            
            saveCurrentAnswer(action);
        });
    }
    
    // Previous button
    const prevBtn = document.getElementById('prev-btn');
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            saveCurrentAnswer('previous');
        });
    }
    
    // Radio button change event
    const radioButtons = document.querySelectorAll('input[name="answer"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Highlight selected option
            document.querySelectorAll('.option-item').forEach(item => {
                item.style.backgroundColor = '#fff';
            });
            this.closest('.option-item').style.backgroundColor = '#e7f3ff';
        });
    });
    
    // Restore selected option highlight
    const selectedRadio = document.querySelector('input[name="answer"]:checked');
    if (selectedRadio) {
        selectedRadio.closest('.option-item').style.backgroundColor = '#e7f3ff';
    }
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight' && nextBtn && !nextBtn.disabled) {
            nextBtn.click();
        } else if (e.key === 'ArrowLeft' && prevBtn && !prevBtn.disabled) {
            prevBtn.click();
        }
    });
    
    // REMOVED: No more warning before leaving page during exam
});

// Clear timer on page unload
window.addEventListener('unload', function() {
    if (timerInterval) {
        clearInterval(timerInterval);
    }
});
