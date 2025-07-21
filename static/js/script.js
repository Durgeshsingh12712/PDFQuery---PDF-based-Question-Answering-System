let documentUploaded = false;
        let isProcessing = false;
        let messageHistory = [];

        // DOM elements
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('fileInput');
        const fileStatus = document.getElementById('fileStatus');
        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const inputStatus = document.getElementById('inputStatus');
        const emptyState = document.getElementById('emptyState');
        const historyList = document.getElementById('historyList');

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            setupEventListeners();
            loadHistory();
        });

        function setupEventListeners() {
            // File upload
            uploadArea.addEventListener('click', () => fileInput.click());
            fileInput.addEventListener('change', handleFileUpload);

            // Drag and drop
            uploadArea.addEventListener('dragover', handleDragOver);
            uploadArea.addEventListener('dragleave', handleDragLeave);
            uploadArea.addEventListener('drop', handleDrop);

            // Message input
            messageInput.addEventListener('input', handleInputChange);
            messageInput.addEventListener('keypress', handleKeyPress);
        }

        function handleDragOver(e) {
            e.preventDefault();
            uploadArea.style.background = 'rgba(16,163,127,0.1)';
        }

        function handleDragLeave(e) {
            e.preventDefault();
            uploadArea.style.background = '';
        }

        function handleDrop(e) {
            e.preventDefault();
            uploadArea.style.background = '';
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFiles(files);
            }
        }

        function handleFileUpload(e) {
            const files = e.target.files;
            if (files.length > 0) {
                handleFiles(files);
            }
        }

        function handleFiles(files) {
            // Validate files
            const validFiles = Array.from(files).filter(file => {
                const isValidType = file.name.toLowerCase().endsWith('.pdf') || 
                                  file.name.toLowerCase().endsWith('.txt');
                const isValidSize = file.size <= 20 * 1024 * 1024; // 20MB
                return isValidType && isValidSize;
            });

            if (validFiles.length === 0) {
                showStatus('fileStatus', 'error', 'Please select valid PDF or TXT files under 20MB');
                return;
            }

            uploadFiles(validFiles);
        }

        async function uploadFiles(files) {
            if (isProcessing) return;

            isProcessing = true;
            showStatus('fileStatus', 'info', 'Uploading and processing files...');

            try {
                const formData = new FormData();
                files.forEach(file => formData.append('file', file));

                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (response.ok) {
                    documentUploaded = true;
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.placeholder = 'Ask anything about your documents...';
                    
                    showStatus('fileStatus', 'success', 
                        `✅ Successfully processed ${result.files_processed} files`);
                    
                    // Hide empty state
                    emptyState.style.display = 'none';
                    
                    // Add welcome message
                    addMessage('Hello! I\'ve processed your documents and I\'m ready to answer questions about them. What would you like to know?', 'bot');
                    
                } else {
                    showStatus('fileStatus', 'error', result.error);
                }
            } catch (error) {
                showStatus('fileStatus', 'error', 'Upload failed. Please try again.');
            } finally {
                isProcessing = false;
            }
        }

        function handleInputChange() {
            // Auto-resize textarea
            messageInput.style.height = 'auto';
            messageInput.style.height = messageInput.scrollHeight + 'px';
        }

        function handleKeyPress(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            
            if (!message || isProcessing || !documentUploaded) return;

            isProcessing = true;
            sendButton.disabled = true;
            
            // Add user message
            addMessage(message, 'user');
            messageInput.value = '';
            messageInput.style.height = 'auto';
            
            // Add typing indicator
            const typingMessage = addMessage('', 'bot', true);
            
            try {
                const response = await fetch('/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ question: message })
                });

                const result = await response.json();
                
                // Remove typing indicator
                typingMessage.remove();
                
                if (response.ok) {
                    addMessage(result.response, 'bot', false, result.sources);
                    updateHistory(message, result.response);
                } else {
                    addMessage('Sorry, I encountered an error: ' + result.error, 'bot');
                }
            } catch (error) {
                typingMessage.remove();
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            } finally {
                isProcessing = false;
                sendButton.disabled = false;
            }
        }

        function addMessage(content, sender, isTyping = false, sources = null) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message';
            
            const avatar = document.createElement('div');
            avatar.className = `message-avatar ${sender}-avatar`;
            avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
            
            const messageContent = document.createElement('div');
            messageContent.className = 'message-content';
            
            if (isTyping) {
                messageContent.innerHTML = `
                    <div class="typing-indicator">
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                        <div class="typing-dot"></div>
                    </div>
                `;
            } else {
                messageContent.innerHTML = `<div class="message-text">${content}</div>`;
                
                if (sources && sources.length > 0) {
                    const sourcesDiv = document.createElement('div');
                    sourcesDiv.className = 'message-sources';
                    sourcesDiv.innerHTML = `
                        <div class="sources-title">Sources:</div>
                        ${sources.map(source => `
                            <div class="source-item">
                                "${source.content}" - ${source.metadata.source || 'Document'}
                            </div>
                        `).join('')}
                    `;
                    messageContent.appendChild(sourcesDiv);
                }
            }
            
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(messageContent);
            
            chatMessages.appendChild(messageDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            return messageDiv;
        }

        // Add this new function to format message content
function formatMessageContent(content) {
    // Convert markdown-like formatting to HTML
    let formatted = content
        // Convert **bold** to <strong>
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Convert *italic* to <em>
        .replace(/(?<!\*)\*(?!\*)([^*]+)\*(?!\*)/g, '<em>$1</em>')
        // Convert `code` to <code>
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        // Convert line breaks to paragraphs
        .split('\n\n')
        .map(paragraph => paragraph.trim())
        .filter(paragraph => paragraph.length > 0)
        .map(paragraph => `<p>${paragraph.replace(/\n/g, '<br>')}</p>`)
        .join('');
    
    // If no paragraphs were created, wrap the whole content
    if (!formatted.includes('<p>')) {
        formatted = `<p>${content.replace(/\n/g, '<br>')}</p>`;
    }
    
    return formatted;
}

        function showStatus(elementId, type, message) {
            const element = document.getElementById(elementId);
            element.innerHTML = `
                <div class="status-message status-${type}">
                    <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
                    ${message}
                </div>
            `;
        }

        function updateHistory(question, answer) {
            messageHistory.unshift({
                question: question.substring(0, 50) + (question.length > 50 ? '...' : ''),
                timestamp: new Date().toLocaleString()
            });
            
            // Keep only last 10 items
            messageHistory = messageHistory.slice(0, 10);
            renderHistory();
        }

        function renderHistory() {
            historyList.innerHTML = messageHistory.map(item => `
                <div class="history-item">
                    <i class="fas fa-message"></i>
                    <div>
                        <div style="font-weight: 500;">${item.question}</div>
                        <div style="font-size: 0.7rem; opacity: 0.7;">${item.timestamp}</div>
                    </div>
                </div>
            `).join('');
        }

        async function clearSession() {
            if (!confirm('Clear all messages and uploaded documents?')) return;
            
            try {
                const response = await fetch('/clear', { method: 'POST' });
                
                if (response.ok) {
                    // Reset UI
                    chatMessages.innerHTML = '';
                    emptyState.style.display = 'flex';
                    messageInput.disabled = true;
                    sendButton.disabled = true;
                    messageInput.placeholder = 'Message PDFQuery...';
                    documentUploaded = false;
                    messageHistory = [];
                    fileStatus.innerHTML = '';
                    renderHistory();
                    
                    showStatus('fileStatus', 'success', 'Session cleared successfully');
                }
            } catch (error) {
                showStatus('fileStatus', 'error', 'Failed to clear session');
            }
        }

        function showSampleQuestions() {
            const samples = [
                "What is the main topic of this document?",
                "Can you summarize the key points?",
                "What are the conclusions mentioned?",
                "Are there any important dates or numbers?"
            ];
            
            samples.forEach(question => {
                const quickAction = document.createElement('div');
                quickAction.className = 'quick-action';
                quickAction.textContent = question;
                quickAction.onclick = () => {
                    messageInput.value = question;
                    messageInput.focus();
                };
                emptyState.appendChild(quickAction);
            });
        }

        function toggleSidebar() {
            document.querySelector('.sidebar').classList.toggle('show');
        }

        async function loadHistory() {
            try {
                const response = await fetch('/history');
                const result = await response.json();
                
                if (response.ok && result.history) {
                    messageHistory = result.history.map(item => ({
                        question: item.question.substring(0, 50) + (item.question.length > 50 ? '...' : ''),
                        timestamp: new Date(item.timestamp).toLocaleString()
                    })).slice(0, 10);
                    renderHistory();
                }
            } catch (error) {
                console.error('Failed to load history:', error);
            }
        }