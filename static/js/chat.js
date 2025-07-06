$(document).ready(function() {
    // Initialize variables
    let currentModel = 'rule';
    let messageHistory = [];

    // Handle model switching
    $('.model-btn').on('click', function() {
        const newModel = $(this).data('type');
        if (newModel !== currentModel) {
            $('#switchModal').modal('show');
            
            $('#confirmSwitch').off('click').on('click', function() {
                // Update UI
                $('.model-btn').removeClass('active');
                $(`.model-btn[data-type="${newModel}"]`).addClass('active');
                
                // Update model status text based on selected model
                let modelName = 'Rule-based';
                if (newModel === 'gemini') modelName = 'Gemini';
                $('#modelStatus').text(`Current: ${modelName} Mode`);
                
                // Clear chat and update model
                $('#messageFormeight').empty();
                currentModel = newModel;
                
                // Add system message
                appendMessage('system', `Switched to ${modelName} mode`);
                $('#switchModal').modal('hide');
            });
        }
    });

    // Function to append messages
    function appendMessage(type, message) {
        const messageArea = $('#messageFormeight');
        const timestamp = new Date().toLocaleTimeString();
        let messageHTML = '';

        switch(type) {
            case 'user':
                messageHTML = `
                    <div class="message">
                        <div class="msg_cotainer_send">
                            ${message}
                            <span class="msg_time_send">${timestamp}</span>
                        </div>
                    </div>`;
                break;
            case 'bot':
                messageHTML = `
                    <div class="message">
                        <div class="msg_cotainer">
                            ${message}
                            <span class="msg_time">${timestamp}</span>
                        </div>
                    </div>`;
                break;
            case 'system':
                messageHTML = `
                    <div class="system-message">
                        ${message}
                    </div>`;
                break;
        }

        messageArea.append(messageHTML);
        messageArea.scrollTop(messageArea[0].scrollHeight);
        
        // Save to history
        messageHistory.push({type, message, timestamp});
    }

    function sendMessage() {
        const messageInput = $('#text');
        const message = messageInput.val().trim();
        
        if (message) {
            // Add user message to chat
            appendMessage('user', message);
            messageInput.val('');
            
            // Show loading indicator
            appendMessage('bot', '<div class="loading-indicator">Thinking...</div>');
            
            // Send message to server
            $.ajax({
                url: '/chat',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    message: message,
                    type: currentModel
                }),
                success: function(response) {
                    $('.loading-indicator').remove();
                    if (response.status === 'success') {
                        appendMessage('bot', response.response);
                    } else {
                        appendMessage('system', response.message || 'Error processing your message');
                    }
                },
                error: function(xhr, status, error) {
                    $('.loading-indicator').remove();
                    let errorMessage = 'Server connection failed. ';
                    
                    // More detailed error messages
                    if (xhr.responseJSON && xhr.responseJSON.message) {
                        errorMessage += xhr.responseJSON.message;
                        
                        // Add helpful API key message for Gemini
                        if (currentModel === 'gemini' && 
                            (xhr.responseJSON.message.includes('not available') || 
                             xhr.responseJSON.message.includes('API key'))) {
                            errorMessage = 'Gemini API key not configured. Please set up your API key in the .env file.';
                        }
                    }
                    
                    appendMessage('system', errorMessage);
                    console.error('Ajax error:', {xhr, status, error});
                    
                    // If model failed, switch back to rule-based
                    if (currentModel !== 'rule') {
                        appendMessage('system', 'Switching back to rule-based model...');
                        currentModel = 'rule';
                        $('.model-btn').removeClass('active');
                        $('.model-btn[data-type="rule"]').addClass('active');
                        $('#modelStatus').text('Current: Rule-based Mode');
                    }
                }
            });
        }
    }

    // Function to reset conversation for a specific model
    function resetConversation() {
        const endpoint = currentModel === 'gemini' ? '/reset-gemini-chat' : null;
        
        if (endpoint) {
            $.ajax({
                url: endpoint,
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    $('#messageFormeight').empty();
                    appendMessage('system', 'Conversation has been reset.');
                    appendMessage('bot', 'Hello! How can I help you today?');
                },
                error: function(xhr, status, error) {
                    appendMessage('system', 'Failed to reset conversation. Please try again.');
                    console.error('Reset error:', {xhr, status, error});
                }
            });
        } else {
            // For rule-based, just clear the UI
            $('#messageFormeight').empty();
            appendMessage('system', 'Conversation has been reset.');
            appendMessage('bot', 'Hello! How can I help you today?');
        }
    }

    // Event listeners
    $('#sendBtn').on('click', sendMessage);
    
    $('#text').on('keypress', function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Add reset button functionality
    $('#resetBtn').on('click', function() {
        resetConversation();
    });

    // Initial greeting
    appendMessage('bot', 'Hello! I am currently in Rule-based mode. How can I help you today?');
});

// Escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
    const messageForm = document.getElementById('messageArea');
    messageForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });

    // Image upload handling
    document.getElementById('uploadButton').addEventListener('click', function() {
        document.getElementById('imageUpload').click();
    });

    document.getElementById('imageUpload').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('image', file);

            fetch('/analyze-image', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const chatbox = document.getElementById('messageFormeight');
                const botMessage = `<div class="message">
                    <div class="msg_cotainer">I detect that you're feeling ${data.mood}</div>
                </div>`;
                chatbox.innerHTML += botMessage;
                chatbox.scrollTop = chatbox.scrollHeight;
            });
        }
    });
});