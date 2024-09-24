$(function() {
  /* ChartJS
   * -------
   * Data and config for chartjs
   */
  'use strict';

  // Função para buscar os dados do gráfico
  function fetchChartData(callback) {
    $.ajax({
      url: '/get_chart_data/',
      method: 'GET',
      success: function(response) {
        callback(response);
      },
      error: function(xhr, status, error) {
        console.error('Erro ao buscar os dados do gráfico:', error);
      }
    });
  }

  // Chamar a função para buscar os dados e inicializar o gráfico
  fetchChartData(function(chartData) {
    var data = {
      labels: chartData.labels,
      datasets: [{
        label: '# Atendimentos',
        data: chartData.data,
        backgroundColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderColor: [
          'rgba(255,99,132,1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 1,
        fill: false
      }]
    };

    var options = {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      legend: {
        display: true
      },
      elements: {
        point: {
          radius: 0
        }
      }
    };

    if ($("#barChart").length) {
      var barChartCanvas = $("#barChart").get(0).getContext("2d");
      // This will get the first returned node in the jQuery collection.
      var barChart = new Chart(barChartCanvas, {
        type: 'bar',
        data: data,
        options: options
      });
    }

  
  });
});
