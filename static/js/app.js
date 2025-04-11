document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector("form");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const passwordContainer = document.querySelector(".password-container"); 

    function createErrorElement(insertBefore) {
        let error = document.createElement("span");
        error.classList.add("error-message");
        error.style.display = "block";  
        insertBefore.parentNode.insertBefore(error, insertBefore); 
        return error;
    }
    

    const emailError = createErrorElement(emailInput);
    const passwordError = createErrorElement(passwordContainer);
    const confirmPasswordError = confirmPasswordInput ? createErrorElement(confirmPasswordInput) : null;

    function togglePasswordVisibility(toggle, passwordField) {
        toggle.addEventListener('click', function () {
            const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordField.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }

    const togglePassword1 = document.querySelector('#togglePassword1');
    const togglePassword2 = document.querySelector('#togglePassword2');

    if (togglePassword1 && passwordInput) togglePasswordVisibility(togglePassword1, passwordInput);
    if (togglePassword2 && confirmPasswordInput) togglePasswordVisibility(togglePassword2, confirmPasswordInput);

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPassword(password) {
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d])[^\s]{8,}$/;
        return passwordRegex.test(password);
    }

    function showError(errorElement, message) {
        errorElement.textContent = message;
        errorElement.style.display = "block";
    }

    function clearError(errorElement) {
        errorElement.textContent = "";
        errorElement.style.display = "none";
    }

    form.addEventListener("submit", function (event) {
        let hasError = false;

        clearError(emailError);
        clearError(passwordError);
        if (confirmPasswordError) clearError(confirmPasswordError);

        if (!isValidEmail(emailInput.value)) {
            showError(emailError, "Email inválido.");
            hasError = true;
        }

        if (confirmPasswordInput) {
            if (!isValidPassword(passwordInput.value)) {
                showError(passwordError, "A senha deve ter no mínimo 8 caracteres, incluindo uma letra minúscula, uma maiúscula, um número e um caractere especial.");
                hasError = true;
            }

            if (passwordInput.value !== confirmPasswordInput.value) {
                showError(confirmPasswordError, "As senhas não coincidem.");
                hasError = true;
            }
        } else {
            if (passwordInput.value.trim() === "") {
                showError(passwordError, "A senha não pode estar vazia.");
                hasError = true;
            }
        }

        if (hasError) {
            event.preventDefault();
        }
    });
});
