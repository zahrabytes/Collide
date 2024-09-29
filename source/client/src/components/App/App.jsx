import { Header } from "../Header/Header";
import { Profile } from "../Profile/Profile";
import { TrendingTopics } from "../TrendingTopics/TrendingTopics";
import { RecommendedUsers } from "../RecommendedUsers/RecommendedUsers";
import { CenterColumn } from "../CenterColumn/CenterColumn";
import styles from "./App.module.scss";

function App() {
  const path = window.location.pathname;
  const userId = path.split("/")[1];
  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <Header />
        <div className={styles.divider}></div>
        <main className={styles.main}>
          <aside className={styles.left}>
            <Profile userId={userId} />
            <RecommendedUsers userId={userId} />
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

export { App };
