document.addEventListener('DOMContentLoaded', function() {
    const reportForm = document.getElementById('report-form');
    const errorMessageContainer = document.getElementById('error-message-container');
    const reportResultsContainer = document.getElementById('report-results-container');

    // Função para enviar o formulário com a página especificada
    function submitForm(page = 1) {
        // Limpa mensagens de erro anteriores
        errorMessageContainer.innerHTML = '';

        // Coleta os dados do formulário
        const dateBegin = document.getElementById('search-date-begin').value;
        const dateEnd = document.getElementById('search-date-end').value;

        // Verifica se pelo menos uma enfermaria foi selecionada
        const infirmaryCheckboxes = document.querySelectorAll('input[name="infirmaries"]:checked');
        const infirmaries = Array.from(infirmaryCheckboxes).map(checkbox => checkbox.value);

        console.log(infirmaries);
        console.log(dateBegin);
        console.log(dateEnd);

        // Validação dos campos
        const errors = [];
        if (!dateBegin) {
            errors.push('Por favor, preencha a data de início.');
        }
        if (!dateEnd) {
            errors.push('Por favor, preencha a data de fim.');
        }
        if (infirmaries.length === 0) {
            errors.push('Por favor, selecione pelo menos uma enfermaria.');
        }

        if (errors.length > 0) {
            // Exibe as mensagens de erro
            errors.forEach(error => {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger';
                errorDiv.innerText = error;
                errorMessageContainer.appendChild(errorDiv);
            });
            return;
        }

        // Prepara os dados para envio
        const formData = new FormData(reportForm);

        // Adiciona o número da página ao FormData
        formData.append('page', page);

        // Envia a requisição via AJAX
        fetch(reportForm.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw data;
                });
            }
            return response.text();
        })
        .then(html => {
            // Atualiza o contêiner de resultados com o HTML retornado
            reportResultsContainer.innerHTML = html;

            // Reatribui os event listeners aos novos links de paginação
            assignPaginationEvents();
        })
        .catch(data => {
            // Exibe mensagens de erro retornadas pelo servidor
            if (data.errors) {
                data.errors.forEach(error => {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'alert alert-danger';
                    errorDiv.innerText = error;
                    errorMessageContainer.appendChild(errorDiv);
                });
            } else {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'alert alert-danger';
                errorDiv.innerText = 'Ocorreu um erro ao processar a requisição.';
                errorMessageContainer.appendChild(errorDiv);
            }
        });
    }

    // Função para atribuir eventos aos links de paginação
    function assignPaginationEvents() {
        const pageLinks = document.querySelectorAll('.page-link.page-btn');
        pageLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const page = this.getAttribute('data-page');
                submitForm(page);
            });
        });
    }

    // Evento de submissão do formulário
    reportForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        // Envia o formulário com a página 1
        submitForm(1);
    });

    // Inicializa os eventos de paginação (caso a página já carregue com resultados)
    assignPaginationEvents();
});
