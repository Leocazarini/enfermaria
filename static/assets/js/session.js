
function saveInfirmary(infirmary) {
        // Armazenar o valor no sessionStorage
    sessionStorage.setItem('infirmary', infirmary);
    console.log('Enfermaria salva: ' + infirmary);
        
        // Atualizar o conteúdo do card com a enfermaria selecionada
    document.getElementById('selectedInfirmary').textContent = infirmary;

    document.cookie = "infirmary=" + encodeURIComponent(infirmary) + "; path=/";
}

    // Função para atualizar o card ao carregar a página
function updateInfirmary() {
    const infirmary = sessionStorage.getItem('infirmary');
    if (infirmary) {
        document.getElementById('selectedInfirmary').textContent = infirmary;
    }
}

function fillFormFields() {
    console.log("Preenchendo os campos do formulário.");
    const infirmary = sessionStorage.getItem('infirmary');

    console.log('Enfermaria: ' + infirmary);


    if (infirmary) {
        document.getElementById('selectedInfirmary').value = infirmary;
    }
}

document.addEventListener('DOMContentLoaded', fillFormFields);
document.addEventListener('DOMContentLoaded', updateInfirmary);


document.addEventListener('DOMContentLoaded', function() {
    fetch('/get_user/')
        .then(response => response.json())
        .then(data => {
            if (data.first_name) {
                sessionStorage.setItem('userFirstName', data.first_name);
                console.log('Nome do usuário: ' + data.first_name);
            } else {
                console.error('Erro ao obter nome do usuário:', data.error);
            }
        })
        .catch(error => {
            console.error('Erro na requisição AJAX:', error);
        });


        var userFirstName = sessionStorage.getItem('userFirstName');

    // Verificar se o valor existe e preencher o campo do formulário
        if (userFirstName) {
            var userFirstNameInput = document.getElementById('userFirstName');
            if (userFirstNameInput) {
                userFirstNameInput.value = userFirstName;
            } else {
                console.error('Campo de formulário não encontrado.');
            }
        } else {
        console.log('Nome do usuário não encontrado no sessionStorage.');
    }
});