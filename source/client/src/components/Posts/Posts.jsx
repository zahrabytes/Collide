import { Post } from "../Post/Post";
import { useFetchUsers } from "../../hooks/useFetchUsers";
import styles from "./Posts.module.scss";

function Posts() {
  const users = useFetchUsers(5);
  return (
    <section className={styles.posts}>
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
