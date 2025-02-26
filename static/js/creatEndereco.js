document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const cepInput = document.getElementById("CEP");
    const numeroInput = document.getElementById("numero");
    const complementoInput = document.getElementById("complemento");
    const ruaInput = document.getElementById("rua");
    const cidadeInput = document.getElementById("cidade");
    const ufSelect = document.getElementById("uf");
    const maxRuaLength = 65;
    const maxCidadeLength = 40;
    const maxCepLength = 8;
    const maxComplementoLength = 200;
    const maxUfLength = 2;
    
    cepInput.addEventListener("input", function () {
        this.value = this.value.replace(/\D/g, "").slice(0, maxCepLength);
    });

    ruaInput.addEventListener("input", function () {
        if (this.value.length > maxRuaLength) {
            this.value = this.value.slice(0, maxRuaLength);
        }
    });

    cidadeInput.addEventListener("input", function () {
        if (this.value.length > maxCidadeLength) {
            this.value = this.value.slice(0, maxCidadeLength);
        }
    });

    complementoInput.addEventListener("input", function () {
        if (this.value.length > maxComplementoLength) {
            this.value = this.value.slice(0, maxComplementoLength);
        }
    });

    ufSelect.addEventListener("input", function () {
        if (this.value.length > maxUfLength) {
            this.value = this.value.slice(0, maxUfLength);
        }
    });

    cepInput.addEventListener("blur", function () {
        const cep = this.value;
        if (cep.length === maxCepLength) {
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => response.json())
                .then(data => {
                    if (!data.erro) {
                        ruaInput.value = data.logradouro.slice(0, maxRuaLength);
                        cidadeInput.value = data.localidade.slice(0, maxCidadeLength);
                        ufSelect.value = data.uf.slice(0, maxUfLength);
                        document.getElementById("cepError").textContent = "";
                    } else {
                        document.getElementById("cepError").textContent = "CEP inválido";
                    }
                })
                .catch(error => {
                    console.error("Erro ao buscar o CEP:", error);
                    document.getElementById("cepError").textContent = "Erro ao buscar o CEP";
                });
        } else {
            document.getElementById("cepError").textContent = "CEP deve ter exatamente " + maxCepLength + " dígitos.";
        }
    });

    form.addEventListener("submit", function (event) {
        let valid = true;

        if (cepInput.value.length !== maxCepLength || document.getElementById("cepError").textContent !== "") {
            document.getElementById("cepError").textContent = "CEP inválido";
            valid = false;
        }

        if (!numeroInput.value) {
            document.getElementById("numeroError").textContent = "Número é obrigatório";
            valid = false;
        } else {
            document.getElementById("numeroError").textContent = "";
        }

        if (!ruaInput.value) {
            document.getElementById("ruaError").textContent = "Rua é obrigatória";
            valid = false;
        } else {
            document.getElementById("ruaError").textContent = "";
        }

        if (!cidadeInput.value) {
            document.getElementById("cidadeError").textContent = "Cidade é obrigatória";
            valid = false;
        } else {
            document.getElementById("cidadeError").textContent = "";
        }

        if (!ufSelect.value) {
            alert("UF é obrigatório");
            valid = false;
        }

        if (complementoInput.value.length > maxComplementoLength) {
            document.getElementById("complementoError").textContent = "Complemento excede o limite de " + maxComplementoLength + " caracteres";
            valid = false;
        } else {
            document.getElementById("complementoError").textContent = "";
        }

        if (!valid) {
            event.preventDefault();
        }
    });
});
