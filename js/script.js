window.addEventListener('scroll', function() {
            let header = document.querySelector('.navbar');
            let navLinks = document.querySelectorAll('.logo a,.nav-links a,.profile-icon ');
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
                navLinks.forEach(link => link.style.color = '#CDAA7D');
            } else {
                header.classList.remove('scrolled');
                navLinks.forEach(link => link.style.color = 'white');
            }
        });




document.addEventListener("DOMContentLoaded", function () {
    console.log("FAQ script loaded...");

    const tabs = document.querySelectorAll("#faq .tab_head a");
    const contents = document.querySelectorAll("#faq .tab_body .item");

    console.log("Tabs found:", tabs.length);
    console.log("Contents found:", contents.length);

    if (tabs.length === 0 || contents.length === 0) {
        console.error("FAQ elements not found! Check your HTML.");
        return;
    }

    tabs.forEach(tab => {
        tab.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default link behavior
            console.log("Tab clicked:", this.dataset.id);

            tabs.forEach(t => t.classList.remove("active"));
            contents.forEach(content => content.classList.remove("active"));

            this.classList.add("active");
            document.getElementById(this.dataset.id)?.classList.add("active");
        });
    });
});




document.addEventListener("DOMContentLoaded", function () {
    const testimonialSlider = document.querySelector(".testimonial-slider");
    const leftArrow = document.querySelector(".arrow.left");
    const rightArrow = document.querySelector(".arrow.right");
    const dotsContainer = document.querySelector(".dots");

    // Duplicate testimonials for continuous loop
    testimonialSlider.innerHTML = testimonialSlider.innerHTML + testimonialSlider.innerHTML + testimonialSlider.innerHTML;

    const testimonials = document.querySelectorAll(".testimonial");

    let currentIndex = testimonials.length / 3; // Starting at the first clone to enable smooth looping
    const totalTestimonials = testimonials.length / 3; // Original number of testimonials

    // Function to show the testimonial at the current index
    function showTestimonial(index, transition = true) {
        currentIndex = index;  // Update currentIndex before using it in calculations
        const offset = -index * 100;  // Move by 100% of one testimonial's width
        testimonialSlider.style.transition = transition ? "transform 0.5s ease" : "none";  // Smooth or none transition
        testimonialSlider.style.transform = `translateX(${offset}%)`;

        // Update the active dot indicator
        updateDots();

        // Loop back to the start seamlessly for both directions
        if (index >= testimonials.length - totalTestimonials) {
            setTimeout(() => {
                testimonialSlider.style.transition = "none";
                testimonialSlider.style.transform = `translateX(${-totalTestimonials * 100}%)`;
                currentIndex = totalTestimonials;
                updateDots();
            }, 500); // Adjust timeout to match the transition duration
        } else if (index < 0) {
            setTimeout(() => {
                testimonialSlider.style.transition = "none";
                testimonialSlider.style.transform = `translateX(${-totalTestimonials * 2 * 100}%)`;
                currentIndex = totalTestimonials * 2 - 1;
                updateDots();
            }, 500); // Adjust timeout to match the transition duration
        }
    }

    // Function to update the active dot indicator based on current slide
    function updateDots() {
        const dots = document.querySelectorAll(".dot");
        dots.forEach(dot => dot.classList.remove("active"));
        let activeIndex = currentIndex % totalTestimonials;
        if (activeIndex < 0) activeIndex += totalTestimonials;
        dots[activeIndex].classList.add("active");
    }

    // Right arrow click event - Move forward (next slide)
    rightArrow.addEventListener("click", function () {
        showTestimonial(currentIndex + 1); // Go to the next testimonial
    });

    // Left arrow click event - Move backward (previous slide, looping to the last)
    leftArrow.addEventListener("click", function () {
        showTestimonial(currentIndex - 1); // Go to the previous testimonial
    });

    // Dot click event - Clicking a dot takes us to the corresponding slide
    dotsContainer.addEventListener("click", function (e) {
        if (e.target.classList.contains('dot')) {
            const index = Array.from(dotsContainer.children).indexOf(e.target);
            showTestimonial(index); // Go to the corresponding testimonial
        }
    });

    // Auto slide every 3 seconds (optional)
    setInterval(function () {
        showTestimonial(currentIndex + 1);  // Auto slide to the next testimonial
    }, 3000);

    // Dynamically create dots based on the number of testimonials
    function createDots() {
        dotsContainer.innerHTML = '';  // Clear any existing dots

        // Create a dot for each testimonial
        for (let i = 0; i < totalTestimonials; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            dotsContainer.appendChild(dot);
        }

        updateDots(); // Initialize dots with the first one as active
    }

    createDots();  // Initialize dots based on the number of testimonials
    showTestimonial(currentIndex, false);  // Show the first testimonial on load
});




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
    const container = document.querySelector(".product-categories");
    
    // Create left and right buttons
    const leftBtn = document.createElement("button");
    const rightBtn = document.createElement("button");

    leftBtn.innerHTML = "&lt;";
    rightBtn.innerHTML = "&gt;";
    leftBtn.classList.add("scroll-btn", "left-btn");
    rightBtn.classList.add("scroll-btn", "right-btn");

    // Insert buttons inside scroll-container
    container.parentNode.insertBefore(leftBtn, container);
    container.parentNode.appendChild(rightBtn);

    const scrollAmount = container.children[0].offsetWidth + 20; // Card width + gap

    leftBtn.addEventListener("click", function () {
        container.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        setTimeout(checkOverflow, 500); // Delay to check after scroll
    });

    rightBtn.addEventListener("click", function () {
        container.scrollBy({ left: scrollAmount, behavior: "smooth" });
        setTimeout(checkOverflow, 500);
    });

    // Hide buttons if there’s no overflow
    function checkOverflow() {
        leftBtn.style.display = container.scrollLeft > 0 ? "block" : "none";
        rightBtn.style.display = 
            container.scrollWidth > container.clientWidth + container.scrollLeft ? "block" : "none";
    }

    container.addEventListener("scroll", checkOverflow);
    window.addEventListener("resize", checkOverflow);
    checkOverflow(); // Initial check
});


document.addEventListener("DOMContentLoaded", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "block";
});
window.addEventListener("load", function() {
    var loadingAnimation = document.getElementById("loadingAnimation");
    loadingAnimation.style.display = "none";
});
