$(document).ready(function() {
    // Verifica se jQuery está carregado corretamente
    if (typeof $ === 'undefined') {
        console.error("jQuery não está carregado. Certifique-se de que jQuery está sendo incluído antes deste script.");
        return;
    }

    // Seleciona o formulário
    var form = $("#searchForm");

    // Adiciona um evento de submissão ao formulário
    form.on("submit", function(event) {
        // Seleciona os campos de nome e RA
        var nameField = $("#name");
        var registryField = $("#registry");

        // Obtém os valores dos campos e remove espaços em branco
        var nameValue = nameField.val().trim();
        var registryValue = registryField.val().trim();

        // Verifica se ambos os campos estão vazios
        if (nameValue === "" && registryValue === "") {
            // Evita o envio do formulário e a navegação para a próxima página
            event.preventDefault();

            // Exibe a mensagem de erro no contêiner de erro
            $("#error-message-container").html("<div class='alert alert-danger'>Por favor, preencha pelo menos um dos campos.</div>");

            // Adiciona classes de erro para destacar os campos
            nameField.addClass('form-control-danger');
            registryField.addClass('form-control-danger');

        } else {
            // Se pelo menos um campo estiver preenchido, remove as mensagens de erro e classes
            nameField.removeClass('form-control-danger');
            registryField.removeClass('form-control-danger');
            $("#error-message-container").html(""); // Limpa a mensagem de erro

        
        }
    });
});