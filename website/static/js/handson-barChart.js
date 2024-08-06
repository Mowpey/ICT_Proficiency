(function () {
  const handson_BarChart = document.getElementById("handsonBarChart");
  Chart.register(ChartDataLabels);

  let myChart;

  const updateBarChart = (labels, data) => {
    const total = data.reduce((acc, val) => acc + val, 0);
    const percentages = data.map((value) => ((value / total) * 100).toFixed(0));

    const chartData = {
      labels: labels,
      datasets: [
        {
          label: "Top Performing Regions",
          data: percentages,
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(255, 205, 86, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(54, 162, 235, 0.2)",
          ],
          borderColor: [
            "rgb(255, 99, 132)",
            "rgb(255, 159, 64)",
            "rgb(255, 205, 86)",
            "rgb(75, 192, 192)",
            "rgb(54, 162, 235)",
          ],
          borderWidth: 1,
        },
      ],
    };

    const config = {
      type: "bar",
      data: chartData,
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: function (value) {
                return value + "%";
              },
              font: {
                weight: 'bold'
              }
            },
          },
          x: {
            ticks: {
              font: {
                weight: 'bold'
              }
            }
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function (context) {
                return context.parsed.y.toFixed(0) + "%";
              },
            },
          },
          datalabels: {
            formatter: (value) => {
              return value + "%";
            },
            color: "#000",
            anchor: "end",
            align: "center",
          },
        },
      },
    };

    if (!myChart) {
      myChart = new Chart(handson_BarChart, config);
    } else {
      myChart.data = chartData;
      myChart.update();
    }
  };

  var passersList = document.querySelectorAll('li[data-province]');
  var passersData = [];
  
  Array.from(passersList).forEach(function (passer) {
    var province = passer.getAttribute('data-province');
    var count = parseInt(passer.getAttribute('data-count'));
    passersData.push({ province: province, count: count });
  });
  
  const labels = passersData.map(function (passer) {
    return passer.province.charAt(0).toUpperCase() + passer.province.slice(1);
  });
  const rawData = passersData.map(function (passer) {
    return passer.count;
  });
  updateBarChart(labels, rawData);
})();
