import { BarChart } from "../BarChart/BarChart";
import { DonutChart } from "../DonutChart/DonutChart";
import { LineChart } from "../LineChart/LineChart";

import styles from "./Analytics.module.scss";

function Analytics({ analytics }) {
  const { topicsMatch, interests } = analytics;

  return (
    <>
      <div className={styles.barContainer}>
        <h2 className={styles.h2}>Trending Topics Match</h2>
        <BarChart topicsMatch={topicsMatch} />
      </div>
      <div className={styles.donutContainer}>
        <h2 className={styles.h2}>Favorite Topics</h2>
        <div className={styles.donutWrapper}>
          <DonutChart interests={interests} />
        </div>
      </div>
      <div className={styles.lineContainer}>
        <h2 className={styles.h2}>Engagement Over Time</h2>
        <LineChart />
      </div>
    </>
  );
}

export { Analytics };
