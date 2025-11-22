// frontend/js/my_orders.js - Authenticated user orders

const API_URL = 'http://localhost:5000';

// Check if user is logged in
function checkAuth() {
    const user = localStorage.getItem('user');
    if (!user) {
        // Not logged in, redirect to login
        window.location.href = 'login.html';
        return null;
    }
    return JSON.parse(user);
}

// Logout function
document.getElementById('logoutBtn').addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('user');
        localStorage.removeItem('userId');
        window.location.href = 'login.html';
    }
});

// Load user's orders
async function loadMyOrders() {
    const user = checkAuth();
    if (!user) return;

    try {
        // Display user info
        document.getElementById('userName').textContent = `Welcome, ${user.first_name || user.email}`;
        document.getElementById('userEmail').textContent = user.email;

        // Fetch user's orders
        const response = await fetch(`${API_URL}/api/auth/user/${user.id}/orders`);
        
        if (!response.ok) {
            throw new Error('Failed to load orders');
        }

        const data = await response.json();
        document.getElementById('loading').style.display = 'none';

        if (data.orders.length === 0) {
            document.getElementById('noOrders').style.display = 'block';
        } else {
            displayOrders(data.orders);
            document.getElementById('ordersContainer').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = error.message || 'Failed to load orders';
        errorDiv.style.display = 'block';
    }
}

// Display orders
function displayOrders(orders) {
    const ordersList = document.getElementById('ordersList');
    
    ordersList.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <h3>Order #${order.id}</h3>
                <span class="order-date">${new Date(order.created_at).toLocaleDateString()}</span>
            </div>
            
            <div class="order-details">
                <p><strong>Name:</strong> ${order.customer_name}</p>
                <p><strong>Phone:</strong> ${order.customer_phone}</p>
                ${order.customer_address ? `<p><strong>Address:</strong> ${order.customer_address}</p>` : ''}
            </div>

            <div class="order-items">
                <h4>Items:</h4>
                <ul>
                    ${order.items.map(item => `
                        <li>
                            ${item.item_name} x${item.quantity} - $${parseFloat(item.subtotal).toFixed(2)}
                        </li>
                    `).join('')}
                </ul>
            </div>

            <div class="order-total">
                <strong>Total: $${parseFloat(order.total_amount).toFixed(2)}</strong>
            </div>
        </div>
    `).join('');
}

// Load on page load
window.addEventListener('load', loadMyOrders);