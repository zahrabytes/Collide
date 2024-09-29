import { useState, useEffect } from "react";
import styles from "./TrendingTopics.module.scss";

function TrendingTopics() {
  const [topics, setTopics] = useState([]);
  const endpoint = "http://127.0.0.1:5000/trendingTopics";

  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((data) => setTopics(data));
  }, []);

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
