import { Header } from "../Header/Header";
import { Posts } from "../Posts/Posts";
import { Profile } from "../Profile/Profile";
import { TrendingTopics } from "../TrendingTopics/TrendingTopics";
import { RecommendedUsers } from "../RecommendedUsers/RecommendedUsers";
import styles from "./App.module.scss";
import { UserCard } from '../UserCard/UserCard';
import data from '../../assets/users.json'; // Corrected import path

const users = data.users;
console.log(users);

function App() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <Header />
        <div className={styles.gridContainer}>
          {Array.isArray(users) && users.map(user => (
            <UserCard key={user.id} user={user} />
          ))}
        </div>
        <div className={styles.divider}></div>
        <main className={styles.main}>
          <aside className={styles.left}>
            <Profile />
            <RecommendedUsers />
          </aside>
          <Posts />
          <section className={styles.right}>
            <TrendingTopics />
          </section>
        </main>
      </div>
    </div>
  );
}

export { App };
