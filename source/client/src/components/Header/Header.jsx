import styles from "./Header.module.scss";
import logo from "../../assets/logo.svg";

function Header() {
  return (
    <header className={styles.header}>
      <section className={styles.left}>
        <img className={styles.logo} src={logo} alt="Logo" />
        <input
          className={styles.search}
          type="text"
          placeholder="Ask questions about energy or search Collide"
        />
      </section>
      <section className={styles.right}>Todo</section>
    </header>
  );
}

export { Header };
