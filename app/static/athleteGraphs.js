$('#btn-graphs').on('click', function(){
  var _data_target;
  var _data_result
  var _labels;
  $.ajax({
    url: window.location.pathname + '/graph_get_data',
    type: "get",
    data: {},
    success: function(response) {
     full_data = JSON.parse(response.payload);
     _data_target = full_data['target'];
     _data_result = full_data['result'];
     _success = full_data['success']
     _labels = full_data['labels'];
    },
    complete: function(data) {

    Chart.defaults.global.tooltipYPadding = 16;
    Chart.defaults.global.tooltipCornerRadius = 0;
    Chart.defaults.global.tooltipTitleFontStyle = "normal";
    Chart.defaults.global.tooltipFillColor = "rgba(0,0,0,0.8)";

    new Chart($('#myLineChart'), {
      type: 'line',
      data: {
        responsive: false,
        labels: _labels,
        datasets: [{
            label: "Targets",
            borderColor: "#cd3e4e",
            pointBorderColor: "#cd3e4e",
            pointBackgroundColor: "#cd3e4e",
            pointHoverBackgroundColor: "#fff",
            pointHitRadius: 20,
            fill: false,
            lineTension: 0,
            data: _data_target,
            yAxisID: 'y-axis-1'
          }, {
            label: "Results",
            fill: false,
            borderColor: "#3e95cd",
            pointBorderColor: "#3e95cd",
            pointBackgroundColor: "#3e95cd",
            pointHoverBackgroundColor: "#fff",
            pointHitRadius: 20,
            lineTension: 0,
            data: _data_result,
            yAxisID: 'y-axis-1'
          }, {
            type: 'bar',
            label: "Success",
            data: _success,
            borderColor: 'rgba(205,190,62,1)',
            borderWidth: 1,
            backgroundColor: 'rgba(205,190,62,0.2)',

            yAxisID: 'y-axis-2'
          }
        ]
      },
      options: {
        legend: {
          position: "bottom",
          display: true
        },
        title: {
          display: false,
          text: "target VS results"
        },
        scales: {
          yAxes: [{
            id: "y-axis-1",
            position: "left",
            ticks: {
              padding: 20,
              fontColor: "rgba(0,0,0,0.5)",
              fontStyle: "bold"
            },
            scaleLabel: {
              display: true,
              labelString: 'points'
            }
          }, {
            id: "y-axis-2",
            position: "right",
            ticks: {
              padding: 20,
              fontColor: "rgba(0,0,0,0.5)",
              fontStyle: "bold"
            },
            scaleLabel: {
              display: true,
              labelString: '% of target'
            },
            gridLines: {
              display:false
            }
          }],
          xAxes: [{
            ticks: {
              padding: 10,
              fontColor: "rgba(0,0,0,0.5)",
              fontStyle: "bold"
            },
            offset: true
          }]
        },
        tooltips: {
          mode: 'index',
        }
      }
    });

    }
  });
});

  // new Chart(document.getElementById('myRadarChart'), {
  //   type: 'radar',
  //   data: {
  //     labels: ['FX', 'PH', 'SR', 'VT', 'PB', 'HB'],
  //     datasets: [
  //       {
  //         label: "1st Quebec Cub",
  //         fill: false,
  //         // backgroundColor: "rgba(205,62,149,0.2)",
  //         borderColor: "rgba(205,62,149,1)",
  //         pointBorderColor: "#fff",
  //         pointBackgroundColor: "rgba(205,62,149,1)",
  //         pointHitRadius: 20,
  //         data: [91.12, 90.23, 82.34, 95.12, 90.21, 89.42]
  //       }, {
  //         label: "2nd Quebec Cup",
  //         fill: false,
  //         // backgroundColor: "rgba(149,205,62,0.2)",
  //         borderColor: "rgba(149,205,62,1)",
  //         pointBorderColor: "#fff",
  //         pointBackgroundColor: "rgba(149,205,62,1)",
  //         pointBorderColor: "#fff",
  //         pointHitRadius: 20,
  //         data: [90.76, 91.23, 50, 98.12, 89.63, 90.50]
  //       }, {
  //         label: "3rd Quebec Cup",
  //         fill: false,
  //         // backgroundColor: "rgba(62,149,205,0.2)",
  //         borderColor: "rgba(62,149,205,1)",
  //         pointBorderColor: "#fff",
  //         pointBackgroundColor: "rgba(62,149,205,1)",
  //         pointBorderColor: "#fff",
  //         pointHitRadius: 20,
  //         data: [92.56, 93.13, 80.23, 96.34, 91.45, 90.29]
  //       }
  //     ]
  //   },
  //   options: {
  //     legend: {
  //       position: "bottom"
  //     },
  //     title: {
  //       display: true,
  //       text: 'Distribution in % of apparatus'
  //     },
  //     scale: {
  //       ticks: {
  //         min: 50,
  //         suggestedMax: 100,
  //         padding: 20,
  //         fontColor: "rgba(0,0,0,0.5)",
  //         fontStyle: "bold"
  //       }
  //     }
  //   }
  // });