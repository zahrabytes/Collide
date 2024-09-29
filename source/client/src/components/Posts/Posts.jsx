import { Post } from "../Post/Post";
import { useFetchUsers } from "../../hooks/useFetchUsers";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleQuestion } from "@fortawesome/free-solid-svg-icons";
import { faComments } from "@fortawesome/free-solid-svg-icons";
import { faSquarePollVertical } from "@fortawesome/free-solid-svg-icons";
import { faNewspaper } from "@fortawesome/free-solid-svg-icons";
import styles from "./Posts.module.scss";

function Posts() {
  const users = useFetchUsers(5);
  return (
    <section className={styles.posts}>
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
            <FontAwesomeIcon className={styles.green} icon={faCircleQuestion} />
            <span className={styles.label}>Ask</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon className={styles.blue} icon={faComments} />
            <span className={styles.label}>Discuss</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon
              className={styles.red}
              icon={faSquarePollVertical}
            />
            <span className={styles.label}>Poll</span>
          </div>
          <div className={styles.postType}>
            <FontAwesomeIcon className={styles.orange} icon={faNewspaper} />
            <span className={styles.label}>Blog</span>
          </div>
        </div>
      </div>
      <div className={styles.chips}>
        <div className={styles.green}>For You</div>
        <div className={styles.blue}>Trending</div>
        <div className={styles.orange}>Latest</div>
      </div>
      {/* <div className={styles.divider}></div> */}
      {users.map((user, index) => (
        <Post user={user} key={index} />
      ))}
    </section>
  );
}

export { Posts };
