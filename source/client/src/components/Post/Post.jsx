import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEllipsis } from "@fortawesome/free-solid-svg-icons";
import { faBolt } from "@fortawesome/free-solid-svg-icons";
import { faComment } from "@fortawesome/free-solid-svg-icons";
import { faShare } from "@fortawesome/free-solid-svg-icons";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";
import { faThumbsDown } from "@fortawesome/free-solid-svg-icons";
import { faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import { Button } from "../ActionButton/ActionButton";
import styles from "./Post.module.scss";

function PlaceholderImage() {
  const width = 1250 + Math.floor(Math.random() * 500 - 500);
  const height = 500 + Math.floor(Math.random() * 250 - 150);
  return Math.random() > 0.5 ? (
    <img
      className={styles.postImage}
      src={`https://picsum.photos/${width}/${height}`}
      alt="Post"
    />
  ) : null;
}

function Post({ user }) {
  const lorem =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse lorem risus, congue sollicitudin mi vel, aliquam viverra eros. In finibus volutpat lobortis. Sed mollis, massa vitae feugiat porta, leo urna lacinia dolor, sit amet gravida eros mi vitae neque. Praesent consectetur, odio id fringilla dictum, turpis ipsum auctor est, ac aliquam elit tortor vel nulla. Nulla facilisi. Sed libero lacus, sagittis eu neque quis, blandit finibus est. Sed posuere, mauris rhoncus rutrum porttitor, nisi nulla vestibulum ante, a auctor purus erat et justo.";
  const paragraph = lorem.slice(0, Math.floor(Math.random() * lorem.length));
  return (
    <div className={styles.post}>
      <section className={styles.topLeft}>
        <img
          className={styles.avatar}
          src={user.picture.thumbnail}
          alt="Avatar"
        />
      </section>
      <section className={styles.topRight}>
        <div className={styles.topRow}>
          <div className={styles.user}>
            <h3 className={styles.name}>
              {user.name.first} {user.name.last}
            </h3>
            <h4 className={styles.username}>@{user.login.username}</h4>
          </div>
          <FontAwesomeIcon
            className={styles.ellipsis}
            icon={faEllipsis}
            size="lg"
          />
        </div>
        <p className={styles.time}>Few minutes ago</p>
      </section>
      <section className={styles.bottomRight}>
        <p className={styles.content}>
          <h2 className={styles.title}>Post Title</h2>
          <p className={styles.body}> {paragraph}</p>
        </p>
        <PlaceholderImage />
        <div className={styles.stats}>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.red}`}>
              <FontAwesomeIcon icon={faBolt} size="s" />
            </div>
            <p className={styles.statNumber}>1</p>
          </div>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.green}`}>
              <FontAwesomeIcon icon={faComment} size="s" />
            </div>
            <p className={styles.statNumber}>2</p>
          </div>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.blue}`}>
              <FontAwesomeIcon icon={faShare} size="s" />
            </div>
            <p className={styles.statNumber}>3</p>
          </div>
        </div>
        <div className={styles.actions}>
          <Button icon={faThumbsUp} label="Like" />
          <Button icon={faThumbsDown} label="Dislike" />
          <Button icon={faComment} label="Comment" />
          <Button icon={faArrowUpFromBracket} type="secondary" />
        </div>
      </section>
    </div>
  );
}

export { Post };
