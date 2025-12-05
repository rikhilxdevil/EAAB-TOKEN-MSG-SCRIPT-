"""
Facebook Group Messenger - Complete Working Script
Supports EAAB, EAAG, EAAU, EAAD Token Formats
Author: Facebook Messenger Bot
"""

import os
import time
import threading
import requests
from flask import Flask, render_template_string, request, jsonify, session
from datetime import datetime
import json

# ==================== FLASK APP SETUP ====================
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24).hex()

# ==================== HTML TEMPLATE ====================
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Group Messenger</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            padding: 30px;
        }
        
        h1 {
            color: #1877f2;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 25px;
            border: 1px solid #e0e0e0;
        }
        
        .card h2 {
            color: #333;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .card h2 i {
            color: #1877f2;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #444;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        input[type="text"],
        input[type="number"],
        input[type="file"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus {
            outline: none;
            border-color: #1877f2;
        }
        
        small {
            display: block;
            margin-top: 5px;
            color: #666;
            font-size: 0.9em;
        }
        
        .form-actions {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        
        button {
            padding: 14px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #1877f2 0%, #0d5cb6 100%);
            color: white;
            flex: 1;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(24, 119, 242, 0.4);
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
            margin-top: 10px;
            padding: 10px 15px;
        }
        
        .btn-secondary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(108, 117, 125, 0.4);
        }
        
        .btn-danger {
            background: linear-gradient(135deg, #dc3545 0%, #b02a37 100%);
            color: white;
            flex: 1;
        }
        
        .btn-danger:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none !important;
            box-shadow: none !important;
        }
        
        /* Token formats display */
        .token-info {
            margin-top: 15px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        .token-formats {
            display: flex;
            gap: 10px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .token-format {
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            font-family: monospace;
            font-size: 1.1em;
            border: 2px solid;
        }
        
        .eaab { background: #e3f2fd; color: #1565c0; border-color: #1565c0; }
        .eaag { background: #f3e5f5; color: #7b1fa2; border-color: #7b1fa2; }
        .eaau { background: #e8f5e9; color: #2e7d32; border-color: #2e7d32; }
        .eaad { background: #fff3e0; color: #ef6c00; border-color: #ef6c00; }
        
        /* Validation results */
        .validation-result {
            margin-top: 10px;
            padding: 10px;
            border-radius: 6px;
        }
        
        .loading {
            color: #0d6efd;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .success {
            color: #198754;
            background: #d1e7dd;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #badbcc;
        }
        
        .error {
            color: #dc3545;
            background: #f8d7da;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #f5c2c7;
        }
        
        /* Status indicators */
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        
        .status-dot.idle { background: #6c757d; }
        .status-dot.sending { 
            background: #0d6efd; 
            animation: pulse 1.5s infinite; 
        }
        .status-dot.error { background: #dc3545; }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Progress bar */
        .progress-bar {
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin: 20px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #1877f2, #764ba2);
            width: 0%;
            transition: width 0.3s;
        }
        
        /* Results display */
        .results-summary {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        
        .result-item {
            flex: 1;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .result-item.success { background: #d1e7dd; color: #198754; }
        .result-item.failed { background: #f8d7da; color: #dc3545; }
        .result-item.total { background: #cfe2ff; color: #0d6efd; }
        
        .detailed-results {
            max-height: 300px;
            overflow-y: auto;
            margin-top: 20px;
            padding-right: 10px;
        }
        
        .result-success, .result-failed {
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 6px;
            border-left: 4px solid;
            font-size: 0.9em;
        }
        
        .result-success {
            background: #d1e7dd;
            border-left-color: #198754;
        }
        
        .result-failed {
            background: #f8d7da;
            border-left-color: #dc3545;
        }
        
        /* Instructions */
        .instructions {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
        }
        
        .instructions h3 {
            margin-bottom: 15px;
            color: #1565c0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .instructions ol {
            margin-left: 20px;
            margin-bottom: 20px;
        }
        
        .instructions li {
            margin-bottom: 8px;
            line-height: 1.5;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffecb5;
            color: #856404;
            padding: 15px;
            border-radius: 6px;
            display: flex;
            align-items: flex-start;
            gap: 10px;
            margin-top: 15px;
        }
        
        .warning i {
            color: #ffc107;
            margin-top: 2px;
        }
        
        code {
            background: #f1f1f1;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 0.9em;
        }
        
        /* Console log */
        .console-log {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            margin-top: 20px;
            max-height: 200px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        
        .log-entry {
            margin-bottom: 5px;
            padding: 2px 0;
            border-bottom: 1px solid #333;
        }
        
        .log-time {
            color: #888;
            font-size: 0.8em;
        }
        
        .log-success { color: #00ff00; }
        .log-error { color: #ff5555; }
        .log-info { color: #55aaff; }
        .log-warning { color: #ffff55; }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .form-actions {
                flex-direction: column;
            }
            
            .results-summary {
                flex-direction: column;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .token-formats {
                justify-content: center;
            }
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        .fa-spin {
            animation: fa-spin 1s infinite linear;
        }
        
        @keyframes fa-spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <h1><i class="fab fa-facebook-messenger"></i> Facebook Group Messenger</h1>
        <p class="subtitle">Send messages to Facebook groups using EAAB/EAAG/EAAU/EAAD tokens</p>
        
        <div class="card">
            <h2><i class="fas fa-cogs"></i> Configuration</h2>
            
            <form id="messageForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="access_token">
                        <i class="fas fa-key"></i> Facebook Access Token
                    </label>
                    <input type="text" id="access_token" name="access_token" 
                           placeholder="Enter EAAB, EAAG, EAAU, or EAAD format token" required>
                    <button type="button" id="validateTokenBtn" class="btn-secondary">
                        <i class="fas fa-check-circle"></i> Validate Token
                    </button>
                    <div id="tokenValidation" class="validation-result"></div>
                    
                    <div class="token-info">
                        <h4><i class="fas fa-info-circle"></i> Supported Token Formats:</h4>
                        <div class="token-formats">
                            <span class="token-format eaab">EAAB</span>
                            <span class="token-format eaag">EAAG</span>
                            <span class="token-format eaau">EAAU</span>
                            <span class="token-format eaad">EAAD</span>
                        </div>
                        <small>Currently Available: EAAB (Others may work if you have valid tokens)</small>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="thread_id">
                        <i class="fas fa-users"></i> Group Thread ID
                    </label>
                    <input type="text" id="thread_id" name="thread_id" 
                           placeholder="Enter Facebook Group ID" required>
                    <small>Find Group ID from Facebook Group URL (e.g., 123456789012345)</small>
                </div>
                
                <div class="form-group">
                    <label for="prefix">
                        <i class="fas fa-tag"></i> Message Prefix (Optional)
                    </label>
                    <input type="text" id="prefix" name="prefix" 
                           placeholder="e.g., IMPORTANT:, NOTICE:, UPDATE:, etc.">
                </div>
                
                <div class="form-group">
                    <label for="delay_seconds">
                        <i class="fas fa-clock"></i> Delay Between Messages (Seconds)
                    </label>
                    <input type="number" id="delay_seconds" name="delay_seconds" 
                           value="2" min="1" max="60" step="1" required>
                    <small>Minimum 1 second, Maximum 60 seconds (to avoid rate limiting)</small>
                </div>
                
                <div class="form-group">
                    <label for="message_file">
                        <i class="fas fa-file-alt"></i> Messages File (.txt)
                    </label>
                    <input type="file" id="message_file" name="message_file" 
                           accept=".txt" required>
                    <small>Upload a .txt file with one message per line (UTF-8 encoding recommended)</small>
                </div>
                
                <div class="form-actions">
                    <button type="submit" id="startBtn" class="btn-primary">
                        <i class="fas fa-paper-plane"></i> Start Sending Messages
                    </button>
                    <button type="button" id="stopBtn" class="btn-danger" disabled>
                        <i class="fas fa-stop-circle"></i> Stop Sending
                    </button>
                    <button type="button" id="clearLogBtn" class="btn-secondary">
                        <i class="fas fa-broom"></i> Clear Log
                    </button>
                </div>
            </form>
        </div>
        
        <div class="card">
            <h2><i class="fas fa-chart-bar"></i> Status & Results</h2>
            <div id="statusPanel">
                <div class="status-indicator" id="statusIndicator">
                    <div class="status-dot idle"></div>
                    <span>Ready to send messages</span>
                </div>
                
                <div id="progressSection" style="display: none;">
                    <div class="progress-bar">
                        <div id="progressFill" class="progress-fill"></div>
                    </div>
                    <p id="progressText">Preparing to send messages...</p>
                </div>
                
                <div id="resultsSection" style="display: none;">
                    <h3><i class="fas fa-history"></i> Last Operation Results</h3>
                    <div class="results-summary">
                        <div class="result-item success">
                            <i class="fas fa-check-circle"></i>
                            <span id="successCount">0</span> Successful
                        </div>
                        <div class="result-item failed">
                            <i class="fas fa-times-circle"></i>
                            <span id="failedCount">0</span> Failed
                        </div>
                        <div class="result-item total">
                            <i class="fas fa-envelope"></i>
                            <span id="totalCount">0</span> Total
                        </div>
                    </div>
                    
                    <div id="detailedResults" class="detailed-results">
                        <!-- Results will be displayed here -->
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2><i class="fas fa-terminal"></i> Console Log</h2>
            <div id="consoleLog" class="console-log">
                <div class="log-entry log-info">
                    <span class="log-time">[{{ current_time }}]</span> System: Application started successfully
                </div>
                <div class="log-entry log-info">
                    <span class="log-time">[{{ current_time }}]</span> System: Ready to send messages
                </div>
            </div>
        </div>
        
        <div class="instructions">
            <h3><i class="fas fa-graduation-cap"></i> How to Use:</h3>
            <ol>
                <li><strong>Get Facebook Access Token:</strong> Use Facebook Graph API Explorer or Business Manager to get a token starting with EAAB, EAAG, EAAU, or EAAD</li>
                <li><strong>Get Group Thread ID:</strong> From Facebook Group URL or use Graph API to find your group ID</li>
                <li><strong>Prepare Messages File:</strong> Create a .txt file with one message per line</li>
                <li><strong>Configure Settings:</strong> Set message prefix and delay between messages</li>
                <li><strong>Validate Token:</strong> Click "Validate Token" to check if token is working</li>
                <li><strong>Start Sending:</strong> Click "Start Sending Messages" to begin</li>
                <li><strong>Monitor Progress:</strong> Watch the console log for real-time updates</li>
            </ol>
            
            <div class="warning">
                <i class="fas fa-exclamation-triangle"></i>
                <div>
                    <strong>Important Notes:</strong>
                    <ul style="margin-top: 10px; margin-left: 20px;">
                        <li>Ensure your token has these permissions: <code>pages_messaging</code>, <code>pages_manage_metadata</code></li>
                        <li>Respect Facebook's rate limits (use appropriate delays)</li>
                        <li>EAAB tokens are currently the most reliable format</li>
                        <li>Test with 1-2 messages first before sending bulk messages</li>
                        <li>Keep delay between 2-5 seconds to avoid being blocked</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.getElementById('messageForm');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            const clearLogBtn = document.getElementById('clearLogBtn');
            const validateTokenBtn = document.getElementById('validateTokenBtn');
            const statusIndicator = document.getElementById('statusIndicator');
            const progressSection = document.getElementById('progressSection');
            const resultsSection = document.getElementById('resultsSection');
            const tokenValidation = document.getElementById('tokenValidation');
            const consoleLog = document.getElementById('consoleLog');
            
            let checkStatusInterval = null;
            let isSending = false;
            
            // Add log entry to console
            function addLogEntry(message, type = 'info') {
                const now = new Date();
                const timeString = now.toLocaleTimeString();
                const logEntry = document.createElement('div');
                logEntry.className = `log-entry log-${type}`;
                logEntry.innerHTML = `<span class="log-time">[${timeString}]</span> ${message}`;
                consoleLog.appendChild(logEntry);
                consoleLog.scrollTop = consoleLog.scrollHeight;
            }
            
            // Clear console log
            clearLogBtn.addEventListener('click', function() {
                consoleLog.innerHTML = '';
                addLogEntry('Console log cleared', 'info');
            });
            
            // Validate Token Button
            validateTokenBtn.addEventListener('click', function() {
                const token = document.getElementById('access_token').value.trim();
                
                if (!token) {
                    tokenValidation.innerHTML = '<div class="error"><i class="fas fa-times-circle"></i> Please enter a token</div>';
                    addLogEntry('Token validation failed: No token entered', 'error');
                    return;
                }
                
                // Check token format
                const validPrefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD'];
                const tokenPrefix = token.substring(0, 4).toUpperCase();
                
                if (!validPrefixes.includes(tokenPrefix)) {
                    tokenValidation.innerHTML = `
                        <div class="error">
                            <i class="fas fa-times-circle"></i> 
                            Invalid token format. Must start with: ${validPrefixes.join(', ')}
                        </div>
                    `;
                    addLogEntry(`Token validation failed: Invalid format (${tokenPrefix})`, 'error');
                    return;
                }
                
                tokenValidation.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Validating token...</div>';
                addLogEntry(`Validating ${tokenPrefix} format token...`, 'info');
                
                const formData = new FormData();
                formData.append('access_token', token);
                
                fetch('/validate_token', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.valid) {
                        tokenValidation.innerHTML = `
                            <div class="success">
                                <i class="fas fa-check-circle"></i> 
                                Token is valid! 
                                <strong>${data.format}</strong> format detected.
                                <br>
                                <small>User: ${data.name} (ID: ${data.user_id})</small>
                            </div>
                        `;
                        addLogEntry(`Token validation successful: ${data.name} (${data.user_id}) - ${data.format} format`, 'success');
                    } else {
                        tokenValidation.innerHTML = `
                            <div class="error">
                                <i class="fas fa-times-circle"></i> 
                                ${data.error || 'Token validation failed'}
                            </div>
                        `;
                        addLogEntry(`Token validation failed: ${data.error || 'Unknown error'}`, 'error');
                    }
                })
                .catch(error => {
                    tokenValidation.innerHTML = `
                        <div class="error">
                            <i class="fas fa-times-circle"></i> 
                            Network error: ${error.message}
                        </div>
                    `;
                    addLogEntry(`Network error during token validation: ${error.message}`, 'error');
                });
            });
            
            // Start Sending Messages
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                // Get form values
                const token = document.getElementById('access_token').value.trim();
                const threadId = document.getElementById('thread_id').value.trim();
                const prefix = document.getElementById('prefix').value.trim();
                const delaySeconds = document.getElementById('delay_seconds').value;
                const fileInput = document.getElementById('message_file');
                
                // Validation
                if (!token) {
                    alert('Please enter an access token');
                    addLogEntry('Error: No access token provided', 'error');
                    return;
                }
                
                if (!threadId) {
                    alert('Please enter a Group Thread ID');
                    addLogEntry('Error: No Group Thread ID provided', 'error');
                    return;
                }
                
                if (!fileInput.files.length) {
                    alert('Please select a messages file');
                    addLogEntry('Error: No messages file selected', 'error');
                    return;
                }
                
                // Check token format
                const validPrefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD'];
                const tokenPrefix = token.substring(0, 4).toUpperCase();
                
                if (!validPrefixes.includes(tokenPrefix)) {
                    alert(`Invalid token format. Must start with: ${validPrefixes.join(', ')}`);
                    addLogEntry(`Error: Invalid token format (${tokenPrefix})`, 'error');
                    return;
                }
                
                // Update UI
                startBtn.disabled = true;
                stopBtn.disabled = false;
                isSending = true;
                
                // Update status
                statusIndicator.innerHTML = `
                    <div class="status-dot sending"></div>
                    <span>Sending messages...</span>
                `;
                progressSection.style.display = 'block';
                resultsSection.style.display = 'none';
                
                // Start checking status
                if (checkStatusInterval) {
                    clearInterval(checkStatusInterval);
                }
                checkStatusInterval = setInterval(checkSendingStatus, 3000);
                
                // Log start
                addLogEntry(`Starting message sending to Group ID: ${threadId}`, 'info');
                addLogEntry(`Using ${tokenPrefix} format token with ${delaySeconds}s delay`, 'info');
                
                // Send form data
                const formData = new FormData(form);
                
                fetch('/send', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        alert('Error: ' + data.error);
                        addLogEntry(`Error starting message sending: ${data.error}`, 'error');
                        resetUI();
                    } else {
                        addLogEntry('Message sending started successfully', 'success');
                    }
                })
                .catch(error => {
                    alert('Network error: ' + error.message);
                    addLogEntry(`Network error: ${error.message}`, 'error');
                    resetUI();
                });
            });
            
            // Stop Sending Messages
            stopBtn.addEventListener('click', function() {
                if (!isSending) return;
                
                addLogEntry('Stopping message sending...', 'warning');
                
                fetch('/stop', {
                    method: 'POST'
                })
                .then(response => response.json())
                .then(data => {
                    alert('Message sending stopped');
                    addLogEntry('Message sending stopped by user', 'warning');
                    resetUI();
                })
                .catch(error => {
                    alert('Error: ' + error.message);
                    addLogEntry(`Error stopping: ${error.message}`, 'error');
                });
            });
            
            // Check sending status
            function checkSendingStatus() {
                fetch('/status')
                .then(response => response.json())
                .then(data => {
                    if (!data.sending_active && isSending) {
                        // Sending finished
                        clearInterval(checkStatusInterval);
                        isSending = false;
                        
                        if (data.last_results && data.last_results.total > 0) {
                            displayResults(data.last_results);
                            resetUI(false);
                        } else {
                            resetUI();
                        }
                    } else if (data.sending_active) {
                        // Still sending - update progress
                        updateProgress();
                    }
                })
                .catch(error => {
                    console.error('Error checking status:', error);
                });
            }
            
            // Display results
            function displayResults(results) {
                document.getElementById('successCount').textContent = results.successful;
                document.getElementById('failedCount').textContent = results.failed;
                document.getElementById('totalCount').textContent = results.total;
                
                const detailedResults = document.getElementById('detailedResults');
                detailedResults.innerHTML = '';
                
                // Log summary
                addLogEntry(`Message sending completed: ${results.successful} successful, ${results.failed} failed out of ${results.total} total`, 
                           results.failed === 0 ? 'success' : 'warning');
                
                if (results.details && results.details.length > 0) {
                    results.details.forEach(result => {
                        const resultItem = document.createElement('div');
                        resultItem.className = result.success ? 'result-success' : 'result-failed';
                        resultItem.innerHTML = `
                            <strong>Message ${result.message_number}:</strong>
                            ${result.content.substring(0, 80)}${result.content.length > 80 ? '...' : ''}
                            ${result.error ? `<br><small><i class="fas fa-exclamation-circle"></i> Error: ${result.error}</small>` : ''}
                        `;
                        detailedResults.appendChild(resultItem);
                        
                        // Log individual result
                        if (result.success) {
                            addLogEntry(`✓ Message ${result.message_number} sent successfully`, 'success');
                        } else {
                            addLogEntry(`✗ Failed to send message ${result.message_number}: ${result.error}`, 'error');
                        }
                    });
                }
                
                resultsSection.style.display = 'block';
            }
            
            // Update progress indicator
            function updateProgress() {
                const progressFill = document.getElementById('progressFill');
                const progressText = document.getElementById('progressText');
                
                // Animate progress bar
                const width = progressFill.style.width || '0%';
                const currentWidth = parseInt(width) || 0;
                let newWidth = currentWidth + 5;
                
                if (newWidth > 95) newWidth = 5;
                
                progressFill.style.width = newWidth + '%';
                
                // Update text
                const messages = [
                    'Sending messages...',
                    'Processing messages file...',
                    'Communicating with Facebook API...',
                    'Waiting between messages...'
                ];
                const randomMessage = messages[Math.floor(Math.random() * messages.length)];
                progressText.textContent = randomMessage;
            }
            
            // Reset UI
            function resetUI(enableStart = true) {
                startBtn.disabled = !enableStart;
                stopBtn.disabled = true;
                isSending = false;
                
                statusIndicator.innerHTML = `
                    <div class="status-dot ${enableStart ? 'idle' : 'error'}"></div>
                    <span>${enableStart ? 'Ready to send messages' : 'Stopped'}</span>
                `;
                
                progressSection.style.display = 'none';
                document.getElementById('progressFill').style.width = '0%';
                
                if (checkStatusInterval) {
                    clearInterval(checkStatusInterval);
                    checkStatusInterval = null;
                }
            }
            
            // Auto-check token format
            document.getElementById('access_token').addEventListener('input', function(e) {
                const token = e.target.value.trim();
                if (token.length >= 4) {
                    const prefix = token.substring(0, 4).toUpperCase();
                    const validPrefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD'];
                    
                    if (validPrefixes.includes(prefix)) {
                        e.target.style.borderColor = '#198754';
                        e.target.style.backgroundColor = '#f8fff9';
                    } else {
                        e.target.style.borderColor = '#dc3545';
                        e.target.style.backgroundColor = '#fff8f8';
                    }
                } else {
                    e.target.style.borderColor = '#ddd';
                    e.target.style.backgroundColor = '';
                }
            });
        });
    </script>
</body>
</html>
'''

# ==================== GLOBAL VARIABLES ====================
sending_active = False
current_thread = None
message_results = []

# ==================== HELPER FUNCTIONS ====================
def send_message_to_group(access_token, thread_id, message):
    """Send message to Facebook group using Graph API"""
    url = f"https://graph.facebook.com/v18.0/{thread_id}/messages"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'message': message,
        'access_token': access_token
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return {'success': True, 'message': 'Message sent successfully'}
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            error_code = error_data.get('error', {}).get('code', response.status_code)
            return {
                'success': False, 
                'error': f'Error {error_code}: {error_msg}'
            }
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Request timeout - Facebook API not responding'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Connection error - Check your internet'}
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}

def send_messages_from_file(access_token, thread_id, file_path, prefix, delay_seconds):
    """Read messages from file and send them with delay"""
    global sending_active, message_results
    
    message_results = []  # Reset results
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            messages = [line.strip() for line in file if line.strip()]
        
        if not messages:
            message_results.append({
                'success': False,
                'error': 'No messages found in file. File is empty or contains only blank lines.'
            })
            return message_results
        
        total_messages = len(messages)
        
        for i, message in enumerate(messages):
            if not sending_active:
                break
                
            # Add prefix if provided
            full_message = f"{prefix} {message}" if prefix else message
            
            # Send message
            result = send_message_to_group(access_token, thread_id, full_message)
            
            # Store result
            result_data = {
                'message_number': i + 1,
                'content': full_message,
                'success': result['success'],
                'error': result.get('error', '')
            }
            message_results.append(result_data)
            
            # Calculate progress percentage
            progress_percent = int(((i + 1) / total_messages) * 100)
            
            # Print to console (server-side)
            if result['success']:
                print(f"[✓] Message {i+1}/{total_messages} ({progress_percent}%) - Sent successfully")
            else:
                print(f"[✗] Message {i+1}/{total_messages} ({progress_percent}%) - Failed: {result.get('error')}")
            
            # Delay between messages (except for the last one)
            if i < total_messages - 1 and sending_active:
                for second in range(int(delay_seconds)):
                    if not sending_active:
                        break
                    time.sleep(1)
        
        return message_results
    except UnicodeDecodeError:
        error_msg = 'File encoding error. Please save file as UTF-8.'
        message_results.append({'success': False, 'error': error_msg})
        return message_results
    except Exception as e:
        error_msg = f'File processing error: {str(e)}'
        message_results.append({'success': False, 'error': error_msg})
        return message_results

# ==================== FLASK ROUTES ====================
@app.route('/')
def index():
    """Render main page"""
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template_string(HTML_TEMPLATE, current_time=current_time)

@app.route('/send', methods=['POST'])
def send_messages():
    """Start sending messages"""
    global sending_active, current_thread
    
    if sending_active:
        return jsonify({'success': False, 'error': 'Already sending messages. Please stop first.'})
    
    # Get form data
    access_token = request.form.get('access_token', '').strip()
    thread_id = request.form.get('thread_id', '').strip()
    prefix = request.form.get('prefix', '').strip()
    delay_seconds = float(request.form.get('delay_seconds', 2))
    
    # Validate inputs
    if not access_token:
        return jsonify({'success': False, 'error': 'Access token is required'})
    
    # Validate token format
    valid_prefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD']
    token_prefix = access_token[:4].upper()
    
    if token_prefix not in valid_prefixes:
        return jsonify({
            'success': False, 
            'error': f'Invalid token format. Only {", ".join(valid_prefixes)} formats are supported.'
        })
    
    if not thread_id or not thread_id.isdigit():
        return jsonify({'success': False, 'error': 'Valid Thread ID (numbers only) is required'})
    
    if delay_seconds < 1 or delay_seconds > 60:
        return jsonify({'success': False, 'error': 'Delay must be between 1 and 60 seconds'})
    
    # Check if file was uploaded
    if 'message_file' not in request.files:
        return jsonify({'success': False, 'error': 'Message file is required'})
    
    file = request.files['message_file']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if not file.filename.endswith('.txt'):
        return jsonify({'success': False, 'error': 'Only .txt files are supported'})
    
    # Save uploaded file
    upload_dir = 'uploads'
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"messages_{int(time.time())}.txt")
    file.save(file_path)
    
    # Print starting info
    print(f"\n{'='*60}")
    print("STARTING MESSAGE SENDING")
    print(f"{'='*60}")
    print(f"Token Format: {token_prefix}")
    print(f"Group ID: {thread_id}")
    print(f"Prefix: '{prefix}'")
    print(f"Delay: {delay_seconds} seconds")
    print(f"File: {file.filename}")
    print(f"{'='*60}\n")
    
    # Start sending messages in a separate thread
    sending_active = True
    
    def send_messages_thread():
        global sending_active, message_results
        try:
            results = send_messages_from_file(
                access_token, 
                thread_id, 
                file_path, 
                prefix, 
                delay_seconds
            )
            
            # Print summary
            successful = sum(1 for r in results if r.get('success'))
            failed = sum(1 for r in results if not r.get('success'))
            
            print(f"\n{'='*60}")
            print("MESSAGE SENDING COMPLETE")
            print(f"{'='*60}")
            print(f"Total Messages: {len(results)}")
            print(f"Successful: {successful}")
            print(f"Failed: {failed}")
            print(f"Success Rate: {(successful/len(results)*100 if results else 0):.1f}%")
            print(f"{'='*60}")
            
        except Exception as e:
            print(f"\n[ERROR] Thread error: {str(e)}")
        finally:
            sending_active = False
            # Clean up uploaded file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except:
                pass
    
    current_thread = threading.Thread(target=send_messages_thread)
    current_thread.daemon = True
    current_thread.start()
    
    return jsonify({
        'success': True, 
        'message': f'Message sending started with {token_prefix} token format',
        'token_format': token_prefix
    })

@app.route('/status')
def get_status():
    """Get current sending status"""
    global sending_active, message_results
    
    # Calculate results if sending is complete
    if not sending_active and message_results:
        successful = sum(1 for r in message_results if r.get('success'))
        failed = sum(1 for r in message_results if not r.get('success'))
        total = len(message_results)
        
        results_data = {
            'total': total,
            'successful': successful,
            'failed': failed,
            'details': message_results[:50]  # Limit details to last 50 messages
        }
    else:
        results_data = {}
    
    return jsonify({
        'sending_active': sending_active,
        'last_results': results_data
    })

@app.route('/stop', methods=['POST'])
def stop_sending():
    """Stop sending messages"""
    global sending_active
    sending_active = False
    return jsonify({'success': True, 'message': 'Stopping message sending...'})

@app.route('/validate_token', methods=['POST'])
def validate_token():
    """Validate Facebook access token"""
    access_token = request.form.get('access_token', '').strip()
    
    if not access_token:
        return jsonify({'valid': False, 'error': 'Token is required'})
    
    # Check token format
    valid_prefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD']
    token_prefix = access_token[:4].upper()
    
    if token_prefix not in valid_prefixes:
        return jsonify({
            'valid': False, 
            'error': f'Invalid format. Must start with: {", ".join(valid_prefixes)}'
        })
    
    # Try to validate with Facebook API
    try:
        url = "https://graph.facebook.com/v18.0/me"
        params = {
            'access_token': access_token,
            'fields': 'id,name,email'
        }
        
        print(f"\n[TOKEN VALIDATION] Testing {token_prefix} format token...")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"[TOKEN VALIDATION] ✓ Valid token for user: {data.get('name')} (ID: {data.get('id')})")
            
            # Additional check for page permissions
            pages_url = "https://graph.facebook.com/v18.0/me/accounts"
            pages_response = requests.get(pages_url, params={'access_token': access_token}, timeout=10)
            
            has_pages = pages_response.status_code == 200
            
            return jsonify({
                'valid': True,
                'user_id': data.get('id'),
                'name': data.get('name'),
                'format': token_prefix,
                'has_pages': has_pages
            })
        else:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Token is invalid or expired')
            print(f"[TOKEN VALIDATION] ✗ Invalid token: {error_msg}")
            
            return jsonify({
                'valid': False,
                'error': error_msg
            })
    except requests.exceptions.Timeout:
        print("[TOKEN VALIDATION] ✗ Timeout - Facebook API not responding")
        return jsonify({'valid': False, 'error': 'Timeout - Facebook API not responding'})
    except Exception as e:
        print(f"[TOKEN VALIDATION] ✗ Error: {str(e)}")
        return jsonify({'valid': False, 'error': str(e)})

@app.route('/check_token_format', methods=['POST'])
def check_token_format():
    """Quick check of token format"""
    access_token = request.form.get('access_token', '').strip()
    
    if not access_token or len(access_token) < 4:
        return jsonify({'valid_format': False, 'format': 'Unknown'})
    
    token_prefix = access_token[:4].upper()
    valid_prefixes = ['EAAB', 'EAAG', 'EAAU', 'EAAD']
    
    return jsonify({
        'valid_format': token_prefix in valid_prefixes,
        'format': token_prefix if token_prefix in valid_prefixes else 'Invalid',
        'suggested_formats': valid_prefixes
    })

# ==================== MAIN EXECUTION ====================
if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Clear old uploads
    for file in os.listdir('uploads'):
        try:
            file_path = os.path.join('uploads', file)
            # Remove files older than 1 hour
            if os.path.getmtime(file_path) < time.time() - 3600:
                os.remove(file_path)
        except:
            pass
    
    # Print startup banner
    print("\n" + "="*70)
    print("FACEBOOK GROUP MESSENGER - COMPLETE WORKING SCRIPT")
    print("="*70)
    print("Author: Facebook Messenger Bot")
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Supported Token Formats: EAAB, EAAG, EAAU, EAAD")
    print("Port: 5000")
    print("="*70)
    print("\nIMPORTANT NOTES:")
    print("1. Use EAAB format tokens for best results")
    print("2. Ensure token has 'pages_messaging' permission")
    print("3. Use appropriate delays (2-5 seconds recommended)")
    print("4. Test with 1-2 messages first")
    print("="*70 + "\n")
    
    # Run the application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
