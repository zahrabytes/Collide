import {
  faArrowUpFromBracket,
  faBolt,
  faComment,
  faEllipsis,
  faShare,
  faThumbsDown,
  faThumbsUp,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useUser } from "../../hooks/useUser";
import { Button } from "../ActionButton/ActionButton";
import styles from "./Post.module.scss";

const formatDate = (dateString) => {
  const replaceSecondOccurrence = (str, substr, replacement) => {
    let parts = str.split(substr);
    if (parts.length > 2)
      return parts[0] + substr + parts.slice(1).join(replacement);
    return str;
  };

  const options = {
    year: "numeric",
    month: "short", // "MMM"
    day: "2-digit", // "DD"
    hour: "numeric",
    minute: "2-digit",
    hour12: true, // Use 12-hour format with AM/PM
  };

  const date = new Date(dateString);
  const almostFormatted = date.toLocaleString("en-US", options);
  const formattedDate = replaceSecondOccurrence(almostFormatted, ",", " at");

  return formattedDate;
};

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

function Post({ post }) {
  const authorUserId = post.payload.authorable_id;
  const author = useUser(authorUserId);
  const formattedDate = formatDate(post.payload.created_at);
  return (
    <div className={styles.post}>
      <section className={styles.topLeft}>
        <img
          className={styles.avatar}
          src={author.profile_picture}
          alt="Avatar"
        />
      </section>
      <section className={styles.topRight}>
        <div className={styles.topRow}>
          <div className={styles.user}>
            <h3 className={styles.name}>{author.name}</h3>
          </div>
          <FontAwesomeIcon
            className={styles.ellipsis}
            icon={faEllipsis}
            size="lg"
          />
        </div>
        <p className={styles.time}>{formattedDate}</p>
      </section>
      <section className={styles.bottomRight}>
        <div className={styles.content}>
          <h2 className={styles.title}>{post.payload.title}</h2>
          <p className={styles.body}>{post.payload.plain_text_body}</p>
        </div>
        <PlaceholderImage />
        <div className={styles.stats}>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.red}`}>
              <FontAwesomeIcon icon={faBolt} />
            </div>
            <p className={styles.statNumber}>1</p>
          </div>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.green}`}>
              <FontAwesomeIcon icon={faComment} />
            </div>
            <p className={styles.statNumber}>2</p>
          </div>
          <div className={styles.stat}>
            <div className={`${styles.iconContainer} ${styles.blue}`}>
              <FontAwesomeIcon icon={faShare} />
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
