from flask import request, jsonify
from services.payment_service import process_payment

def register_payment_routes(app):

    @app.route("/payment", methods=["POST"])
    def payment():
        data = request.json
        order_id = data.get("order_id")
        card_number = data.get("card_number")
        amount = data.get("amount")

        if not order_id or not card_number or not amount:
            return jsonify({"error": "Missing required fields"}), 400

        result = process_payment(order_id, card_number, amount)
        return jsonify(result)

