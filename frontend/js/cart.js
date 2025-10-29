let cart = [];

function displayMenu(items) {
  const menuDiv = document.getElementById("menuGrid");
  menuDiv.innerHTML = "";
  items.forEach((item) => {
    menuDiv.innerHTML += `
            <div class="menu-item">
                <h3>${item.name} - $${item.price}</h3>
                <p>${item.description}</p>
                <button onclick='addToCart(${JSON.stringify(
                  item
                )})'>Add to Cart</button>
            </div>
        `;
  });
}

function addToCart(item) {
  const existing = cart.find((cartItem) => cartItem.id === item.id);
  if (existing) {
    existing.quantity += 1;
  } else {
    item.quantity = 1;
    cart.push(item);
  }
  updateCartDisplay();
}

function removeFromCart(itemId) {
  cart = cart.filter((item) => item.id !== itemId);
  updateCartDisplay();
}

function updateCartDisplay() {
  const cartDiv = document.getElementById("cart");
  cartDiv.innerHTML = "";
  let total = 0;
  cart.forEach((item) => {
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
  if (cart.length == 0) {
    alert("Your cart is empty! Add items to your cart before checking out!");
    return;
  }
  localStorage.setItem("cart", JSON.stringify(cart));

  //Total of all the items in cart
  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

  //Saves order in local storage
  localStorage.setItem("orderId", orderId);
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
