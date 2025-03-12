
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
    const sizeSelector = document.getElementById("choose-size");
    const quantityInput = document.getElementById("quantity");
    const tpriceElement = document.getElementById("total-price");
    const priceElement = document.getElementById("price");
    const ratingStars = document.querySelectorAll(".star-rating span");
    const overallRating = document.getElementById("overall-rating");
    const overallStars = document.getElementById("overall-stars");
    const increaseBtn = document.querySelector(".increase-btn");
    const decreaseBtn = document.querySelector(".decrease-btn");

    
    let price = 35;
    function updatePrice() {
        priceElement.innerText = `₹${price}`;
    }

    function updateTPrice() {

        let quantity = parseInt(quantityInput.value);
        let totalPrice = price * quantity;
        tpriceElement.innerText = `₹${totalPrice}`;
    }

    sizeSelector.addEventListener("change", function () {
        if (sizeSelector.value === "ml") {
            price = 35;
        } else {
            price = 70;
        }
        updatePrice()
        updateTPrice();
    });

    quantityInput.addEventListener("input", updateTPrice);

    increaseBtn.addEventListener("click", function () {
        quantityInput.value = parseInt(quantityInput.value) + 1;
         updateTPrice();
    });

    decreaseBtn.addEventListener("click", function () {
        if (quantityInput.value > 1) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
             updateTPrice();
        }
    });

    ratingStars.forEach((star, index) => {
        star.addEventListener("click", function () {
            ratingStars.forEach(s => s.classList.remove("active"));
            for (let i = 0; i <= index; i++) {
                ratingStars[i].classList.add("active");
            }
            overallRating.innerText = (index + 1).toFixed(1);
        });
    });

    document.getElementById("submit-review").addEventListener("click", function () {
        const reviewText = document.getElementById("review-text").value;
        if (reviewText) {
            const reviewList = document.querySelector(".review-list");
            const newReview = document.createElement("div");
            newReview.classList.add("review-item");
            newReview.innerHTML = `<p>${reviewText}</p>`;
            reviewList.appendChild(newReview);
            document.getElementById("review-text").value = "";
        }
    });
    updateTPrice();
});

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

document.addEventListener("DOMContentLoaded", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "block";
});
window.addEventListener("load", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "none";
});


// productjs-future-update
// "I want to dynamically update product types and prices for an e-commerce site using a backend system. How can I set it up so sellers can add different types like 'ml', 'grams', and 'packets' from a seller page, and have these updates reflected in the product page template? Could you provide an example of the backend setup with a database, an API endpoint, and the frontend JavaScript to fetch and display this dynamic data?"
