document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        // Captura os valores dos campos
        const cpf = document.getElementById("CPF").value.trim();
        const telefone = document.getElementById("telefone").value.trim();
        const dataNascimento = document.getElementById("data").value;
        const genero = document.getElementById("genero").value;
        const carro = document.getElementById("carro").value;

        // Resetando mensagens de erro
        document.querySelectorAll(".error-message").forEach(el => el.innerText = "");

        // Validação do CPF
        if (!validarCPF(cpf)) {
            document.getElementById("CPFerror").innerText = "CPF inválido.";
            isValid = false;
        }

        // Validação do telefone
        if (!validarTelefone(telefone)) {
            document.getElementById("telefoneError").innerText = "Telefone inválido (apenas números, 10 ou 11 dígitos).";
            isValid = false;
        }

        // Validação da data de nascimento
        if (!validarDataNascimento(dataNascimento)) {
            document.getElementById("dataError").innerText = "Você deve ter no mínimo 18 anos.";
            isValid = false;
        }

        // Validação do gênero
        if (!["1", "2", "3", "4"].includes(genero)) {
            document.getElementById("generoError").innerText = "Selecione um gênero válido.";
            isValid = false;
        }

        // Validação da opção de carro
        if (!["1", "2", "3"].includes(carro)) {
            document.getElementById("carroError").innerText = "Selecione uma opção válida.";
            isValid = false;
        }

        // Se houver erro, impede o envio do formulário
        if (!isValid) {
            event.preventDefault();
        }
    });

    // Função para validar CPF (mesma lógica do back-end)
    function validarCPF(cpf) {
        cpf = cpf.replace(/\D/g, ""); // Remove caracteres não numéricos

        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;

        function calcularDigito(cpfParcial, pesos) {
            const soma = cpfParcial.split("").reduce((acc, num, i) => acc + num * pesos[i], 0);
            const resto = soma % 11;
            return resto < 2 ? "0" : String(11 - resto);
        }

        const digito1 = calcularDigito(cpf.slice(0, 9), [...Array(9)].map((_, i) => 10 - i));
        const digito2 = calcularDigito(cpf.slice(0, 10), [...Array(10)].map((_, i) => 11 - i));

        return cpf.endsWith(digito1 + digito2);
    }

    // Função para validar telefone (somente números e 10 ou 11 dígitos)
    function validarTelefone(telefone) {
        return /^\d{10,11}$/.test(telefone);
    }

    // Função para validar data de nascimento (idade >= 18 anos)
    function validarDataNascimento(data) {
        if (!data) return false;

        const dataNascimento = new Date(data);
        const hoje = new Date();
        let idade = hoje.getFullYear() - dataNascimento.getFullYear();
        
        // Ajusta a idade caso ainda não tenha feito aniversário este ano
        const mesAtual = hoje.getMonth();
        const diaAtual = hoje.getDate();
        const mesNascimento = dataNascimento.getMonth();
        const diaNascimento = dataNascimento.getDate();

        if (mesAtual < mesNascimento || (mesAtual === mesNascimento && diaAtual < diaNascimento)) {
            idade--;
        }

        return idade >= 18;
    }
});