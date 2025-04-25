


document.addEventListener("DOMContentLoaded", function () {
    const categoryFilter = document.getElementById("categoryFilter");
    const priceSort = document.getElementById("priceSort");
    const productContainer = document.querySelector(".product-container");
    const products = Array.from(document.querySelectorAll(".card"));

    // Function to Filter and Sort Products
    function filterAndSortProducts() {
        let selectedCategory = categoryFilter.value;
        let sortOrder = priceSort.value;

        // Step 1: Filter Products by Category
        let filteredProducts = products.filter(product => {
            let productCategory = product.getAttribute("data-category");
            return selectedCategory === "all" || productCategory === selectedCategory;
        });

        // Step 2: Sort Products by Price
        if (sortOrder === "low") {
            filteredProducts.sort((a, b) => {
                return parseInt(a.getAttribute("data-price")) - parseInt(b.getAttribute("data-price"));
            });
        } else if (sortOrder === "high") {
            filteredProducts.sort((a, b) => {
                return parseInt(b.getAttribute("data-price")) - parseInt(a.getAttribute("data-price"));
            });
        }

        // Step 3: Update Displayed Prices & Render Products
        productContainer.innerHTML = "";
        filteredProducts.forEach(product => {
            let priceElement = product.querySelector(".card-footer .text-title");
            let updatedPrice = product.getAttribute("data-price");
            priceElement.textContent = `₹${updatedPrice}`; // Update displayed price
            productContainer.appendChild(product);
        });
    }

    // Event Listeners for Category & Price Sort
    categoryFilter.addEventListener("change", filterAndSortProducts);
    priceSort.addEventListener("change", filterAndSortProducts);

    // Run the function once on page load
    // Helper to get URL query parameters
function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Set dropdown based on URL category (if exists)
const initialCategory = getQueryParam("category");
if (initialCategory) {
    // Match the value to what’s in the dropdown (case-sensitive)
    const options = Array.from(categoryFilter.options);
    const match = options.find(opt => opt.value.toLowerCase() === initialCategory.toLowerCase());
    if (match) {
        categoryFilter.value = match.value;
    }
}

// Run the filter based on URL or default
filterAndSortProducts();

});

