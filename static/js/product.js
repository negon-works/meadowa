

// Price, Stock & Delivery Logic
document.addEventListener("DOMContentLoaded", function () {
    const sizeSelector = document.getElementById("choose-size");
    const quantityInput = document.getElementById("quantity");
    const tpriceElement = document.getElementById("total-price");
    const priceElement = document.getElementById("price");
    const deliveryChargeElement = document.getElementById("delivery-charge");
    const priceContainer = document.querySelector(".total-price");
    const increaseBtn = document.querySelector(".increase-btn");
    const decreaseBtn = document.querySelector(".decrease-btn");
    const stockInfo = document.getElementById("stock-info");

    // ✅ Initialize delivery charge
    let deliveryCharge = priceContainer ? parseInt(priceContainer.getAttribute("data-delivery")) || 0 : 0;

    // 📝 Update price, stock, and delivery information
    function updatePrice() {
        let selectedOption = sizeSelector.options[sizeSelector.selectedIndex];
        let price = parseInt(selectedOption.getAttribute("data-price")) || 0;
        let stock = parseInt(selectedOption.getAttribute("data-stock")) || 0;
        let delivery = parseInt(selectedOption.getAttribute("data-delivery")) || 0;

        priceElement.innerText = `₹${price}`;
        deliveryCharge = delivery;

        // 🔥 Stock info display
        if (stock === 0) {
            stockInfo.innerHTML = `<span style="color: red; font-weight: bold;">Out of Stock</span>`;
            quantityInput.disabled = true;
            increaseBtn.disabled = true;
            decreaseBtn.disabled = true;
            
            // ✅ Change delivery text color to red if out of stock
            deliveryChargeElement.innerHTML = delivery === 0
                ? `<span style="color: red; font-weight: bold; text-decoration: line-through;">Free Delivery</span>`
                : `<span style="color: red; font-weight: bold;">(Out of Stock) ₹${delivery}</span>`;
        } else {
            stockInfo.innerHTML = `<span style="color: #666666; font-weight: normal;">In Stock:</span>
                <span style="color: green; font-weight: bold;"> ${stock}</span>`;
            quantityInput.disabled = false;
            increaseBtn.disabled = false;
            decreaseBtn.disabled = false;

            // ✅ Show "Free Delivery" if delivery is 0
            deliveryChargeElement.innerHTML = delivery === 0
                ? `<span style="color: green; font-weight: bold;">Free Delivery</span>`
                : `<span style="color: #666666; font-weight: bold;">₹${delivery}</span> `;
        }

        updateTPrice();
    }

    // 📝 Update total price based on quantity and delivery charge
    function updateTPrice() {
        let selectedOption = sizeSelector.options[sizeSelector.selectedIndex];
        let price = parseInt(selectedOption.getAttribute("data-price")) || 0;
        let quantity = parseInt(quantityInput.value) || 1;
        let totalPrice = (price * quantity) + deliveryCharge;

        tpriceElement.innerText = `₹${totalPrice}`;
    }

    // 🔥 Mark out-of-stock options dynamically
    function markOutOfStockOptions() {
        Array.from(sizeSelector.options).forEach(option => {
            let stock = parseInt(option.getAttribute("data-stock")) || 0;
            if (stock === 0) {
                option.classList.add("out-of-stock");
                if (!option.textContent.includes("(Out of Stock)")) {
                    option.textContent += " (Out of Stock)";
                }
            } else {
                option.classList.remove("out-of-stock");
                option.textContent = option.textContent.replace(" (Out of Stock)", "");
            }
        });
    }

    // ✅ Increase quantity
    increaseBtn.addEventListener("click", function () {
        let stock = parseInt(sizeSelector.options[sizeSelector.selectedIndex].getAttribute("data-stock")) || 0;
        if (parseInt(quantityInput.value) < stock) {
            quantityInput.value = parseInt(quantityInput.value) + 1;
            updateTPrice();
        }
    });

    // ✅ Decrease quantity
    decreaseBtn.addEventListener("click", function () {
        if (quantityInput.value > 1) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
            updateTPrice();
        }
    });

    // 🎯 Event Listeners
    sizeSelector.addEventListener("change", updatePrice);
    quantityInput.addEventListener("input", updateTPrice);

    // ⚡️ Call functions on page load
    updatePrice(); // Ensures initial values are populated
    markOutOfStockOptions();
});

// Product Image Slider
document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".image-slider");
    const mainImage = document.querySelector(".product-image img");
    const additionalImages = document.querySelectorAll(".image-slider img");
    const leftBtn = document.getElementById("prev-btn");
    const rightBtn = document.getElementById("next-btn");

    const scrollAmount = container.children[0].offsetWidth + 10; // Image width + gap

    leftBtn.addEventListener("click", function () {
        container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        checkOverflow();
    });

    rightBtn.addEventListener("click", function () {
        container.scrollBy({ left: scrollAmount, behavior: "smooth" });
        checkOverflow();
    });

    additionalImages.forEach((image) => {
        image.addEventListener("click", function () {
            // Swap the src attribute of the main image and the clicked image
            let tempSrc = mainImage.src;
            mainImage.src = image.src;
            image.src = tempSrc;
        });
    });

    container.addEventListener("scroll", checkOverflow);
    window.addEventListener("resize", checkOverflow);

    // Initial check
    checkOverflow();
});

function checkOverflow() {
    const container = document.querySelector(".image-slider");
    const leftBtn = document.getElementById("prev-btn");
    const rightBtn = document.getElementById("next-btn");

    // Check if there's overflow in the container
    const isOverflowing = container.scrollWidth > container.clientWidth;

    // Enable/disable buttons based on overflow
    if (isOverflowing) {
        const isAtStart = container.scrollLeft === 0;
        const isAtEnd = container.scrollLeft + container.clientWidth >= container.scrollWidth;

        leftBtn.classList.toggle("show", !isAtStart);
        rightBtn.classList.toggle("show", !isAtEnd);
    } else {
        leftBtn.classList.remove("show");
        rightBtn.classList.remove("show");
    }
}


document.getElementById('add-to-cart-btn').addEventListener('click', function() {
        const productId = "{{ product.id }}";
        const variantId = document.getElementById('choose-size').value;
        const quantity = document.getElementById('quantity').value;
        const subscription = document.getElementById('subscription').value;
    
        fetch("{% url 'web:add_to_cart' 0 %}".replace("0", productId), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({
                variant_id: variantId,
                quantity: quantity,
                subscription: subscription
            })
        })
        .then(response => {
            if (response.ok) {
                // SweetAlert notification for adding to cart
                Swal.fire({
                    icon: 'success',
                    title: 'Added to Cart!',
                    text: 'Your product has been added to the cart 🎉',
                    showConfirmButton: false,
                    timer: 1500 // Show for 1.5 seconds
                });
            } else {
                // SweetAlert notification for error
                Swal.fire({
                    icon: 'error',
                    title: 'Oops!',
                    text: 'Something went wrong 😢',
                    showConfirmButton: true
                });
            }
        });
    });


<script>
    document.getElementById('add-to-cart-btn').addEventListener('click', function() {
        const productId = "{{ product.id }}";
        const variantId = document.getElementById('choose-size').value;
        const quantity = document.getElementById('quantity').value;
        const subscription = document.getElementById('subscription').value;
    
        fetch("{% url 'web:add_to_cart' 0 %}".replace("0", productId), {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
            body: JSON.stringify({
                variant_id: variantId,
                quantity: quantity,
                subscription: subscription
            })
        })
        .then(response => {
            if (response.ok) {
                // SweetAlert notification for adding to cart
                Swal.fire({
                    icon: 'success',
                    title: 'Added to Cart!',
                    text: 'Your product has been added to the cart 🎉',
                    showConfirmButton: false,
                    timer: 1500 // Show for 1.5 seconds
                });
            } else {
                // SweetAlert notification for error
                Swal.fire({
                    icon: 'error',
                    title: 'Oops!',
                    text: 'Something went wrong 😢',
                    showConfirmButton: true
                });
            }
        });
    });
</script>
// productjs-future-update
// "I want to dynamically update product types and prices for an e-commerce site using a backend system. How can I set it up so sellers can add different types like 'ml', 'grams', and 'packets' from a seller page, and have these updates reflected in the product page template? Could you provide an example of the backend setup with a database, an API endpoint, and the frontend JavaScript to fetch and display this dynamic data?"

