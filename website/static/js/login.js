document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');
    const icon = togglePassword.querySelector('i');

    // Set initial state: password hidden, icon as eye-slash
    passwordField.setAttribute('type', 'password');
    icon.classList.add('bi-eye-slash');
    icon.classList.remove('bi-eye');

    togglePassword.addEventListener('click', function() {
        // Toggle the type attribute
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);

        // Toggle the icon class
        icon.classList.toggle('bi-eye');
        icon.classList.toggle('bi-eye-slash');
    });
});
