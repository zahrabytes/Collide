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

const BarChart = ({ topicsMatch }) => {
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

  const likeScore = Object.values(topicsMatch).map((score) =>
    score > 0 ? score : 0
  );
  const dislikeScore = Object.values(topicsMatch).map((score) =>
    score < 0 ? score : 0
  );

  const data = {
    labels: Object.keys(topicsMatch),
    datasets: [
      {
        label: "Like Score",
        data: likeScore,
        backgroundColor: "rgba(54, 162, 235, 0.75)",
      },
      {
        label: "Dislike Score",
        data: dislikeScore,
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
