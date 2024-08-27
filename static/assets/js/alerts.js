(function($) {
  showSwal = function(type) {
    'use strict';
    if (type === 'basic') {
      swal({
        text: 'Any fool can use a computer',
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })

    } else if (type === 'error-message') {
      swal({
        title: 'Erro!',
        text: message,  // Usa a mensagem recebida como parâmetro
        icon: 'error',
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      });
    } else if (type === 'title-and-text') {
      swal({
        title: 'Read the alert!',
        text: 'Click OK to close this alert',
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })

    } else if (type === 'success-message') {
      swal({
        title: 'Congratulations!',
        text: 'You entered the correct answer',
        icon: 'success',
        button: {
          text: "Continue",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })

    } else if (type === 'auto-close') {
      swal({
        title: 'Auto close alert!',
        text: 'I will close in 2 seconds.',
        timer: 2000,
        button: false
      }).then(
        function() {},
        // handling the promise rejection
        function(dismiss) {
          if (dismiss === 'timer') {
            console.log('I was closed by the timer')
          }
        }
      )
    } else if (type === 'warning-message-and-cancel') {
      swal({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3f51b5',
        cancelButtonColor: '#ff4081',
        confirmButtonText: 'Great ',
        buttons: {
          cancel: {
            text: "Cancel",
            value: null,
            visible: true,
            className: "btn btn-danger",
            closeModal: true,
          },
          confirm: {
            text: "OK",
            value: true,
            visible: true,
            className: "btn btn-primary",
            closeModal: true
          }
        }
      })

    } else if (type === 'custom-html') {
      swal({
        content: {
          element: "input",
          attributes: {
            placeholder: "Type your password",
            type: "password",
            class: 'form-control'
          },
        },
        button: {
          text: "OK",
          value: true,
          visible: true,
          className: "btn btn-primary"
        }
      })
    }
  }


  $(document).ready(function() {
    $('#searchForm').on('submit', function(event) {
      event.preventDefault();  // Impede o envio padrão do formulário

      var form = $(this);
      var actionUrl = form.attr('action');
      var formData = form.serialize();

      // Faz uma requisição AJAX para a URL especificada
      $.ajax({
        url: actionUrl,
        method: 'GET',
        data: formData,
        dataType: 'json',
        success: function(response) {
          if (response.status === 'success') {
            // Lida com os dados do paciente retornados com sucesso
            // Aqui você pode redirecionar, exibir os dados, etc.
            // Exemplo de redirecionamento ou renderização de informações na página
            window.location.href = "appointments/student";  // Ajuste isso conforme sua lógica
          } else if (response.status === 'error') {
            // Exibe a mensagem de erro usando swal
            showSwal('error-message', response.message);
          }
        },
        error: function(xhr) {
          var response = xhr.responseJSON;
          if (response && response.status === 'error') {
            // Exibe a mensagem de erro usando swal
            showSwal('error-message', response.message);
          } else {
            // Lida com possíveis outros erros de rede
            showSwal('error-message', 'Ocorreu um erro inesperado. Tente novamente.');
          }
        }
      });
    });
  });

})(jQuery);