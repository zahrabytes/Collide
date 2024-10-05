import React from "react";
import styles from "./Loading.module.scss";

const Loading = () => {
  return (
    <div className={styles.tetrominos}>
      <div className={`${styles.tetromino} ${styles.box1}`}></div>
      <div className={`${styles.tetromino} ${styles.box2}`}></div>
      <div className={`${styles.tetromino} ${styles.box3}`}></div>
      <div className={`${styles.tetromino} ${styles.box4}`}></div>
    </div>
  );
};

export default Loading;
