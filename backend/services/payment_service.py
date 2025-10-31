from models.payment_model import insert_payment
import uuid

def process_payment(order_id, card_number, amount):
    """
    Fake payment to ensure it works
    - If card starts with an 8 it's a success
    - Otherwise it should failed
    """

    if card_number and card_number.startswith("4"):
        status = "success"
        message = "Payment Received"
    else:
        status = "failed"
        message = "Payment Failed, Please Try Again"

    # Insert payment record into MySQL
    transaction_id = insert_payment(order_id, status, amount)

    return {
        "status": status,
        "message": message,
        "transaction_id": transaction_id,
        "order_id": order_id,
        "amount": amount
    }

#