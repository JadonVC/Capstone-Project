// frontend/js/admin_auth.js - Admin authentication handling

const API_URL = 'http://localhost:5000';

// Switch between login and signup forms
function switchForm(formType) {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    
    if (formType === 'login') {
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
    } else {
        signupForm.classList.add('active');
        loginForm.classList.remove('active');
    }
    
    // Clear previous messages
    document.getElementById('login-message').textContent = '';
    document.getElementById('signup-message').textContent = '';
}

// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const messageDiv = document.getElementById('login-message');
    const button = e.target.querySelector('button');
    
    clearErrors();
    
    try {
        button.disabled = true;
        button.textContent = 'Signing in...';
        
        const response = await fetch(`${API_URL}/api/admin/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('admin', JSON.stringify(data.admin));
            localStorage.setItem('adminId', data.admin.id);
            
            messageDiv.textContent = '✓ ' + data.message;
            messageDiv.className = 'message success';
            
            setTimeout(() => {
                window.location.href = 'admin_dashboard.html';
            }, 1500);
        } else {
            messageDiv.textContent = data.error || 'Login failed';
            messageDiv.className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'Connection error. Please try again.';
        messageDiv.className = 'message error';
    } finally {
        button.disabled = false;
        button.textContent = 'Login';
    }
});

// Handle signup form submission
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const firstNameInput = document.getElementById('signup-first');
    const lastNameInput = document.getElementById('signup-last');
    const emailInput = document.getElementById('signup-email');
    const passwordInput = document.getElementById('signup-password');
    const confirmInput = document.getElementById('signup-confirm');
    const messageDiv = document.getElementById('signup-message');
    const button = e.target.querySelector('button');
    
    clearErrors();
    
    let hasErrors = false;
    
    if (!emailInput.value.trim()) {
        showError('signup-email-error', 'Email is required');
        hasErrors = true;
    }
    
    if (!passwordInput.value) {
        showError('signup-password-error', 'Password is required');
        hasErrors = true;
    }
    
    if (passwordInput.value !== confirmInput.value) {
        showError('signup-confirm-error', 'Passwords do not match');
        hasErrors = true;
    }
    
    if (hasErrors) return;
    
    try {
        button.disabled = true;
        button.textContent = 'Creating account...';
        
        const response = await fetch(`${API_URL}/api/admin/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: emailInput.value.trim(),
                password: passwordInput.value,
                first_name: firstNameInput.value.trim(),
                last_name: lastNameInput.value.trim()
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            messageDiv.textContent = 'Account created! Redirecting to login...';
            messageDiv.className = 'message success';
            
            e.target.reset();
            
            setTimeout(() => {
                document.getElementById('signup-email').value = emailInput.value;
                switchForm('login');
                messageDiv.textContent = '';
            }, 2000);
        } else {
            messageDiv.textContent = data.error || 'Signup failed';
            messageDiv.className = 'message error';
            
            if (data.error.includes('email')) {
                showError('signup-email-error', data.error);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.textContent = 'Connection error. Please try again.';
        messageDiv.className = 'message error';
    } finally {
        button.disabled = false;
        button.textContent = 'Create Admin Account';
    }
});

// Helper functions
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        const inputId = elementId.replace('-error', '');
        const input = document.getElementById(inputId);
        if (input) {
            input.classList.add('error');
            input.addEventListener('input', () => {
                input.classList.remove('error');
                element.textContent = '';
            });
        }
    }
}

function clearErrors() {
    document.querySelectorAll('.error-message').forEach(el => {
        el.textContent = '';
    });
    document.querySelectorAll('input').forEach(input => {
        input.classList.remove('error');
    });
}

// Check if admin is already logged in
function checkAdminSession() {
    const admin = localStorage.getItem('admin');
    if (admin) {
        const messageDiv = document.getElementById('login-message');
        if (messageDiv) {
            messageDiv.textContent = 'Already logged in. Redirecting...';
            messageDiv.className = 'message success';
            setTimeout(() => {
                window.location.href = 'admin_dashboard.html';
            }, 1500);
        }
    }
}

window.addEventListener('load', checkAdminSession);