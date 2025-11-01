// frontend/js/auth.js - Authentication handling

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
    
    // Clear previous messages
    clearErrors();
    
    try {
        button.disabled = true;
        button.textContent = 'Signing in...';
        
        const response = await fetch(`${API_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store user info in localStorage
            localStorage.setItem('user', JSON.stringify(data.user));
            localStorage.setItem('userId', data.user.id);
            
            messageDiv.textContent = '✓ ' + data.message;
            messageDiv.className = 'message success';
            
            // Redirect to orders page after 1.5 seconds
            setTimeout(() => {
                window.location.href = 'orders.html';
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
        button.textContent = 'Sign In';
    }
});

// Handle signup form submission
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const firstNameInput = document.getElementById('signup-first');
    const lastNameInput = document.getElementById('signup-last');
    const emailInput = document.getElementById('signup-email');
    const phoneInput = document.getElementById('signup-phone');
    const passwordInput = document.getElementById('signup-password');
    const confirmInput = document.getElementById('signup-confirm');
    const messageDiv = document.getElementById('signup-message');
    const button = e.target.querySelector('button');
    
    // Clear previous messages and errors
    clearErrors();
    
    // Validation
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
    
    if (phoneInput.value && !validatePhone(phoneInput.value)) {
        showError('signup-phone-error', 'Invalid phone format');
        hasErrors = true;
    }
    
    if (hasErrors) return;
    
    try {
        button.disabled = true;
        button.textContent = 'Creating account...';
        
        const response = await fetch(`${API_URL}/api/auth/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: emailInput.value.trim(),
                password: passwordInput.value,
                first_name: firstNameInput.value.trim(),
                last_name: lastNameInput.value.trim(),
                phone: phoneInput.value.trim()
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            messageDiv.textContent = '✓ Account created! Redirecting to login...';
            messageDiv.className = 'message success';
            
            // Clear form
            e.target.reset();
            
            // Switch to login form after 2 seconds
            setTimeout(() => {
                document.getElementById('signup-email').value = emailInput.value;
                switchForm('login');
                messageDiv.textContent = '';
            }, 2000);
        } else {
            messageDiv.textContent = data.error || 'Signup failed';
            messageDiv.className = 'message error';
            
            // Show specific field errors
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
        button.textContent = 'Create Account';
    }
});

// Helper functions
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        // Add error class to input
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

function validatePhone(phone) {
    const cleaned = phone.replace(/[\s\-().-]/g, '');
    return /^\d{10,}$/.test(cleaned);
}

// Check if user is already logged in
function checkUserSession() {
    const user = localStorage.getItem('user');
    if (user) {
        // User already logged in, redirect to orders
        window.location.href = 'orders.html';
    }
}

// Run on page load
window.addEventListener('load', checkUserSession);