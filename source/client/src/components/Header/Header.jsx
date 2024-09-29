import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faHome,
  faBriefcase,
  faRocket,
  faUsers,
  faInbox,
  faBell,
  faCaretDown,
  faSearch,
} from "@fortawesome/free-solid-svg-icons";
import styles from "./Header.module.scss";
import logo from "../../assets/logo.svg";

function Header() {
  return (
    <header className={styles.header}>
      <section className={styles.left}>
        <a href="/">
          <img className={styles.logo} src={logo} alt="Logo" />
        </a>
        <div className={styles.searchContainer}>
          <FontAwesomeIcon className={styles.searchIcon} icon={faSearch} />
          <input
            className={styles.search}
            type="text"
            placeholder="Ask questions about energy or search Collide"
          />
        </div>
      </section>
      <nav className={styles.nav}>
        <div className={`${styles.navAction} ${styles.selected}`}>
          <FontAwesomeIcon className={styles.icon} icon={faHome} />
          <span className={styles.label}>Feed</span>
        </div>
        <div className={styles.navAction}>
          <FontAwesomeIcon className={styles.icon} icon={faBriefcase} />
          <span className={styles.label}>Resources</span>
        </div>
        <div className={styles.navAction}>
          <FontAwesomeIcon className={styles.icon} icon={faRocket} />
          <span className={styles.label}>CollideGPT</span>
        </div>
        <div className={styles.navAction}>
          <FontAwesomeIcon className={styles.icon} icon={faUsers} />
          <span className={styles.label}>Jobs</span>
        </div>
        <div className={styles.navAction}>
          <FontAwesomeIcon className={styles.icon} icon={faInbox} />
          <span className={styles.label}>Chat</span>
        </div>
        <div className={styles.navAction}>
          <FontAwesomeIcon className={styles.icon} icon={faBell} />
          <span className={styles.label}>Notifications</span>
        </div>
        <div className={styles.profile}>
          <img
            className={styles.avatar}
            src="https://xsgames.co/randomusers/avatar.php?g=female"
            alt="Avatar"
          />
          <span className={styles.name}>Admin</span>
          <FontAwesomeIcon className={styles.caret} icon={faCaretDown} />
        </div>
      </nav>
    </header>
  );
}

export { Header };
