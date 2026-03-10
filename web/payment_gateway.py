# web/payment_gateway.py
def process_payment(payment_method, order_amount, order_id):
    if payment_method == "razorpay":
        # Integrate Razorpay payment processing logic here
        # Example: return razorpay_response
        return "Payment processed via Razorpay"
    elif payment_method == "cod":
        # Handle Cash on Delivery logic
        return "Cash on Delivery selected"
    else:
        return "Invalid payment method"
