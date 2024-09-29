import { Post } from "../Post/Post";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircleQuestion } from "@fortawesome/free-solid-svg-icons";
import { faComments } from "@fortawesome/free-solid-svg-icons";
import { faSquarePollVertical } from "@fortawesome/free-solid-svg-icons";
import { faNewspaper } from "@fortawesome/free-solid-svg-icons";
import styles from "./Posts.module.scss";

import { useEffect, useState } from "react";

function Posts() {
  const [posts, setPosts] = useState([]);
  const endpoint = "http://127.0.0.1:5000/users/1/recommendedPosts";

  useEffect(() => {
    fetch(endpoint)
      .then((response) => response.json())
      .then((data) => data.posts)
      .then((posts) => setPosts(posts));
  }, []);

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
      {posts.map((post, index) => (
        <Post post={post} key={index} />
      ))}
    </>
  );
}

export { Posts };
