document.addEventListener('DOMContentLoaded', function() {
    const togglePassword1 = document.querySelector('#togglePassword1');
    const password1 = document.querySelector('#password');
    const togglePassword2 = document.querySelector('#togglePassword2');
    const password2 = document.querySelector('#confirm_password');

    function togglePasswordVisibility(toggle, passwordField) {
        toggle.addEventListener('click', function () {
            // Toggle the type attribute
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            // Toggle the eye icon
            this.classList.toggle('fa-eye-slash');
        });
    }

    if (togglePassword1 && password1) {
        togglePasswordVisibility(togglePassword1, password1);
    }

    if (togglePassword2 && password2) {
        togglePasswordVisibility(togglePassword2, password2);
    }
});



