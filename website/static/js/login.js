document.addEventListener("DOMContentLoaded", function () {
  const togglePassword = document.getElementById("togglePassword");
  const passwordField = document.getElementById("password");
  const icon = togglePassword.querySelector("i");

  passwordField.setAttribute("type", "password");
  icon.classList.add("bi-eye-slash");
  icon.classList.remove("bi-eye");

  togglePassword.addEventListener("click", function () {
    const type =
      passwordField.getAttribute("type") === "password" ? "text" : "password";
    passwordField.setAttribute("type", type);

    icon.classList.toggle("bi-eye");
    icon.classList.toggle("bi-eye-slash");
  });
});
