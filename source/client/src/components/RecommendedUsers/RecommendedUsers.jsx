import { useFetchUsers } from "../../hooks/useFetchUsers";
import styles from "./RecommendedUsers.module.scss";

function UserCard({ user }) {
  return (
    <div className={styles.userCard}>
      <img
        className={styles.avatar}
        src={user.picture.thumbnail}
        alt="Avatar"
      />
      <div className={styles.right}>
        <div>
          <p className={styles.name}>
            {user.name.first} {user.name.last}
          </p>
          <p className={styles.username}>@{user.login.username}</p>
        </div>
        <button className={styles.follow}>Follow</button>
      </div>
    </div>
  );
}

function RecommendedUsers() {
  const users = useFetchUsers(8);
  return (
    <div className={styles.container}>
      <h2 className={styles.h2}>Recommended Users</h2>
      <div className={styles.users}>
        {users.map((user, index) => (
          <UserCard user={user} key={index} />
        ))}
      </div>
      <a className={styles.link} href="#">
        Show More
      </a>
    </div>
  );
}

export { RecommendedUsers };
