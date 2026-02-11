// Math Study AI - Frontend Script

// Dynamically set API base URL
const API_BASE_URL = (() => {
    // In production, use the same host as the frontend
    const protocol = window.location.protocol; // http: or https:
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // If running on localhost or development
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'http://localhost:5000/api';
    }
    
    // In production (same domain)
    const baseUrl = `${protocol}//${hostname}${port ? ':' + port : ''}`;
    return `${baseUrl}/api`;
})();

console.log('API Base URL:', API_BASE_URL);

// DOM Elements
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const resetBtn = document.getElementById('resetBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const toast = document.getElementById('toast');
const navButtons = document.querySelectorAll('.nav-btn');
const pageTitle = document.getElementById('pageTitle');
const pageDescription = document.getElementById('pageDescription');

// Page content
const modeContents = {
    chat: document.getElementById('chatMode'),
    explain: document.getElementById('explainMode'),
    solve: document.getElementById('solveMode'),
    resources: document.getElementById('resourcesMode')
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('Math Study AI loaded');
    setupEventListeners();
    loadResources();
});

// Event Listeners Setup
function setupEventListeners() {
    // Navigation buttons
    navButtons.forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });
    
    // Chat form
    chatForm.addEventListener('submit', sendMessage);
    
    // Reset button
    resetBtn.addEventListener('click', resetConversation);
    
    // Explain form
    document.querySelector('#explainMode form')?.addEventListener('submit', explainConcept);
    
    // Solve form
    document.querySelector('#solveMode form')?.addEventListener('submit', solveProblem);
    
    // Resources form
    document.querySelector('#resourcesMode form')?.addEventListener('submit', searchResources);
}

// Mode Switching
function switchMode(mode) {
    // Update active nav button
    navButtons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.mode === mode) btn.classList.add('active');
    });
    
    // Update page title
    const titles = {
        chat: { title: 'Chat with Your AI Math Tutor', desc: 'Ask any math question and get instant help' },
        explain: { title: 'Explain a Math Concept', desc: 'Get clear, step-by-step explanations' },
        solve: { title: 'Solve a Problem', desc: 'Get detailed solutions with explanations' },
        resources: { title: 'Find Learning Resources', desc: 'Discover helpful math learning websites and tools' }
    };
    
    if (titles[mode]) {
        pageTitle.textContent = titles[mode].title;
        pageDescription.textContent = titles[mode].desc;
    }
    
    // Switch content
    Object.keys(modeContents).forEach(key => {
        modeContents[key].classList.remove('active');
    });
    if (modeContents[mode]) {
        modeContents[mode].classList.add('active');
    }
}

// Send Message (Chat Mode)
function sendMessage(event) {
    event.preventDefault();
    
    const message = chatInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    chatInput.value = '';
    
    // Show loading
    showLoading(true);
    
    // Send to backend
    fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        if (data.success) {
            addMessage(data.message, 'bot');
        } else {
            addMessage(`Error: ${data.error || 'Failed to get response'}`, 'bot');
            showToast(data.error || 'Error processing your message', 'error');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Error:', error);
        addMessage('Error: Unable to connect to the server. Make sure the backend is running.', 'bot');
        showToast('Connection error. Is the server running?', 'error');
    });
}

// Add Message to Chat
function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Explain Concept
function explainConcept(event) {
    event.preventDefault();
    
    const concept = document.getElementById('conceptInput').value.trim();
    if (!concept) return;
    
    showLoading(true);
    
    fetch(`${API_BASE_URL}/explain`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ concept })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        const responseDiv = document.getElementById('explainResponse');
        if (data.success) {
            responseDiv.innerHTML = `
                <div class="response-area">
                    <h4>Explanation of: ${data.concept}</h4>
                    <p>${formatText(data.explanation)}</p>
                </div>
            `;
            showToast('Concept explained!', 'success');
        } else {
            responseDiv.innerHTML = `<div class="response-area"><p style="color: red;">Error: ${data.error}</p></div>`;
            showToast(data.error || 'Error', 'error');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Error:', error);
        document.getElementById('explainResponse').innerHTML = 
            `<div class="response-area"><p style="color: red;">Error: ${error.message}</p></div>`;
    });
}

// Solve Problem
function solveProblem(event) {
    event.preventDefault();
    
    const problem = document.getElementById('problemInput').value.trim();
    if (!problem) return;
    
    showLoading(true);
    
    fetch(`${API_BASE_URL}/solve`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ problem })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        const responseDiv = document.getElementById('solveResponse');
        if (data.success) {
            responseDiv.innerHTML = `
                <div class="response-area">
                    <h4>Solution</h4>
                    <p>${formatText(data.solution)}</p>
                </div>
            `;
            showToast('Problem solved!', 'success');
        } else {
            responseDiv.innerHTML = `<div class="response-area"><p style="color: red;">Error: ${data.error}</p></div>`;
            showToast(data.error || 'Error', 'error');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Error:', error);
        document.getElementById('solveResponse').innerHTML = 
            `<div class="response-area"><p style="color: red;">Error: ${error.message}</p></div>`;
    });
}

// Search Resources
function searchResources(event) {
    event.preventDefault();
    
    const query = document.getElementById('resourceSearch').value.trim();
    if (!query) return;
    
    showLoading(true);
    
    fetch(`${API_BASE_URL}/resources/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query })
    })
    .then(response => response.json())
    .then(data => {
        showLoading(false);
        const resourcesList = document.getElementById('resourcesList');
        
        if (data.success && data.count > 0) {
            let html = `<h3>Found ${data.count} resource(s)</h3>`;
            data.resources.forEach(resource => {
                html += `
                    <div class="resource-card">
                        <h4>${resource.Title}</h4>
                        <p>${resource.Description}</p>
                        <div class="meta">
                            <span>📚 ${resource.Topic}</span>
                            <span>⭐ ${resource.Difficulty}</span>
                            <span>🎯 ${resource.Type}</span>
                        </div>
                        <a href="${resource.URL}" target="_blank">Visit Resource →</a>
                    </div>
                `;
            });
            resourcesList.innerHTML = html;
            showToast(`Found ${data.count} resources!`, 'success');
        } else {
            resourcesList.innerHTML = '<p>No resources found for your query.</p>';
            showToast('No resources found', 'error');
        }
    })
    .catch(error => {
        showLoading(false);
        console.error('Error:', error);
        document.getElementById('resourcesList').innerHTML = 
            `<p style="color: red;">Error: ${error.message}</p>`;
    });
}

// Load Resources on Startup
function loadResources() {
    fetch(`${API_BASE_URL}/resources`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`Loaded ${data.count} resources`);
            }
        })
        .catch(error => {
            console.error('Error loading resources:', error);
            showToast('Failed to load resources', 'error');
        });
}

// Reset Conversation
function resetConversation() {
    if (confirm('Reset conversation? This will clear the chat history.')) {
        fetch(`${API_BASE_URL}/chat/reset`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-content">
                        👋 Hello! I'm your Math Tutor AI. Ask me anything about mathematics. What can I help you with today?
                    </div>
                </div>
            `;
            showToast('Conversation reset', 'success');
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error resetting conversation', 'error');
        });
    }
}

// Utility Functions

// Show/Hide Loading Spinner
function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

// Show Toast Notification
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Format Text with Basic Markdown
function formatText(text) {
    if (!text) return '';
    
    // Replace line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italic text
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Code blocks
    text = text.replace(/```(.*?)```/gs, '<pre>$1</pre>');
    
    // Inline code
    text = text.replace(/`(.*?)`/g, '<code>$1</code>');
    
    return text;
}

// API Error Handler
function handleApiError(error) {
    console.error('API Error:', error);
    showToast('An error occurred. Please try again.', 'error');
}

// Health Check (Optional)
function checkServerHealth() {
    fetch(`${API_BASE_URL}/../health`)
        .then(response => response.json())
        .then(data => {
            console.log('Server health:', data);
        })
        .catch(error => {
            console.warn('Server not available. Make sure to start the backend.', error);
        });
}

// Run health check on load
setTimeout(checkServerHealth, 1000);
