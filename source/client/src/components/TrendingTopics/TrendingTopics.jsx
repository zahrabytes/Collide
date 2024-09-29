import styles from "./TrendingTopics.module.scss";

function TrendingTopics({ trendingTopics }) {
  return (
    <div className={styles.container}>
      <h2 className={styles.h2}>Trending Topics</h2>
      {!trendingTopics.length ? null : (
        <div className={styles.topics}>
          {trendingTopics.map((topic, index) => (
            <div className={styles.topic} key={index}>
              {topic}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export { TrendingTopics };
