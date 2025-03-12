const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
    container.classList.add('active');
})

loginBtn.addEventListener('click', () => {
    container.classList.remove('active');
})

document.addEventListener("DOMContentLoaded", function () {
    const passwordFields = document.querySelectorAll(".input-box input[type='password']");
    const toggleIcons = document.querySelectorAll(".input-box i.bxs-lock-alt");

    toggleIcons.forEach((icon, index) => {
        icon.addEventListener("click", function () {
            if (passwordFields[index].type === "password") {
                passwordFields[index].type = "text";
                icon.classList.remove("bxs-lock-alt");
                icon.classList.add("bxs-lock-open-alt"); // Change to unlocked icon
            } else {
                passwordFields[index].type = "password";
                icon.classList.remove("bxs-lock-open-alt");
                icon.classList.add("bxs-lock-alt"); // Change back to locked icon
            }
        });
    });
});
