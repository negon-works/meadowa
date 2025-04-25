document.addEventListener("DOMContentLoaded", function () {
    // Set item-total based on price * quantity + delivery
    document.querySelectorAll('.cart-item').forEach(cartItem => {
        updateItemPrice(cartItem);
    });

    updateCartTotal();

    document.querySelectorAll(".quantity-increase").forEach(button => {
        button.addEventListener("click", function () {
            let input = this.previousElementSibling;
            input.value = parseInt(input.value) + 1;
            updateItemPrice(this.closest(".cart-item"));
            updateCartTotal();
        });
    });

    document.querySelectorAll(".quantity-decrease").forEach(button => {
        button.addEventListener("click", function () {
            let input = this.nextElementSibling;
            if (parseInt(input.value) > 1) {
                input.value = parseInt(input.value) - 1;
                updateItemPrice(this.closest(".cart-item"));
                updateCartTotal();
            }
        });
    });

    document.querySelectorAll(".remove-item").forEach(button => {
        button.addEventListener("click", function () {
            const cartItem = this.closest(".cart-item");
            const variantId = this.getAttribute("data-variant");

            fetch("/remove-cart-item/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCSRFToken()
                },
                body: `variant_id=${variantId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    cartItem.remove();
                    updateCartTotal();
                } else {
                    alert("Failed to remove item: " + (data.error || "Unknown error"));
                }
            });
        });
    });

    document.querySelectorAll(".quantity-input").forEach(input => {
        input.addEventListener("input", function () {
            updateItemPrice(this.closest(".cart-item"));
            updateCartTotal();
        });
    });

    function updateItemPrice(cartItem) {
        let price = parseFloat(cartItem.getAttribute("data-price"));
        let delivery = parseFloat(cartItem.getAttribute("data-delivery")) || 0;
        let quantity = parseInt(cartItem.querySelector(".quantity-input").value);
        let totalPrice = price * quantity + delivery;
        cartItem.querySelector(".item-total").textContent = totalPrice.toFixed(2);
    }

    function updateCartTotal() {
        let subtotal = 0;
        let totalDelivery = 0;
        let grandTotal = 0;
    
        document.querySelectorAll(".cart-item").forEach(item => {
            let price = parseFloat(item.getAttribute("data-price"));
            let delivery = parseFloat(item.getAttribute("data-delivery")) || 0;
            let quantity = parseInt(item.querySelector(".quantity-input").value);
    
            subtotal += price * quantity;
            totalDelivery += delivery 
        });
    
        grandTotal = subtotal + totalDelivery;
    
        document.querySelector(".cart-total-price").textContent = subtotal.toFixed(2);
        document.querySelector(".cart-delivery-charge").textContent = totalDelivery.toFixed(2);
        document.querySelector(".cart-grand-total").textContent = grandTotal.toFixed(2);
    }
    
});

function getCSRFToken() {
    let name = "csrftoken";
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
