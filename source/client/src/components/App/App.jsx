import { Header } from "../Header/Header";
import { Profile } from "../Profile/Profile";
import { TrendingTopics } from "../TrendingTopics/TrendingTopics";
import { RecommendedUsers } from "../RecommendedUsers/RecommendedUsers";

import styles from "./App.module.scss";
import { CenterColumn } from "../CenterColumn/CenterColumn";

function App() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <Header />
        <div className={styles.divider}></div>
        <main className={styles.main}>
          <aside className={styles.left}>
            <Profile />
            <RecommendedUsers />
          </aside>
          <CenterColumn />
          <section className={styles.right}>
            <TrendingTopics />
          </section>
        </main>
      </div>
    </div>
  );
}

export { App };
