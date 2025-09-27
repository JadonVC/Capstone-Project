// Initial frontend development

// API configuration
const API_BASE_URL = 'http://localhost:5000/api';

// API functions for communicating with Flask backend
const API = {
    
    // Get all menu items
    getMenu: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/menu`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('Error fetching menu:', error);
            throw error;
        }
    },
    
    // Get menu items by category
    getMenuByCategory: async (category) => {
        try {
            const response = await fetch(`${API_BASE_URL}/menu/${category}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error(`Error fetching menu for category ${category}:`, error);
            throw error;
        }
    }
    
    // Additional API functions can be added here as needed
    // Example: addMenuItem, updateMenuItem, deleteMenuItem for admin features
};