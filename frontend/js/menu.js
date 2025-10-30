// frontend/js/menu.js - Updated with ordering functionality

let menuData = [];
let currentFilter = 'all';

// Load menu data when page loads
document.addEventListener('DOMContentLoaded', loadMenu);

async function loadMenu() {
    const loading = document.getElementById('loading');
    const error = document.getElementById('error');
    
    try {
        loading.style.display = 'block';
        error.style.display = 'none';
        
        // Use API to fetch menu data
        menuData = await API.getMenu();
        
        if (menuData && menuData.length > 0) {
            createCategoryFilters();
            displayMenu(menuData);
            loading.style.display = 'none';
        } else {
            throw new Error('No menu items found');
        }
        
    } catch (err) {
        loading.style.display = 'none';
        error.style.display = 'block';
        error.textContent = `Failed to load menu: ${err.message}. Make sure your Flask backend is running on http://localhost:5000`;
        console.error('Error loading menu:', err);
    }
}

function createCategoryFilters() {
    const filtersContainer = document.getElementById('categoryFilters');
    
    // Get unique categories from menu data
    const categories = [...new Set(menuData.map(item => item.category))];
    
    // Clear existing filters except "All Items"
    filtersContainer.innerHTML = '<button class="filter-btn active" onclick="filterMenu(\'all\')">All Items</button>';
    
    // Add category buttons
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'filter-btn';
        button.textContent = category;
        button.onclick = () => filterMenu(category);
        filtersContainer.appendChild(button);
    });
}

function filterMenu(category) {
    currentFilter = category;
    
    // Update active button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Filter and display items
    const filteredItems = category === 'all' 
        ? menuData 
        : menuData.filter(item => item.category === category);
    
    displayMenu(filteredItems);
}

function displayMenu(items) {
    const grid = document.getElementById('menuGrid');
    
    if (items.length === 0) {
        grid.innerHTML = '<p style="text-align: center; grid-column: 1/-1;">No items found in this category.</p>';
        return;
    }
    
    grid.innerHTML = items.map(item => `
        <div class="menu-item">
            <div class="item-name">${item.name}</div>
            <div class="item-description">${item.description || 'Delicious menu item'}</div>
            <div class="item-footer">
                <div class="item-price">${parseFloat(item.price).toFixed(2)}</div>
                <div class="item-category">${item.category}</div>
            </div>
            <div class="item-controls">
                <div class="quantity-selector">
                    <label>Qty:</label>
                    <input type="number" min="1" max="10" value="1" class="qty-input" id="qty-${item.id}">
                </div>
                <button class="add-to-order-btn" onclick="addToOrder(${item.id}, '${item.name}', ${item.price})">
                    Add to Order
                </button>
            </div>
        </div>
    `).join('');
}

function addToOrder(itemId, itemName, itemPrice) {
    const qtyInput = document.getElementById(`qty-${itemId}`);
    const quantity = parseInt(qtyInput.value) || 1;
    
    // Add to cart using cart.js functions
    cart.addItem({
        id: itemId,
        name: itemName,
        price: itemPrice,
        quantity: quantity
    });
    
    // Reset quantity to 1
    qtyInput.value = 1;
    
    // Show feedback
    const button = event.target;
    const originalText = button.textContent;
    button.textContent = 'Added!';
    button.style.background = '#48bb78';
    
    setTimeout(() => {
        button.textContent = originalText;
        button.style.background = '#667eea';
    }, 1000);
}

function toggleOrderSummary() {
    const orderSection = document.getElementById('orderSection');
    const toggleBtn = document.getElementById('orderToggle');
    
    if (orderSection.style.display === 'none') {
        orderSection.style.display = 'block';
        toggleBtn.textContent = `Hide Order (${cart.getItemCount()} items)`;
    } else {
        orderSection.style.display = 'none';
        toggleBtn.textContent = `View Order (${cart.getItemCount()} items)`;
    }
}

function showCustomerForm() {
    document.getElementById('customerForm').style.display = 'block';
    document.getElementById('proceedBtn').style.display = 'none';
}

async function placeOrder() {
    const name = document.getElementById('customerName').value;
    const phone = document.getElementById('customerPhone').value;
    const address = document.getElementById('customerAddress').value;
    
    if (!name || !phone) {
        alert('Please fill in your name and phone number.');
        return;
    }
    
    const orderData = {
        customer: {
            name: name,
            phone: phone,
            address: address
        },
        items: cart.getItems(),
        total: cart.getTotal(),
        timestamp: new Date().toISOString()
    };
    
    try {
    const response = await API.placeOrder(orderData);
    
    if (response.success) {
        const orderId = response.order_id;
        alert(`Thank you ${name}! Your order #${orderId} for $${cart.getTotal().toFixed(2)} has been placed. We'll contact you at ${phone} with updates.`);
        
        cart.clear();
        document.getElementById('customerForm').style.display = 'none';
        document.getElementById('proceedBtn').style.display = 'none';
    } else {
        alert('Error placing order: ' + response.error);
    }
    } catch (error) {
    alert('Error placing order: ' + error.message);
    console.error('Order error:', error);
    }
}