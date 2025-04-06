function showHealthForm() {
    document.getElementById('healthForm').style.display = 'block';
}

async function submitHealthForm(event) {
    event.preventDefault();
    
    const formData = {
        height: document.getElementById('height').value,
        weight: document.getElementById('weight').value,
        age: document.getElementById('age').value,
        activity_level: document.getElementById('activity').value,
        conditions: document.getElementById('conditions').value || 'None',
        goals: document.getElementById('goals').value || 'General health improvement'
    };

    try {
        const response = await fetch('/api/health-recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('recommendations').innerHTML = `
                <div class="recommendation-section">
                    <h3>Health Status</h3>
                    <p>${data.recommendations.overview}</p>
                </div>
                <div class="recommendation-section">
                    <h3>Your Personalized Plan</h3>
                    ${formatRecommendations(data.recommendations.details)}
                </div>
            `;
            
            document.getElementById('recommendations').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error submitting form: ' + error);
    }
}

function formatRecommendations(text) {
    return text.split('\n').map(line => {
        line = line.trim();
        if (!line) return '';
        if (line.match(/^\d\./)) {
            return `<h4>${line}</h4>`;
        }
        return `<p>${line}</p>`;
    }).join('');
}

async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;
    
    addMessageToChat(message, 'user');
    userInput.value = '';

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        if (response.ok) {
            addMessageToChat(data.response, 'system');
        } else {
            addMessageToChat('Sorry, there was an error processing your request.', 'system');
        }
    } catch (error) {
        addMessageToChat('Sorry, there was an error processing your request.', 'system');
    }
}

function addMessageToChat(message, type) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add enter key support for chat
if (document.getElementById('userInput')) {
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
} 