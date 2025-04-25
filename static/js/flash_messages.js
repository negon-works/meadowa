document.addEventListener("DOMContentLoaded", function () {
    const messages = JSON.parse(document.getElementById("django-messages-data").textContent);
    messages.forEach(msg => {
      Swal.fire({
        icon: msg.tags || "info",
        title: msg.message,
        toast: true,
        position: "top-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
      });
    });
  });
  