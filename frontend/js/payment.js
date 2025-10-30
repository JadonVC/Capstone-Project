async function submitPayment() {
  const orderId = document.getElementById("orderId").value;
  const cardNumber = document.getElementById("cardNumber").value;
  const amount = document.getElementById("amount").value;

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
      document.getElementById(
        "result"
      ).innerHTML = `<p style="color:green;">${result.message}<br>
        Transaction ID: ${result.transaction_id}<br>
        Amount: $${result.amount}</p>`;
    } else {
      document.getElementById(
        "result"
      ).innerHTML = `<p style="color:red;">${result.message}</p>`;
    }
  } catch (err) {
    console.error("Payment error:", err);
    document.getElementById(
      "result"
    ).innerHTML = `<p style="color:red;">Error connecting to payment system</p>`;
  }
}
