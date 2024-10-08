import {
  faBriefcase,
  faBuilding,
  faCalendarAlt,
  faMapMarkerAlt,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import styles from "./UserCard.module.scss";

function UserCard({ user }) {
  const handleCardClick = () => (window.location.href = `/${user.id}`);

  return (
    <div className={styles["profile-card"]} onClick={handleCardClick}>
      <div className={styles["profile-header"]}>
        <img
          className={styles["profile-pic"]}
          src={user.profile_picture}
          alt={user.name}
        />
        <div className={styles["profile-info"]}>
          {user.prefix && (
            <h3>
              {user.prefix} {user.name}
            </h3>
          )}
          {!user.prefix && <h3>{user.name}</h3>}
          {user.biography && <p className={styles["bio"]}>{user.biography}</p>}
          {user.company && (
            <p>
              <FontAwesomeIcon icon={faBuilding} className={styles["icon"]} />{" "}
              {user.company}
            </p>
          )}
          {user.department && (
            <p>
              <FontAwesomeIcon icon={faBriefcase} className={styles["icon"]} />{" "}
              {user.department}
            </p>
          )}
          {user.seniority && (
            <p>
              <FontAwesomeIcon icon={faBriefcase} className={styles["icon"]} />{" "}
              {user.seniority}
            </p>
          )}
          {(user.city || user.state) && (
            <p>
              <FontAwesomeIcon
                icon={faMapMarkerAlt}
                className={styles["icon"]}
              />{" "}
              {user.city}, {user.state}
            </p>
          )}
          {user.role_location && (
            <p>
              <FontAwesomeIcon
                icon={faMapMarkerAlt}
                className={styles["icon"]}
              />{" "}
              {user.role_location}
            </p>
          )}
          {user.role_start_at && (
            <p>
              <FontAwesomeIcon
                icon={faCalendarAlt}
                className={styles["icon"]}
              />{" "}
              {new Date(user.role_start_at).toLocaleDateString()}
            </p>
          )}
        </div>
      </div>
      <div className={styles["tags-container"]}>
        {user.tags &&
          user.tags.map((tag, index) => (
            <div className={styles["tag"]} key={index}>
              {tag}
            </div>
          ))}
      </div>
    </div>
  );
}

export { UserCard };
