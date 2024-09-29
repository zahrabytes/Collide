import { Post } from "../Post/Post";
import { useFetchUsers } from "../../hooks/useFetchUsers";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleQuestion } from "@fortawesome/free-solid-svg-icons";
import { faComments } from "@fortawesome/free-solid-svg-icons";
import { faSquarePollVertical } from "@fortawesome/free-solid-svg-icons";
import { faNewspaper } from "@fortawesome/free-solid-svg-icons";
import styles from "./Posts.module.scss";

function Posts() {
  const users = useFetchUsers(10);
  return (
    <>
      <div className={styles.create}>
        <img
          className={styles.avatar}
          src="https://xsgames.co/randomusers/avatar.php?g=male"
          alt=""
        />
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
      {users.map((user, index) => (
        <Post user={user} key={index} />
      ))}
    </>
  );
}

export { Posts };
