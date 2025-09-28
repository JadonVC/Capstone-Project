let cart = [];

function displayMenu(items) {
    const menuDiv = document.getElementById('menu');
    menuDiv.innerHTML = '';
    items.forEach(item => {
        menuDiv.innerHTML += `
            <div class="menu-item">
                <h3>${item.name} - $${item.price}</h3>
                <p>${item.description}</p>
                <button onclick='addToCart(${JSON.stringify(item)})'>Add to Cart</button>
            </div>
        `;
    });
}

function addToCart(item) {
    const existing = cart.find(cartItem => cartItem.id === item.id);
    if (existing) {
        existing.quantity += 1;
    } else {
        item.quantity = 1;
        cart.push(item);
    }
    updateCartDisplay();
}

function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    updateCartDisplay();
}

function updateCartDisplay() {
    const cartDiv = document.getElementById('cart');
    cartDiv.innerHTML = '';
    let total = 0;
    cart.forEach(item => {
        total += item.price * item.quantity;
        cartDiv.innerHTML += `
            <p>${item.name} x ${item.quantity} - $${(item.price*item.quantity).toFixed(2)} 
            <button onclick="removeFromCart(${item.id})">Remove</button></p>
        `;
    });
    cartDiv.innerHTML += `<p>Total: $${total.toFixed(2)}</p>`;
}

fetch("http://localhost:5000/api/menu")
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
  })
  .then(data => displayMenu(data))
  .catch(error => {
      console.error('Fetch error:', error);
      const menuDiv = document.getElementById('menu');
      menuDiv.innerHTML = '<p>Failed to load menu. Check console for errors.</p>';
  });
