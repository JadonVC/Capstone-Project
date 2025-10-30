// frontend/js/orders.js - Order lookup and receipt display

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('orderIdInput').addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            lookupOrder();
        }
    });
});

async function lookupOrder() {
    const orderId = document.getElementById('orderIdInput').value.trim();
    const errorMessage = document.getElementById('errorMessage');
    const receiptSection = document.getElementById('receiptSection');
    
    errorMessage.style.display = 'none';
    
    if (!orderId) {
        errorMessage.textContent = 'Please enter an Order ID';
        errorMessage.style.display = 'block';
        return;
    }
    
    try {
        receiptSection.innerHTML = '<div class="loading">Loading order...</div>';
        receiptSection.style.display = 'block';
        
        const order = await API.getOrder(orderId);
        
        if (order && order.id) {
            displayReceipt(order);
        } else {
            throw new Error('Order not found');
        }
        
    } catch (error) {
        receiptSection.style.display = 'none';
        errorMessage.textContent = 'Order not found. Please check your Order ID and try again.';
        errorMessage.style.display = 'block';
        console.error('Error:', error);
    }
}

function displayReceipt(order) {
    const receiptSection = document.getElementById('receiptSection');
    
    if (!receiptSection) {
        console.error('receiptSection element not found');
        return;
    }
    
    if (!order || !order.id) {
        receiptSection.innerHTML = '<p>Invalid order data</p>';
        return;
    }
    
    const orderDate = new Date(order.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    const itemsHTML = order.items.map(item => `
        <div class="receipt-item">
            <div class="item-details">
                <div class="item-name">${item.item_name}</div>
                <div class="item-qty">Qty: ${item.quantity} @ $${parseFloat(item.item_price).toFixed(2)} each</div>
            </div>
            <div class="item-price">$${parseFloat(item.subtotal).toFixed(2)}</div>
        </div>
    `).join('');
    
    receiptSection.innerHTML = `
        <div class="receipt-header">
            <h2>Order Receipt</h2>
            <div class="order-id">Order #${order.id}</div>
        </div>
        
        <div class="receipt-info">
            <h4>Order Details</h4>
            <p><strong>Order Date:</strong> ${orderDate}</p>
        </div>
        
        <div class="receipt-info">
            <h4>Customer Information</h4>
            <p><strong>Name:</strong> ${order.customer_name}</p>
            <p><strong>Phone:</strong> ${order.customer_phone}</p>
            ${order.customer_address ? `<p><strong>Address:</strong> ${order.customer_address}</p>` : ''}
        </div>
        
        <div class="receipt-items">
            <h4 style="margin-top: 0;">Items Ordered</h4>
            ${itemsHTML}
        </div>
        
        <div class="receipt-total">
            <span>Total:</span>
            <span>$${parseFloat(order.total_amount).toFixed(2)}</span>
        </div>
        
        <div class="receipt-actions">
            <button class="back-btn" onclick="goBackToMenu()">Back to Menu</button>
            <button class="print-btn" onclick="window.print()">Print Receipt</button>
        </div>
    `;
}

function goBackToMenu() {
    window.location.href = 'index.html';
}