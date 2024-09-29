import styles from "./Summary.module.scss";

function Summary({ summary }) {
  return (
    <>
      <div className={styles.container}>
        <h2 className={styles.h2}>Summary</h2>
        <p className={styles.body}>{summary.summary}</p>
      </div>
      <div className={styles.container}>
        <h2 className={styles.h2}>Overall Attitude</h2>
        <p className={styles.body}>{summary.overall_attitude}</p>
      </div>
      <div className={styles.container}>
        <h2 className={styles.h2}>Likely Engagement</h2>
        <p className={styles.body}>{summary.likely_engagement}</p>
      </div>
    </>
  );
}

export { Summary };
