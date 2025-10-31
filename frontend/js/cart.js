// frontend/js/cart.js - Order management functionality

// Cart management system
const cart = {
  items: [],

  // Add item to cart
  addItem: function (item) {
    const existingItem = this.items.find((cartItem) => cartItem.id === item.id);

    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      this.items.push({ ...item });
    }

    this.updateDisplay();
  },

  // Remove item from cart
  removeItem: function (itemId) {
    this.items = this.items.filter((item) => item.id !== itemId);
    this.updateDisplay();
  },

  // Update item quantity
  updateQuantity: function (itemId, newQuantity) {
    if (newQuantity <= 0) {
      this.removeItem(itemId);
      return;
    }

    const item = this.items.find((cartItem) => cartItem.id === itemId);
    if (item) {
      item.quantity = newQuantity;
      this.updateDisplay();
    }
  },

  // Get total price
  getTotal: function () {
    return this.items.reduce(
      (total, item) => total + item.price * item.quantity,
      0
    );
  },

  // Get total item count
  getItemCount: function () {
    return this.items.reduce((count, item) => count + item.quantity, 0);
  },

  // Get all items
  getItems: function () {
    return this.items;
  },

  // Clear cart
  clear: function () {
    this.items = [];
    this.updateDisplay();
  },

  // Update the order display
  updateDisplay: function () {
    const orderItems = document.getElementById("orderItems");
    const orderTotal = document.getElementById("orderTotal");
    const orderCount = document.getElementById("orderCount");
    const proceedBtn = document.getElementById("proceedBtn");

    // Update counter in header
    orderCount.textContent = this.getItemCount();

    // Update total
    orderTotal.textContent = this.getTotal().toFixed(2);

    // Update items display
    if (this.items.length === 0) {
      orderItems.innerHTML = '<p class="empty-order">No items added yet</p>';
      proceedBtn.style.display = "none";
      document.getElementById("customerForm").style.display = "none";
    } else {
      orderItems.innerHTML = this.items
        .map(
          (item) => `
                <div class="order-item">
                    <div class="order-item-details">
                        <div class="order-item-name">${item.name}</div>
                        <div class="order-item-price">$${item.price.toFixed(
                          2
                        )} each</div>
                    </div>
                    <div class="quantity-controls">
                        <button class="qty-btn" onclick="cart.updateQuantity(${
                          item.id
                        }, ${item.quantity - 1})">-</button>
                        <span>${item.quantity}</span>
                        <button class="qty-btn" onclick="cart.updateQuantity(${
                          item.id
                        }, ${item.quantity + 1})">+</button>
                    </div>
                </div>
            `
        )
        .join("");

      proceedBtn.style.display = "block";
    }
  },
};

function displayMenu(items) {
  const menuDiv = document.getElementById("menuGrid");
  menuDiv.innerHTML = "";

  items.forEach((item) => {
    // Store the item in a data attribute or use a closure
    const itemDiv = document.createElement("div");
    itemDiv.className = "menu-item";
    itemDiv.innerHTML = `
      <h3>${item.name} - $${item.price}</h3>
      <p>${item.description}</p>
      <button>Add to Cart</button>
    `;
    itemDiv.querySelector("button").addEventListener("click", () => {
      addToCart(item); // pass the object directly
    });
    menuDiv.appendChild(itemDiv);
  });
}

function addToCart(item) {
  const existing = cart.items.find((cartItem) => cartItem.id === item.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    cart.items.push({ ...item, quantity: 1 });
  }
  cart.updateDisplay();
}

function removeFromCart(itemId) {
  cart.items = cart.items.filter((item) => item.id !== itemId);
  cart.updateCartDisplay();
}

function updateCartDisplay() {
  const cartDiv = document.getElementById("cart");
  cartDiv.innerHTML = "";
  let total = 0;
  cart.items.forEach((item) => {
    total += item.price * item.quantity;
    cartDiv.innerHTML += `
            <p>${item.name} x ${item.quantity} - $${(
      item.price * item.quantity
    ).toFixed(2)} 
            <button onclick="removeFromCart(${item.id})">Remove</button></p>
        `;
  });
  cartDiv.innerHTML += `<p>Total: $${total.toFixed(2)}</p>`;
}

function goToCheckout() {
  if (cart.items.length == 0) {
    alert("Your cart is empty! Add items to your cart before checking out!");
    return;
  }

  // Generate a random order ID for demo
  const orderId = "ORD-" + Date.now();
  localStorage.setItem("orderId", orderId);
  localStorage.setItem("cartItems", JSON.stringify(cart.items));

  //Total of all the items in cart
  const total = cart.items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  localStorage.setItem("orderTotal", total.toFixed(2));

  //redirects to payment.html
  window.location.href = "payment.html";
}

fetch("http://localhost:5000/api/menu")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok " + response.statusText);
    }
    return response.json();
  })
  .then((data) => displayMenu(data))
  .catch((error) => {
    console.error("Fetch error:", error);
    const menuDiv = document.getElementById("menu");
    menuDiv.innerHTML = "<p>Failed to load menu. Check console for errors.</p>";
  });
