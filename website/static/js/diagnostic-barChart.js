(function () {
  const diagnostic_BarChart = document.getElementById("diagnosticBarChart");

  Chart.register(ChartDataLabels);

  const labels = ["Cagayan", "Isabela", "Batanes", "Nueva Vizcaya", "Quirino"];
  const rawData = [65, 59, 80, 81, 56];

  const total = rawData.reduce((acc, val) => acc + val, 0);
  const percentages = rawData.map((value) =>
    ((value / total) * 100).toFixed(2)
  );

  const data = {
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
    data: data,
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
          },
        },
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: function (context) {
              return context.parsed.y.toFixed(2) + "%";
            },
          },
        },
      },
      datalabels: {
        formatter: (value) => {
          return value + "%";
        },
        color: "#000",
        anchor: "end",
        align: "top",
      },
    },
  };

  new Chart(diagnostic_BarChart, config);
})();
