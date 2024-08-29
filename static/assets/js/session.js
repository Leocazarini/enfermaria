const userFirstName = document.getElementById('userFirstName').textContent.trim();
sessionStorage.setItem('userFirstName', userFirstName);
console.log('Nome do usuário armazenado:', userFirstName);

        
function saveInfirmary(infirmary) {
        // Armazenar o valor no sessionStorage
    sessionStorage.setItem('infirmary', infirmary);
    console.log('Enfermaria salva: ' + infirmary);
        
        // Atualizar o conteúdo do card com a enfermaria selecionada
    document.getElementById('selectedInfirmary').textContent = infirmary;
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
    const userFirstName = sessionStorage.getItem('userFirstName');
    const infirmary = sessionStorage.getItem('infirmary');

    console.log('Nome do usuário: ' + userFirstName);
    console.log('Enfermaria: ' + infirmary);

    if (userFirstName) {
        document.getElementById('userFirstName').value = userFirstName;
    }

    if (infirmary) {
        document.getElementById('selectedInfirmary').value = infirmary;
    }
}

document.addEventListener('DOMContentLoaded', fillFormFields);

window.onload = fillFormFields;
    // Chamar a função ao carregar a página
window.onload = updateInfirmary;