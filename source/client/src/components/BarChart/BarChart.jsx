import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
} from "chart.js";

const BarChart = () => {
  ChartJS.register(
    CategoryScale,
    LinearScale,
    RadialLinearScale,
    PointElement,
    BarElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

  const data = {
    labels: [
      "Topic 1",
      "Topic 2",
      "Topic 3",
      "Topic 4",
      "Topic 4",
      "Topic 6",
      "Topic 7",
      "Topic 8",
      "Topic 9",
      "Topic 0",
    ],
    datasets: [
      {
        label: "Like Score",
        data: [0, 0.75, 0, 0, 0.5, 0, 0.2, 0, 1, 0],
        backgroundColor: "rgba(54, 162, 235, 0.75)",
      },
      {
        label: "Dislike Score",
        data: [-1, 0, -0.5, -0.25, 0, -0.66, 0, -0.33, 0, -0.5],
        backgroundColor: "rgba(255, 99, 132, 0.75)",
      },
    ],
  };

  const options = {
    indexAxis: "y",
    scales: {
      x: { stacked: true },
      y: { stacked: true },
    },
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: false },
    },
  };

  return <Bar data={data} options={options} />;
};

export { BarChart };
