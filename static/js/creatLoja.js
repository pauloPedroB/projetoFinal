document.addEventListener("DOMContentLoaded", function () {
    document.querySelector("form").addEventListener("submit", function (event) {
        let isValid = true;

        // Validação do CNPJ
        const cnpjInput = document.getElementById("CNPJ");
        const cnpjError = document.getElementById("CNPJerror");
        if (!validarCNPJ(cnpjInput.value)) {
            cnpjError.textContent = "CNPJ INVÁLIDO";
            isValid = false;
        } else {
            cnpjError.textContent = "";
        }

        // Validação do Nome Fantasia
        const nomeInput = document.getElementById("nomeFantasia");
        const nameError = document.getElementById("nameError");
        if (!validarNome(nomeInput.value)) {
            nameError.textContent = "Nome Fantasia Inválido";
            isValid = false;
        } else {
            nameError.textContent = "";
        }

        // Validação da Razão Social
        const razaoInput = document.getElementById("razaoSocial");
        const razaoError = document.getElementById("razaoError");
        if (!validarNome(razaoInput.value)) {
            razaoError.textContent = "Razão Social Inválida";
            isValid = false;
        } else {
            razaoError.textContent = "";
        }

        // Validação do Telefone
        const telefoneInput = document.getElementById("telefone");
        const telefoneError = document.getElementById("telefoneError");
        if (!validarTelefone(telefoneInput.value)) {
            telefoneError.textContent = "Telefone Inválido";
            isValid = false;
        } else {
            telefoneError.textContent = "";
        }

        // Validação do Celular (opcional)
        const celularInput = document.getElementById("celular");
        const cellError = document.getElementById("cellError");
        if (celularInput.value !== "" && !validarTelefone(celularInput.value)) {
            cellError.textContent = "Número de Telefone Inválido";
            isValid = false;
        } else {
            cellError.textContent = "";
        }

        // Validação da Data de Abertura
        const dataInput = document.getElementById("abertura");
        const dataError = document.getElementById("dataError");
        if (!validarDataAbertura(dataInput.value)) {
            dataError.textContent = "Data inválida";
            isValid = false;
        } else {
            dataError.textContent = "";
        }

        if (!isValid) {
            event.preventDefault(); // Impede o envio do formulário
        }
    });
});

function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, "");
    if (cnpj.length !== 14) return false;

    const pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
    const pesos2 = [6].concat(pesos1);

    function calcularDigito(cnpjParcial, pesos) {
        let soma = cnpjParcial.split("").reduce((acc, num, i) => acc + num * pesos[i], 0);
        let resto = soma % 11;
        return resto < 2 ? "0" : String(11 - resto);
    }

    let digito1 = calcularDigito(cnpj.slice(0, 12), pesos1);
    let digito2 = calcularDigito(cnpj.slice(0, 12) + digito1, pesos2);

    return cnpj.endsWith(digito1 + digito2);
}

function validarNome(nome) {
    return nome.length >= 3 && nome.length <= 65 && /^[a-zA-Záéíóúãõâêîôûàèìòùãẽĩõũ ]+$/.test(nome.trim());
}

function validarTelefone(telefone) {
    return /^\d{10,11}$/.test(telefone.replace(/\D/g, ""));
}

function validarDataAbertura(data) {
    if (!data) return false;
    const dataAbertura = new Date(data);
    const dataAtual = new Date();
    return dataAbertura <= dataAtual;
}
