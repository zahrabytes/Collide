import { useUser } from "../../hooks/useUser";
import styles from "./Profile.module.scss";

function Profile({ userId }) {
  const user = useUser(userId);
  return (
    <div className={styles.profile}>
      <img
        className={styles.background}
        src="https://picsum.photos/1080/400"
        alt=""
      />
      <div className={styles.avatarContainer}>
        <img className={styles.avatar} src={user.profile_picture} alt="" />
      </div>
      <div className={styles.info}>
        <h2 className={styles.name}>{user.name}</h2>
        <h3 className={styles.username}>@{user.username}</h3>
        {user.biography && <p className={styles.bio}>{user.biography}</p>}
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
          View Profile
        </a>
      </p>
    </div>
  );
}

export { Profile };
