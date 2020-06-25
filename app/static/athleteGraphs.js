// Chart.defaults.global.animationSteps = 50;
Chart.defaults.global.tooltipYPadding = 16;
Chart.defaults.global.tooltipCornerRadius = 0;
Chart.defaults.global.tooltipTitleFontStyle = "normal";
Chart.defaults.global.tooltipFillColor = "rgba(0,0,0,0.8)";
// Chart.defaults.global.animationEasing = "easeOutBounce";
// Chart.defaults.global.responsive = false;
// Chart.defaults.global.scaleLineColor = "black";
// Chart.defaults.global.scaleFontSize = 16;


new Chart($('#myLineChart'), {
  type: 'line',
  data: {
    labels: [
      '1st Quebec Cup',
      '2nd Quebec cup',
      '3rd Quebec Cup',
      'final Quebec Cup',
      'Canadian championship'
    ],
    datasets: [{
      //   data: [65.34, 66.76, 67.12, 67.15, 68.98],
      //   label: "Results",
      //   borderColor: "#3e95cd",
      //   fill: false
      // }, {
      //   data: [66.50, 67, 67.50, 68, 68.50],
      //   label: "Target",
      //   borderColor: "#c45850",
      //   fill: false
        data: [91.23, 95.12, 85.45, 89.12, 91.56],
        label: "Target",
        borderColor: "#c45850",
        fill: false,
        pointHitRadius: 20
      }
    ]
  },
  options: {
    legend: {
      position: "bottom",
      display: false
    },
    title: {
      display: true,
      text: "target VS results"
    },
    scales: {
      yAxes: [{
        ticks: {
          suggestedMin: 70,
          suggestedMax: 100,
          padding: 20,
          fontColor: "rgba(0,0,0,0.5)",
          fontStyle: "bold"
        },
        scaleLabel: {
          display: true,
          labelString: '% of the target'
        }

      }],
      xAxes: [{
        gridLines: {
          // drawTicks: false,
          // display: false,
          // zeroLineColor: "transparent"
        },
        ticks: {
          padding: 20,
          fontColor: "rgba(0,0,0,0.5)",
          fontStyle: "bold"
        }
      }]
    },
    annotation: {
      annotations: [{
        type: 'line',
        mode: 'horizontal',
        scaleID: 'y-axis-0',
        value: 90,  // data-value at which the line is drawn
        borderWidth: 2,
        borderColor: 'black',
        // label: {
        //   enabled: true,
        //   content: 'Test label'
        // }
      }]
    }
  }
});


new Chart(document.getElementById('myRadarChart'), {
  type: 'radar',
  data: {
    labels: ['FX', 'PH', 'SR', 'VT', 'PB', 'HB'],
    datasets: [
      {
        label: "1st Quebec Cub",
        fill: false,
        // backgroundColor: "rgba(205,62,149,0.2)",
        borderColor: "rgba(205,62,149,1)",
        pointBorderColor: "#fff",
        pointBackgroundColor: "rgba(205,62,149,1)",
        pointHitRadius: 20,
        data: [91.12, 90.23, 82.34, 95.12, 90.21, 89.42]
      }, {
        label: "2nd Quebec Cup",
        fill: false,
        // backgroundColor: "rgba(149,205,62,0.2)",
        borderColor: "rgba(149,205,62,1)",
        pointBorderColor: "#fff",
        pointBackgroundColor: "rgba(149,205,62,1)",
        pointBorderColor: "#fff",
        pointHitRadius: 20,
        data: [90.76, 91.23, 83.12, 98.12, 89.63, 90.50]
      }, {
        label: "3rd Quebec Cup",
        fill: false,
        // backgroundColor: "rgba(62,149,205,0.2)",
        borderColor: "rgba(62,149,205,1)",
        pointBorderColor: "#fff",
        pointBackgroundColor: "rgba(62,149,205,1)",
        pointBorderColor: "#fff",
        pointHitRadius: 20,
        data: [92.56, 93.13, 80.23, 96.34, 91.45, 90.29]
      }
    ]
  },
  options: {
    legend: {
      position: "bottom"
    },
    title: {
      display: true,
      text: 'Distribution in % of apparatus'
    },
    scale: {
      ticks: {
        suggestedMin: 70,
        suggestedMax: 100,
        padding: 20,
        fontColor: "rgba(0,0,0,0.5)",
        fontStyle: "bold"
      }
    }
  }
});