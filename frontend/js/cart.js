// frontend/js/cart.js - Order management functionality

// Cart management system
const cart = {
    items: [],
    
    // Add item to cart
    addItem: function(item) {
        const existingItem = this.items.find(cartItem => cartItem.id === item.id);
        
        if (existingItem) {
            existingItem.quantity += item.quantity;
        } else {
            this.items.push({...item});
        }
        
        this.updateDisplay();
    },
    
    // Remove item from cart
    removeItem: function(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
        this.updateDisplay();
    },
    
    // Update item quantity
    updateQuantity: function(itemId, newQuantity) {
        if (newQuantity <= 0) {
            this.removeItem(itemId);
            return;
        }
        
        const item = this.items.find(cartItem => cartItem.id === itemId);
        if (item) {
            item.quantity = newQuantity;
            this.updateDisplay();
        }
    },
    
    // Get total price
    getTotal: function() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    
    // Get total item count
    getItemCount: function() {
        return this.items.reduce((count, item) => count + item.quantity, 0);
    },
    
    // Get all items
    getItems: function() {
        return this.items;
    },
    
    // Clear cart
    clear: function() {
        this.items = [];
        this.updateDisplay();
    },
    
    // Update the order display
    updateDisplay: function() {
        const orderItems = document.getElementById('orderItems');
        const orderTotal = document.getElementById('orderTotal');
        const orderCount = document.getElementById('orderCount');
        const proceedBtn = document.getElementById('proceedBtn');
        
        // Update counter in header
        orderCount.textContent = this.getItemCount();
        
        // Update total
        orderTotal.textContent = this.getTotal().toFixed(2);
        
        // Update items display
        if (this.items.length === 0) {
            orderItems.innerHTML = '<p class="empty-order">No items added yet</p>';
            proceedBtn.style.display = 'none';
            document.getElementById('customerForm').style.display = 'none';
        } else {
            orderItems.innerHTML = this.items.map(item => `
                <div class="order-item">
                    <div class="order-item-details">
                        <div class="order-item-name">${item.name}</div>
                        <div class="order-item-price">$${item.price.toFixed(2)} each</div>
                    </div>
                    <div class="quantity-controls">
                        <button class="qty-btn" onclick="cart.updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="cart.updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                    </div>
                </div>
            `).join('');
            
            proceedBtn.style.display = 'block';
        }
    }
};