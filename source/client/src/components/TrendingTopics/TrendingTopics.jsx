import styles from "./TrendingTopics.module.scss";

function TrendingTopics() {
  const topics = [
    "AI",
    "Oil",
    "Upstream",
    "Production",
    "Operator",
    "Software",
    "Drilling",
    "Engineering",
    "Data",
    "Rig",
    "Revenue",
    "Geology",
    "Geophysics",
    "Reservoir",
    "Petrophysics",
    "Seismic",
    "Renewable",
    "Energy",
    "Gas",
    "Solar",
  ];
  return (
    <div className={styles.container}>
      <h2 className={styles.h2}>Trending Topics</h2>
      <div className={styles.topics}>
        {topics.map((topic, index) => (
          <div className={styles.topic} key={index}>
            {topic}
          </div>
        ))}
      </div>
    </div>
  );
}

export { TrendingTopics };
