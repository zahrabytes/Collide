import { useUsers } from "../../hooks/useUsers"; // Import the custom hook
import { CenterColumn } from "../CenterColumn/CenterColumn";
import { Header } from "../Header/Header";
import { Profile } from "../Profile/Profile";
import { RecommendedUsers } from "../RecommendedUsers/RecommendedUsers";
import { TrendingTopics } from "../TrendingTopics/TrendingTopics";
import { UserCard } from "../UserCard/UserCard";

import styles from "../App/App.module.scss";

function Admin() {
  const { users, loading, error } = useUsers(); // Fetch users, loading, and error

  const path = window.location.pathname;
  const userId = path.split("/")[1];

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <Header />
        <div className={styles.gridContainer}>
          {loading && <div className={styles.loading}>Loading users...</div>}

          {!loading &&
            Array.isArray(users) &&
            users.map((user) => <UserCard key={user.id} user={user} />)}

          {error && <div className={styles.error}>Error: {error}</div>}
        </div>
        <div className={styles.divider}></div>
        <main className={styles.main}>
          <aside className={styles.left}>
            <Profile userId={userId} />
            <RecommendedUsers />
          </aside>
          <CenterColumn userId={userId} />
          <section className={styles.right}>
            <TrendingTopics />
          </section>
        </main>
      </div>
    </div>
  );
}

export { Admin };
