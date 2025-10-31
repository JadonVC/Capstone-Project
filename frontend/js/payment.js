async function submitPayment() {
  const orderId = document.getElementById("orderId").value;
  const cardNumber = document.getElementById("cardNumber").value;
  const amount = document.getElementById("amount").value;
  const expiry = document.getElementById("expiry").value;
  const cvc = document.getElementById("cvc").value;

  const payload = {
    order_id: orderId,
    card_number: cardNumber,
    amount: parseFloat(amount),
  };

  try {
    const response = await fetch("http://localhost:5000/payment", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (result.status === "success") {
      window.location.href = "success_page.html";
    } else {
      window.location.href = "failure_page.html";
    }
  } catch (err) {
    console.error("Payment error:", err);
    window.location.href = "failure_page.html";
  }
}

const API_BASE = "http://localhost:5000/api";
const response = await fetch("http://localhost:5000/api/rewards");

// Load customer's points and available rewards
async function loadLoyaltyOptions() {
  try {
    // Get customer's points balance
    const balanceResponse = await fetch(`${API_BASE}/loyalty/balance`, {
      credentials: "include",
    });
    const balance = await balanceResponse.json();

    // Display points
    document.getElementById("loyaltyPoints").innerHTML = `
            <p>You have <strong>${balance.total_points}</strong> points available</p>
            <a href="rewards.html" style="color: #667eea;">View all rewards →</a>
        `;

    // Get redeemable rewards
    const rewardsResponse = await fetch(`${API_BASE}/loyalty/rewards`, {
      credentials: "include",
    });
    const rewards = await rewardsResponse.json();

    // Show only redeemable rewards
    const redeemable = rewards.filter((r) => r.can_redeem === 1);

    if (redeemable.length > 0) {
      displayRedeemableRewards(redeemable);
    } else {
      document.getElementById("availableRewards").innerHTML =
        '<p style="color: #666;">No rewards available yet. Keep ordering to earn more points!</p>';
    }
  } catch (error) {
    console.error("Error loading loyalty options:", error);
  }
}

// Display rewards customer can redeem
function displayRedeemableRewards(rewards) {
  const container = document.getElementById("availableRewards");

  container.innerHTML = `
        <h4>Available to Redeem:</h4>
        <div class="rewards-list">
            ${rewards
              .map((reward) => {
                const discountText =
                  reward.discount_type === "percentage"
                    ? `${reward.discount_value}% OFF`
                    : `$${parseFloat(reward.discount_value).toFixed(2)} OFF`;

                return `
                    <div class="reward-option">
                        <div class="reward-info">
                            <strong>${reward.name}</strong>
                            <span class="discount-badge">${discountText}</span>
                            <span class="points-cost">${reward.points_required} points</span>
                        </div>
                        <button class="apply-btn" onclick="applyReward(${reward.id})">
                            Apply
                        </button>
                    </div>
                `;
              })
              .join("")}
        </div>
    `;
}

// Apply reward to current order
async function applyReward(rewardId) {
  try {
    const response = await fetch(`${API_BASE}/loyalty/redeem`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ reward_id: rewardId }),
    });

    const result = await response.json();

    if (response.ok) {
      // Store discount info
      window.appliedDiscount = result.discount;

      // Update order total with discount
      applyDiscountToTotal(result.discount);

      // Show applied discount
      showAppliedDiscount(result.discount);

      // Hide rewards list
      document.getElementById("availableRewards").style.display = "none";
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    console.error("Error applying reward:", error);
    alert("Failed to apply reward. Please try again.");
  }
}

// Apply discount to order total
function applyDiscountToTotal(discount) {
  // Get current subtotal (you'll need to adjust this based on your code)
  let subtotal = parseFloat(
    document.getElementById("subtotal").textContent.replace("$", "")
  );

  let discountAmount = 0;
  if (discount.discount_type === "percentage") {
    discountAmount = subtotal * (discount.discount_value / 100);
  } else {
    discountAmount = discount.discount_value;
  }

  // Update display
  const discountRow =
    document.getElementById("discountRow") || createDiscountRow();
  discountRow.querySelector(
    ".discount-amount"
  ).textContent = `-$${discountAmount.toFixed(2)}`;
  discountRow.style.display = "flex";

  // Recalculate total
  updateTotal();
}

// Show applied discount message
function showAppliedDiscount(discount) {
  const section = document.getElementById("appliedDiscount");
  const details = document.getElementById("discountDetails");

  const discountText =
    discount.discount_type === "percentage"
      ? `${discount.discount_value}% discount`
      : `$${discount.discount_value} discount`;

  details.textContent = `${discount.reward_name} - ${discountText} applied to your order`;
  section.style.display = "block";
}

// Remove applied discount
function removeDiscount() {
  window.appliedDiscount = null;
  document.getElementById("appliedDiscount").style.display = "none";
  document.getElementById("availableRewards").style.display = "block";

  // Remove discount from total
  const discountRow = document.getElementById("discountRow");
  if (discountRow) {
    discountRow.style.display = "none";
  }

  updateTotal();
}

// Create discount row in order summary
function createDiscountRow() {
  const orderSummary = document.querySelector(".order-summary");
  const discountRow = document.createElement("div");
  discountRow.id = "discountRow";
  discountRow.className = "summary-row";
  discountRow.style.display = "none";
  discountRow.innerHTML = `
        <span>Discount:</span>
        <span class="discount-amount" style="color: #28a745;">-$0.00</span>
    `;

  // Insert before total row
  const totalRow = document.querySelector(".total-row");
  orderSummary.insertBefore(discountRow, totalRow);

  return discountRow;
}

// Complete order (call this after payment is confirmed)
async function completeOrder(orderId, totalAmount) {
  try {
    const response = await fetch(`${API_BASE}/orders/complete`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        order_id: orderId,
        total_amount: totalAmount,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      // Show success message with points earned
      showOrderSuccess(result.points_earned);

      // Redirect to order confirmation or orders page
      setTimeout(() => {
        window.location.href = `my-orders.html?order=${orderId}`;
      }, 3000);
    }
  } catch (error) {
    console.error("Error completing order:", error);
  }
}

// Show success message
function showOrderSuccess(pointsEarned) {
  alert(
    `Order placed successfully!\n\nYou earned ${pointsEarned} loyalty points! 🎉`
  );
}

// Initialize loyalty section on checkout page load
document.addEventListener("DOMContentLoaded", async function () {
  // Check if we're on checkout page
  if (window.location.pathname.includes("checkout")) {
    await loadLoyaltyOptions();
  }
});

// After payment is successful
async function finalizeOrder(orderId, totalAmount) {
  const response = await fetch("http://localhost:5000/api/orders/complete", {
    method: "POST",
    credentials: "include", // Important for sessions
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      order_id: orderId,
      total_amount: totalAmount,
    }),
  });

  const result = await response.json();
  console.log(`Earned ${result.points_earned} points!`);
}
