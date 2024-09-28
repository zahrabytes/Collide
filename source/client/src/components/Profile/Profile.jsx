import styles from "./Profile.module.scss";

function Profile() {
  return (
    <div className={styles.profile}>
      <img
        className={styles.background}
        src="https://picsum.photos/720/340"
        alt=""
      />
      <div className={styles.avatarContainer}>
        <img
          className={styles.avatar}
          src="https://xsgames.co/randomusers/avatar.php?g=male"
          alt=""
        />
      </div>
      <div className={styles.info}>
        <h2 className={styles.name}>Yeremias NJ</h2>
        <h3 className={styles.username}>@notojoyoo</h3>
        <p className={styles.bio}>
          Lorem ipsum dolor sit amet, con secte tur adi piscing ✨
        </p>
      </div>
      <div className={styles.stats}>
        <div className={styles.stat}>
          <h4 className={styles.number}>572</h4>
          <p className={styles.label}>Following</p>
        </div>
        <div className={styles.divider}></div>
        <div className={styles.stat}>
          <h4 className={styles.number}>837</h4>
          <p className={styles.label}> Followers</p>
        </div>
      </div>
      <p className={styles.bottom}>
        <a className={styles.link} href="#">
          My Profile
        </a>
      </p>
    </div>
  );
}

export { Profile };
