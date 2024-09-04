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
        console.log("Evento de submissão capturado."); // Log de depuração
        // Seleciona os campos de nome e RA
        var nameField = $("#student-name-input").length ? $("#student-name-input") : $("#employee-name-input");
        var registryField = $("#student-registry-input").length ? $("#student-registry-input") : $("#employee-registry-input");


        // Obtém os valores dos campos e remove espaços em branco
        var nameValue = nameField.val().trim();
        var registryValue = registryField.val().trim();

        // Logs de depuração
        console.log("Nome:", nameValue); 
        console.log("Registro:", registryValue); 

        // Verifica se ambos os campos estão vazios
    if (nameValue === "" && registryValue === "") {
        // Evita o envio do formulário e a navegação para a próxima página
        event.preventDefault();
        console.log("Campos vazios, formulário não enviado."); // Log de depuração

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



    // Busca de nomes
    // Função para buscar alunos
    function searchStudents(query) {
        $.ajax({
            url: '/patients/students/search/name/',
            data: {
                'q': query
            },
            success: function(data) {
                var results = data.results;
                var resultsTable = $('#results-table tbody');
                resultsTable.empty(); // Limpa resultados anteriores

                if (results.length > 0) {
                    $('#results-container').show(); // Mostra a tabela

                    results.forEach(function(student) {
                        resultsTable.append(
                            '<tr>' +
                            '<td>' + student.name + '</td>' +
                            '<td>' + student.registry + '</td>' +
                            '<td>' + student.age + '</td>' +
                            '<td>' + student.class_group_name + '</td>' +
                            '</tr>'
                        );
                    });

                    // Adiciona evento de clique em cada linha
                    $('#results-table tbody tr').on('click', function() {
                        var name = $(this).find('td:eq(0)').text();
                        var registry = $(this).find('td:eq(1)').text();
                        $('#student-name-input').val("");
                        // O valor de nome não está sendo preenchido, pois está gerando bug com homônimos
                        // Corrigir em uma proxima versão
                        $('#student-registry-input').val(registry);
                        $('#results-container').hide(); // Esconde a tabela após seleção
                    });
                } else {
                    $('#results-container').hide(); // Esconde a tabela se não houver resultados
                }
            }
        });
    }

    // Função para buscar funcionários
    function searchEmployees(query) {
        $.ajax({
            url: '/patients/employees/search/name/',
            data: {
                'q': query
            },
            success: function(data) {
                var results = data.results;
                var resultsTable = $('#results-table tbody');
                resultsTable.empty(); // Limpa resultados anteriores

                if (results.length > 0) {
                    $('#results-container').show(); // Mostra a tabela

                    results.forEach(function(employee) {
                        resultsTable.append(
                            '<tr>' +
                            '<td>' + employee.name + '</td>' +
                            '<td>' + employee.registry + '</td>' +
                            '<td>' + employee.department_name + '</td>' +
                            '</tr>'
                        );
                    });

                    // Adiciona evento de clique em cada linha
                    $('#results-table tbody tr').on('click', function() {
                        var name = $(this).find('td:eq(0)').text();
                        var registry = $(this).find('td:eq(1)').text();
                        $('#employee-name-input').val("");
                        // O valor de nome não está sendo preenchido, pois está gerando bug com homônimos
                        // Corrigir em uma proxima versão
                        $('#employee-registry-input').val(registry);
                        $('#results-container').hide(); // Esconde a tabela após seleção
                    });
                } else {
                    $('#results-container').hide(); // Esconde a tabela se não houver resultados
                }
            }
        });
    }

    // Função para buscar visitantes
    function searchVisitors(query) {
        $.ajax({
            url: '/patients/visitors/search/name/',
            data: {
                'q': query
            },
            success: function(data) {
                var results = data.results;
                var resultsTable = $('#results-table tbody');
                resultsTable.empty(); // Limpa resultados anteriores

                if (results.length > 0) {
                    $('#results-container').show(); // Mostra a tabela

                    results.forEach(function(visitor) {
                        resultsTable.append(
                            '<tr>' +
                            '<td>' + visitor.name + '</td>' +
                            '<td>' + visitor.age + '</td>' +
                            '<td>' + visitor.relationship + '</td>' +
                            '</tr>'
                        );
                    });

                    // Adiciona evento de clique em cada linha
                    $('#results-table tbody tr').on('click', function() {
                        var name = $(this).find('td:eq(0)').text();
                        $('#visitor-name-input').val(name);
                        $('#results-container').hide(); // Esconde a tabela após seleção
                    });
                } else {
                    $('#results-container').hide(); // Esconde a tabela se não houver resultados
                }
            }
        });
    }

    // Captura de eventos de keyup para diferentes inputs
    $('#student-name-input').on('keyup', function() {
        var query = $(this).val();
        if (query.length >= 3) {
            searchStudents(query);
        } else {
            $('#results-container').hide();
        }
    });

    $('#employee-name-input').on('keyup', function() {
        var query = $(this).val();
        if (query.length >= 3) {
            searchEmployees(query);
        } else {
            $('#results-container').hide();
        }
    });

    $('#visitor-name-input').on('keyup', function() {
        var query = $(this).val();
        if (query.length >= 3) {
            searchVisitors(query);
        } else {
            $('#results-container').hide();
        }
    });
});