let map; // Variável global para armazenar o mapa

function buscarCep() {
    let cep = document.getElementById("cep").value.trim();

    if (cep.length !== 8 || isNaN(cep)) {
        alert("Por favor, insira um CEP válido com 8 dígitos.");
        return;
    }

    fetch(`/buscar_cep?cep=${cep}`)
        .then(response => response.json())
        .then(data => {
            if (data.latitude && data.longitude) {
                exibirMapa(data.latitude, data.longitude);
            } else {
                alert("CEP inválido ou não encontrado!");
            }
        })
        .catch(error => {
            console.error("Erro na requisição:", error);
            alert("Erro ao buscar o CEP!");
        });
}

function exibirMapa(lat, lon) {
    if (!map) {
        // Se o mapa ainda não foi inicializado, cria um novo
        map = L.map('map').setView([lat, lon], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
    } else {
        // Se o mapa já existe, apenas move a visualização para a nova localização
        map.setView([lat, lon], 13);
    }

    // Adiciona um marcador na nova posição
    L.marker([lat, lon]).addTo(map).bindPopup("Localização encontrada!").openPopup();
}
