// frontend/js/admin_dashboard.js - Admin dashboard functionality

const API_URL = 'http://localhost:5000';
let statusPollingIntervals = {};

// Check if admin is logged in
function checkAdminAuth() {
    const admin = localStorage.getItem('admin');
    if (!admin) {
        window.location.href = 'admin_login.html';
        return null;
    }
    return JSON.parse(admin);
}

window.addEventListener('load', () => {
    const admin = checkAdminAuth();
    if (admin) {
        document.getElementById('adminName').textContent = `Welcome, ${admin.first_name || admin.email}`;
        loadAllOrders();
        loadOrderManagement();
        loadAllMenuItems();
        loadAllAdmins();
    }
});

// Handle logout
document.getElementById('logoutBtn').addEventListener('click', () => {
    if (confirm('Are you sure you want to logout?')) {
        localStorage.removeItem('admin');
        localStorage.removeItem('adminId');
        window.location.href = 'admin_login.html';
    }
});

// Tab switching logic
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
    
    if (tabName === 'order-management') {
        loadOrderManagement();
    }
}

// Load all orders for orders tab
async function loadAllOrders() {
    try {
        const response = await fetch(`${API_URL}/api/orders/all`);
        
        if (!response.ok) {
            throw new Error('Failed to load orders');
        }
        
        const orders = await response.json();
        displayOrders(orders);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('ordersContainer').innerHTML = `<p class="error">Error loading orders: ${error.message}</p>`;
    }
}

function displayOrders(orders) {
    const container = document.getElementById('ordersContainer');
    
    if (orders.length === 0) {
        container.innerHTML = '<p>No orders yet.</p>';
        return;
    }
    
    container.innerHTML = orders.map(order => `
        <div class="order-card">
            <div class="order-header">
                <h3>Order #${order.id}</h3>
                <span class="order-date">${new Date(order.created_at).toLocaleDateString()}</span>
            </div>
            <div class="order-details">
                <p><strong>Customer:</strong> ${order.customer_name}</p>
                <p><strong>Phone:</strong> ${order.customer_phone}</p>
                ${order.customer_address ? `<p><strong>Address:</strong> ${order.customer_address}</p>` : ''}
                <p><strong>Status:</strong> <span class="status-badge status-${order.order_status}">${order.order_status}</span></p>
            </div>
            <div class="order-items">
                <strong>Items:</strong>
                <ul>
                    ${order.items.map(item => `<li>${item.item_name} x${item.quantity} - $${parseFloat(item.subtotal).toFixed(2)}</li>`).join('')}
                </ul>
            </div>
            <div class="order-total">
                <strong>Total: $${parseFloat(order.total_amount).toFixed(2)}</strong>
            </div>
        </div>
    `).join('');
}

// Load orders for order management tab with status controls
async function loadOrderManagement() {
    try {
        const response = await fetch(`${API_URL}/api/orders/all`);
        
        if (!response.ok) {
            throw new Error('Failed to load orders');
        }
        
        const orders = await response.json();
        displayOrderManagement(orders);
        startOrderPolling();
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('orderManagementContainer').innerHTML = `<p class="error">Error loading orders: ${error.message}</p>`;
    }
}

function displayOrderManagement(orders) {
    const container = document.getElementById('orderManagementContainer');
    
    if (orders.length === 0) {
        container.innerHTML = '<p>No orders yet.</p>';
        return;
    }
    
    container.innerHTML = orders.map(order => `
        <div class="order-management-card">
            <div class="order-mgmt-header">
                <h3>Order #${order.id}</h3>
                <div class="status-control">
                    <label for="status-${order.id}">Status:</label>
                    <select id="status-${order.id}" class="status-dropdown" onchange="updateOrderStatus(${order.id}, this.value)">
                        <option value="pending" ${order.order_status === 'pending' ? 'selected' : ''}>Pending</option>
                        <option value="preparing" ${order.order_status === 'preparing' ? 'selected' : ''}>Preparing</option>
                        <option value="ready" ${order.order_status === 'ready' ? 'selected' : ''}>Ready</option>
                        <option value="completed" ${order.order_status === 'completed' ? 'selected' : ''}>Completed</option>
                    </select>
                </div>
            </div>
            <div class="order-mgmt-details">
                <p><strong>Customer:</strong> ${order.customer_name}</p>
                <p><strong>Phone:</strong> ${order.customer_phone}</p>
                <p><strong>Time:</strong> ${new Date(order.created_at).toLocaleTimeString()}</p>
            </div>
            <div class="order-mgmt-items">
                <strong>Items:</strong>
                <ul>
                    ${order.items.map(item => `<li>${item.item_name} x${item.quantity}</li>`).join('')}
                </ul>
            </div>
            <div class="order-mgmt-total">
                <strong>$${parseFloat(order.total_amount).toFixed(2)}</strong>
            </div>
        </div>
    `).join('');
}

// Update order status via API
async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`${API_URL}/api/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (response.ok) {
            console.log(`Order #${orderId} status updated to ${newStatus}`);
        } else {
            const error = await response.json();
            alert('Error updating status: ' + error.error);
            loadOrderManagement();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating order status');
        loadOrderManagement();
    }
}

// Start polling for order status updates every 5 seconds
function startOrderPolling() {
    Object.values(statusPollingIntervals).forEach(interval => clearInterval(interval));
    statusPollingIntervals = {};
    
    statusPollingIntervals.management = setInterval(() => {
        if (document.getElementById('order-management-tab').classList.contains('active')) {
            loadOrderManagement();
        }
    }, 5000);
}

// Load menu items
async function loadAllMenuItems() {
    try {
        const response = await fetch(`${API_URL}/api/menu`);
        
        if (!response.ok) {
            throw new Error('Failed to load menu');
        }
        
        const menu = await response.json();
        displayMenuItems(menu);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('menuContainer').innerHTML = `<p class="error">Error loading menu: ${error.message}</p>`;
    }
}

function displayMenuItems(items) {
    const container = document.getElementById('menuContainer');
    
    if (items.length === 0) {
        container.innerHTML = '<p>No menu items.</p>';
        return;
    }
    
    container.innerHTML = items.map(item => `
        <div class="menu-card">
            <div class="menu-header">
                <h3>${item.name}</h3>
                <span class="menu-price">$${parseFloat(item.price).toFixed(2)}</span>
            </div>
            <p class="menu-description">${item.description || 'No description'}</p>
            <span class="menu-category">${item.category}</span>
            <div class="menu-actions">
                <button class="btn btn-small btn-primary" onclick="editMenuItem(${item.id})">Edit</button>
                <button class="btn btn-small btn-danger" onclick="deleteMenuItem(${item.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

function showAddMenuForm() {
    document.getElementById('menuModal').style.display = 'block';
}

function closeMenuModal() {
    document.getElementById('menuModal').style.display = 'none';
    document.getElementById('menuForm').reset();
}

document.getElementById('menuForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const itemData = {
        name: document.getElementById('item-name').value,
        description: document.getElementById('item-description').value,
        price: parseFloat(document.getElementById('item-price').value),
        category: document.getElementById('item-category').value
    };
    
    try {
        const response = await fetch(`${API_URL}/api/menu/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(itemData)
        });
        
        if (response.ok) {
            alert('Menu item added successfully!');
            closeMenuModal();
            loadAllMenuItems();
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error adding item: ' + error.message);
    }
});

function editMenuItem(itemId) {
    alert('Edit functionality coming soon!');
}

function deleteMenuItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        alert('Delete functionality coming soon!');
    }
}

// Load all admins
async function loadAllAdmins() {
    try {
        const response = await fetch(`${API_URL}/api/admin/all`);
        
        if (!response.ok) {
            throw new Error('Failed to load admins');
        }
        
        const admins = await response.json();
        displayAdmins(admins);
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('adminsContainer').innerHTML = `<p class="error">Error loading admins: ${error.message}</p>`;
    }
}

function displayAdmins(admins) {
    const container = document.getElementById('adminsContainer');
    
    if (admins.length === 0) {
        container.innerHTML = '<p>No admins.</p>';
        return;
    }
    
    container.innerHTML = admins.map(admin => `
        <div class="admin-card">
            <div class="admin-info">
                <h3>${admin.first_name} ${admin.last_name}</h3>
                <p>${admin.email}</p>
                <small>Created: ${new Date(admin.created_at).toLocaleDateString()}</small>
            </div>
            <div class="admin-actions">
                <button class="btn btn-small btn-danger" onclick="deleteAdmin(${admin.id})">Remove</button>
            </div>
        </div>
    `).join('');
}

function showAddAdminForm() {
    document.getElementById('adminModal').style.display = 'block';
}

function closeAdminModal() {
    document.getElementById('adminModal').style.display = 'none';
    document.getElementById('adminForm').reset();
}

document.getElementById('adminForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const adminData = {
        email: document.getElementById('admin-email').value,
        password: document.getElementById('admin-password').value,
        first_name: document.getElementById('admin-first').value,
        last_name: document.getElementById('admin-last').value
    };
    
    try {
        const response = await fetch(`${API_URL}/api/admin/signup`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(adminData)
        });
        
        if (response.ok) {
            alert('Admin created successfully!');
            closeAdminModal();
            loadAllAdmins();
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('Error creating admin: ' + error.message);
    }
});

function deleteAdmin(adminId) {
    if (confirm('Are you sure you want to remove this admin?')) {
        alert('Delete functionality coming soon!');
    }
}

// Close modals when clicking outside
window.addEventListener('click', (event) => {
    const menuModal = document.getElementById('menuModal');
    const adminModal = document.getElementById('adminModal');
    
    if (event.target === menuModal) {
        menuModal.style.display = 'none';
    }
    if (event.target === adminModal) {
        adminModal.style.display = 'none';
    }
});