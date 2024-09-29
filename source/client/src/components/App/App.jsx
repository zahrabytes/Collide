import { Header } from "../Header/Header";
import { Profile } from "../Profile/Profile";
import { TrendingTopics } from "../TrendingTopics/TrendingTopics";
import { RecommendedUsers } from "../RecommendedUsers/RecommendedUsers";
import { CenterColumn } from "../CenterColumn/CenterColumn";
import { useTrendingTopics } from "../../hooks/useTrendingTopics";
import { UserCard } from "../Admin/UserCard/UserCard";
import { useFetchAllUsers } from "../../hooks/useFetchAllUsers"; // Import the custom hook
import styles from "./App.module.scss";

function isNumberOrEmpty(variable) {
  return typeof variable === "number" || variable === "";
}

function App() {
  const path = window.location.pathname;
  const userId = path.split("/")[1];

  const { users, loading, error } = useFetchAllUsers();
  const trendingTopics = useTrendingTopics();

  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <Header />
        {isNumberOrEmpty(userId) && (
          <div className={styles.gridContainer}>
            {isNumberOrEmpty(userId) && loading && (
              <div className={styles.loading}>Loading users...</div>
            )}
            {isNumberOrEmpty(userId) &&
              !loading &&
              Array.isArray(users) &&
              users.map((user) => <UserCard key={user.id} user={user} />)}
            {error && <div className={styles.error}>Error: {error}</div>}
          </div>
        )}
        {!isNumberOrEmpty(userId) && (
          <>
            <div className={styles.divider}></div>
            <main className={styles.main}>
              <aside className={styles.left}>
                <Profile userId={userId} />
                <RecommendedUsers userId={userId} />
              </aside>
              <CenterColumn {...{ userId, trendingTopics }} />
              <section className={styles.right}>
                <TrendingTopics trendingTopics={trendingTopics} />
              </section>
            </main>
          </>
        )}
      </div>
    </div>
  );
}

export { App };
