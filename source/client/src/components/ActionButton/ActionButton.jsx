import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import styles from "./ActionButton.module.scss";

function Button({ icon, label, type }) {
  const className = type === "secondary" ? styles.secondary : styles.primary;
  return (
    <button className={className}>
      {icon && (
        <span className={styles.icon}>
          <FontAwesomeIcon icon={icon} size="lg" />
        </span>
      )}
      <span>{label}</span>
    </button>
  );
}

export { Button };
