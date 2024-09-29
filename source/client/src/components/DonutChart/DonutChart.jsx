import { Doughnut } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Title, Tooltip, Legend } from "chart.js";

const DonutChart = ({ interests }) => {
  ChartJS.register(ArcElement, Tooltip, Legend, Title);

  const data = {
    labels: Object.keys(interests),
    datasets: [
      {
        label: "Score",
        data: Object.values(interests),
        backgroundColor: [
          "rgba(255, 99, 132, 0.75)",
          "rgba(255, 159, 64, 0.75)",
          "rgba(75, 192, 192, 0.75)",
          "rgba(54, 162, 235, 0.75)",
          "rgba(153, 102, 255, 0.75)",
        ],
        borderColor: [
          "rgba(255, 99, 132, 1)",
          "rgba(255, 159, 64, 1)",
          "rgba(75, 192, 192, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(153, 102, 255, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: { display: false },
    },
  };

  return <Doughnut data={data} options={options} />;
};

export { DonutChart };
