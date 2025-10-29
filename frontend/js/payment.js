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
      window.location.href = "success.html";
    } else {
      window.location.href = "failure.html";
    }
  } catch (err) {
    console.error("Payment error:", err);
    window.location.href = "failure.html";
  }
}
