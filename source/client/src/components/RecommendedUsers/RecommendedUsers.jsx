import { useState } from "react";
import { useRecommendedUsers } from "../../hooks/useRecommendedUsers";
import { useUser } from "../../hooks/useUser";
import styles from "./RecommendedUsers.module.scss";

function UserCard({ userId }) {
  const user = useUser(userId);
  return (
    <div className={styles.userCard}>
      <img className={styles.avatar} src={user.profile_picture} alt="Avatar" />
      <div className={styles.right}>
        <div>
          <p className={styles.name}>{user.name}</p>
          <p className={styles.username}>@{user.username}</p>
        </div>
        <button className={styles.follow}>Follow</button>
      </div>
    </div>
  );
}

function RecommendedUsers({ userId }) {
  const users = useRecommendedUsers(userId);
  const firstEightUsers = users.slice(0, 8);

  const [showMore, setShowMore] = useState(false);
  const shownUsers = showMore ? users : firstEightUsers;

  return (
    <div className={styles.container}>
      <h2 className={styles.h2}>Recommended Users</h2>
      <div className={styles.users}>
        {shownUsers.map((user, index) => (
          <UserCard userId={user.id} key={index} />
        ))}
      </div>
      <button
        className={styles.showMore}
        onClick={() => setShowMore(!showMore)}
      >
        {showMore ? "Show Less" : `Show More`}
      </button>
    </div>
  );
}

export { RecommendedUsers };
