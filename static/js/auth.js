document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector('.container');
    const registerBtn = document.querySelector('.register-btn');
    const loginBtn = document.querySelector('.login-btn');

    // Toggle between Login and Register forms
    registerBtn.addEventListener('click', () => {
        container.classList.add('active');
    });

    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');
    });

    // Password Toggle Functionality
    const passwordFields = document.querySelectorAll(".input-box input[type='password']");
    const toggleIcons = document.querySelectorAll(".input-box i.bxs-lock-alt");

    toggleIcons.forEach((icon, index) => {
        icon.addEventListener("click", function () {
            if (passwordFields[index].type === "password") {
                passwordFields[index].type = "text";
                icon.classList.remove("bxs-lock-alt");
                icon.classList.add("bxs-lock-open-alt"); // Unlock Icon
            } else {
                passwordFields[index].type = "password";
                icon.classList.remove("bxs-lock-open-alt");
                icon.classList.add("bxs-lock-alt"); // Lock Icon
            }
        });
    });

    // OTP Verification Logic
    const loginBtnAction = document.getElementById("login-btn");
    const registerBtnAction = document.getElementById("register-btn");

    const loginOtpBox = document.getElementById("login-otp-box");
    const registerOtpBox = document.getElementById("register-otp-box");

    loginBtnAction.addEventListener("click", function () {
        // Send OTP for login
        sendOTP("login");
    });

    registerBtnAction.addEventListener("click", function () {
        // Send OTP for registration
        sendOTP("register");
    });

    function sendOTP(type) {
        if (type === "login") {
            // Show OTP Box for Login
            loginOtpBox.style.display = "block";
            loginBtnAction.style.display = "none";
        } else if (type === "register") {
            // Show OTP Box for Registration
            registerOtpBox.style.display = "block";
            registerBtnAction.style.display = "none";
        }

        // Simulate OTP sending (replace with actual backend logic)
        alert("OTP sent successfully. Please check your email.");
    }

    // Resend OTP Logic
    const resendLoginOtp = document.getElementById("resend-login-otp");
    const resendRegisterOtp = document.getElementById("resend-register-otp");

    resendLoginOtp.addEventListener("click", function () {
        alert("Resending OTP... Please check your email.");
    });

    resendRegisterOtp.addEventListener("click", function () {
        alert("Resending OTP... Please check your email.");
    });
});
