document.addEventListener("DOMContentLoaded", function () {
    // Category Dropdown
    const categoryBtn = document.getElementById("category-btn");
    const dropdownMenu = document.getElementById("dropdown-menu");

    categoryBtn.addEventListener("click", function (event) {
        event.preventDefault();
        dropdownMenu.classList.toggle("active");
    });

    document.addEventListener("click", function (event) {
        if (!categoryBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove("active");
        }
    });

    // Profile Dropdown
    const profileBtn = document.getElementById("profile-btn");
    const profileMenu = document.getElementById("profile-menu");

    if (profileBtn) {
        profileBtn.addEventListener("click", function (event) {
            event.preventDefault();
            profileMenu.classList.toggle("active");
        });

        document.addEventListener("click", function (event) {
            if (!profileBtn.contains(event.target) && !profileMenu.contains(event.target)) {
                profileMenu.classList.remove("active");
            }
        });
    }

    // Simulate login system (For Testing)
    const loginBtn = document.getElementById("login-btn");
    const profileSection = document.getElementById("profile-section");
    
    loginBtn.addEventListener("click", function () {
        loginBtn.style.display = "none"; // Hide login button
        profileSection.style.display = "block"; // Show profile section
    });

    document.getElementById("logout-btn").addEventListener("click", function () {
        profileSection.style.display = "none"; // Hide profile
        loginBtn.style.display = "block"; // Show login button
    });
});

document.addEventListener("DOMContentLoaded", function () {
        updateCartTotal(); // Initial total price update

        // Initialize item-total with data-price
        document.querySelectorAll('.cart-item').forEach(cartItem => {
            let dataPrice = cartItem.getAttribute('data-price');
            cartItem.querySelector('.item-total').textContent = dataPrice;
        });

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
                this.closest(".cart-item").remove();
                updateCartTotal();
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
            let quantity = parseInt(cartItem.querySelector(".quantity-input").value);
            cartItem.querySelector(".item-total").textContent = (price * quantity).toFixed(2);
        }


        function updateCartTotal() {
            let total = 0;
            document.querySelectorAll(".cart-item").forEach(item => {
                total += parseFloat(item.querySelector(".item-total").textContent);
            });
            document.querySelector(".cart-total-price").textContent = total.toFixed(2);
        }
        updateCartTotal();
    });


document.addEventListener("DOMContentLoaded", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "block";
});
window.addEventListener("load", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "none";
});