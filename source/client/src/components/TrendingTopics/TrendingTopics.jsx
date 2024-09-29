import { useTrendingTopics } from "../../hooks/useTrendingTopics";
import styles from "./TrendingTopics.module.scss";

function TrendingTopics() {
  const topics = useTrendingTopics();
  return (
    <div className={styles.container}>
      <h2 className={styles.h2}>Trending Topics</h2>
      {!topics.length ? null : (
        <div className={styles.topics}>
          {topics.map((topic, index) => (
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
