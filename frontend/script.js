const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyze-btn');
    const emailContent = document.getElementById('email-content');
    const loader = document.getElementById('loader');
    const btnText = document.querySelector('.btn-text');
    const resultSection = document.getElementById('result-section');
    const historyList = document.getElementById('history-list');

    // Load history on start
    fetchHistory();

    analyzeBtn.addEventListener('click', async () => {
        const text = emailContent.value.trim();
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        // UI State: Loading
        analyzeBtn.disabled = true;
        loader.style.display = 'block';
        btnText.style.opacity = '0.5';
        resultSection.style.display = 'none';

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text }),
            });

            if (!response.ok) throw new Error('API Error');

            const data = await response.json();
            displayResult(data);
            fetchHistory(); // Refresh history
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to analyze. Make sure backend is running.');
        } finally {
            analyzeBtn.disabled = false;
            loader.style.display = 'none';
            btnText.style.opacity = '1';
        }
    });

    function displayResult(data) {
        resultSection.style.display = 'block';
        const type = data.is_spam ? 'spam' : 'safe';
        const icon = data.is_spam ? '⚠️' : '✅';
        const confidence = (data.confidence * 100).toFixed(1);

        resultSection.innerHTML = `
            <div class="result-card ${type}">
                <div class="status-icon">${icon}</div>
                <div class="status-label">${data.label}</div>
                <div class="confidence">AI Confidence: ${confidence}%</div>
            </div>
        `;
    }

    async function fetchHistory() {
        try {
            const response = await fetch(`${API_URL}/history`);
            const data = await response.json();

            if (data.length === 0) {
                historyList.innerHTML = '<p style="color: var(--text-muted); font-size: 0.9rem;">No recent checks found.</p>';
                return;
            }

            historyList.innerHTML = data.map(item => `
                <div class="history-item">
                    <div class="history-text">${item.text}</div>
                    <div style="display: flex; align-items: center;">
                        <div class="history-tag ${item.is_spam ? 'tag-spam' : 'tag-safe'}">
                            ${item.is_spam ? 'SPAM' : 'SAFE'}
                        </div>
                        <button class="delete-btn" onclick="deleteHistory('${item.id}', event)" title="Remove from history">×</button>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.warn('Could not fetch history');
        }
    }

    // Global function for the onclick handler
    window.deleteHistory = async (id, event) => {
        event.stopPropagation();
        try {
            const response = await fetch(`${API_URL}/history/${id}`, {
                method: 'DELETE'
            });
            if (response.ok) {
                fetchHistory(); // Refresh the list
            }
        } catch (error) {
            console.error('Failed to delete history item:', error);
        }
    };
});
