// frontend/js/api.js - API communication helper

const API = {
    BASE_URL: 'http://localhost:5000/api',
    
    async getMenu() {
        try {
            const response = await fetch(`${this.BASE_URL}/menu`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async placeOrder(orderData) {
        try {
            const response = await fetch(`${this.BASE_URL}/orders`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(orderData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async getOrder(orderId) {
        try {
            const response = await fetch(`${this.BASE_URL}/orders/${orderId}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }
};