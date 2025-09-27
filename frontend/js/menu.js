// frontend/js/menu.js - Initial frontend development

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
                <div class="item-price">$${parseFloat(item.price).toFixed(2)}</div>
                <div class="item-category">${item.category}</div>
            </div>
        </div>
    `).join('');
}