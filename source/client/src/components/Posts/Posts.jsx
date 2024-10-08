import {
  faCircleQuestion,
  faComments,
  faNewspaper,
  faSquarePollVertical,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Post } from "../Post/Post";
import styles from "./Posts.module.scss";

function Posts({ posts, user }) {
  return (
    <>
      <div className={styles.create}>
        <img className={styles.avatar} src={user.profile_picture} alt="" />
        <div className={styles.right}>
          <input
            className={styles.input}
            type="text"
            placeholder="What's happening?"
          />
          <textarea
            className={styles.textarea}
            placeholder="Add more detail..."
          ></textarea>
          <div className={styles.postType}>
            <FontAwesomeIcon
              className={styles.greenIcon}
              icon={faCircleQuestion}
            ></FontAwesomeIcon>
            <span className={styles.label}>Ask</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon
              className={styles.blueIcon}
              icon={faComments}
            ></FontAwesomeIcon>
            <span className={styles.label}>Discuss</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon
              className={styles.redIcon}
              icon={faSquarePollVertical}
            ></FontAwesomeIcon>
            <span className={styles.label}>Poll</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon
              className={styles.orangeIcon}
              icon={faNewspaper}
            ></FontAwesomeIcon>
            <span className={styles.label}>Blog</span>
          </div>
        </div>
      </div>
      {posts.map((post, index) => (
        <Post post={post} key={index} />
      ))}
    </>
  );
}

export { Posts };
